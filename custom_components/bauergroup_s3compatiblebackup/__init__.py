"""The S3 Compatible Backup integration."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from queue import Queue
from threading import Thread
from typing import Any, cast

from aiobotocore.session import AioSession
from botocore.exceptions import ClientError, ConnectionError, ParamValidationError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryError, ConfigEntryNotReady

from .const import (
    CONF_ACCESS_KEY_ID,
    CONF_BUCKET,
    CONF_ENDPOINT_URL,
    CONF_REGION,
    CONF_SECRET_ACCESS_KEY,
    DATA_BACKUP_AGENT_LISTENERS,
    DEFAULT_REGION,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class S3ClientWrapper:
    """Wrapper for S3 client that runs all operations in a dedicated worker thread.

    This avoids blocking the main Home Assistant event loop with botocore's
    synchronous I/O operations (listdir, file reads, SSL certificate loading).
    All S3 operations are dispatched to a worker thread with its own event loop.
    """

    def __init__(
        self,
        endpoint_url: str | None,
        access_key: str,
        secret_key: str,
        region: str,
        bucket: str,
    ) -> None:
        """Initialize the wrapper and start the worker thread."""
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key
        self._region = region
        self._bucket = bucket
        self._client: Any = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: Thread | None = None
        self._started = False

    def _run_worker_loop(self) -> None:
        """Run the worker event loop in a dedicated thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _create_client(self) -> None:
        """Create the S3 client (runs in worker thread)."""
        session = AioSession()
        # pylint: disable-next=unnecessary-dunder-call
        self._client = await session.create_client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_secret_access_key=self._secret_key,
            aws_access_key_id=self._access_key,
            region_name=self._region,
        ).__aenter__()
        # Verify credentials and warm SSL context
        await self._client.head_bucket(Bucket=self._bucket)

    async def _close_client(self) -> None:
        """Close the S3 client (runs in worker thread)."""
        if self._client:
            await self._client.__aexit__(None, None, None)
            self._client = None

    def start(self) -> None:
        """Start the worker thread and create the client.

        This method blocks until the client is ready.
        Should be called from an executor via hass.async_add_executor_job.
        """
        if self._started:
            return

        # Start worker thread
        self._thread = Thread(target=self._run_worker_loop, daemon=True)
        self._thread.start()

        # Wait for loop to be ready
        while self._loop is None:
            pass

        # Create client in worker thread
        future = asyncio.run_coroutine_threadsafe(self._create_client(), self._loop)
        future.result()  # Block until client is created
        self._started = True

    def stop(self) -> None:
        """Stop the worker thread and close the client.

        Should be called from an executor via hass.async_add_executor_job.
        """
        if not self._started or self._loop is None:
            return

        # Close client in worker thread
        future = asyncio.run_coroutine_threadsafe(self._close_client(), self._loop)
        future.result()

        # Stop the loop
        self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=5)
        self._started = False

    async def _dispatch[T](self, coro: Any) -> T:
        """Dispatch a coroutine to the worker thread and await its result."""
        if self._loop is None:
            raise RuntimeError("Worker loop not started")
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return await asyncio.wrap_future(future)

    async def head_bucket(self, **kwargs: Any) -> dict[str, Any]:
        """Check if a bucket exists and is accessible."""
        return await self._dispatch(self._client.head_bucket(**kwargs))

    async def list_objects_v2(self, **kwargs: Any) -> dict[str, Any]:
        """List objects in a bucket."""
        return await self._dispatch(self._client.list_objects_v2(**kwargs))

    async def get_object(self, **kwargs: Any) -> dict[str, Any]:
        """Get an object from a bucket."""
        return await self._dispatch(self._client.get_object(**kwargs))

    async def get_object_body(self, **kwargs: Any) -> bytes:
        """Get an object and read its full body in the worker thread.

        This avoids the 'Future attached to a different loop' error that occurs
        when trying to read a response body stream from a different event loop.
        Use this for small objects (e.g., metadata JSON files).
        """

        async def _get_and_read() -> bytes:
            response = await self._client.get_object(**kwargs)
            return await response["Body"].read()

        return await self._dispatch(_get_and_read())

    async def get_object_stream(self, **kwargs: Any) -> AsyncIterator[bytes]:
        """Get an object and stream its body from the worker thread.

        Uses a thread-safe queue to bridge the worker thread's event loop
        and the caller's event loop for streaming large objects (e.g., backups).
        """
        data_queue: Queue[bytes | None] = Queue()
        error_holder: list[BaseException | None] = [None]

        async def _stream_body() -> None:
            try:
                response = await self._client.get_object(**kwargs)
                async for chunk in response["Body"].iter_chunks():
                    data_queue.put(chunk)
            except BaseException as exc:
                error_holder[0] = exc
            finally:
                data_queue.put(None)  # Sentinel to signal completion

        if self._loop is None:
            raise RuntimeError("Worker loop not started")
        asyncio.run_coroutine_threadsafe(_stream_body(), self._loop)

        loop = asyncio.get_running_loop()
        while True:
            chunk = await loop.run_in_executor(None, data_queue.get)
            if chunk is None:
                if error_holder[0] is not None:
                    raise error_holder[0]
                break
            yield chunk

    async def put_object(self, **kwargs: Any) -> dict[str, Any]:
        """Put an object into a bucket."""
        return await self._dispatch(self._client.put_object(**kwargs))

    async def delete_object(self, **kwargs: Any) -> dict[str, Any]:
        """Delete an object from a bucket."""
        return await self._dispatch(self._client.delete_object(**kwargs))

    async def create_multipart_upload(self, **kwargs: Any) -> dict[str, Any]:
        """Initiate a multipart upload."""
        return await self._dispatch(self._client.create_multipart_upload(**kwargs))

    async def upload_part(self, **kwargs: Any) -> dict[str, Any]:
        """Upload a part in a multipart upload."""
        return await self._dispatch(self._client.upload_part(**kwargs))

    async def complete_multipart_upload(self, **kwargs: Any) -> dict[str, Any]:
        """Complete a multipart upload."""
        return await self._dispatch(self._client.complete_multipart_upload(**kwargs))

    async def abort_multipart_upload(self, **kwargs: Any) -> dict[str, Any]:
        """Abort a multipart upload."""
        return await self._dispatch(self._client.abort_multipart_upload(**kwargs))


type S3CompatibleConfigEntry = ConfigEntry[S3ClientWrapper]


async def async_setup_entry(hass: HomeAssistant, entry: S3CompatibleConfigEntry) -> bool:
    """Set up S3 Compatible Backup from a config entry."""

    data = cast(dict, entry.data)
    region = data.get(CONF_REGION, DEFAULT_REGION)

    # Create wrapper that will run S3 client in dedicated worker thread
    wrapper = S3ClientWrapper(
        endpoint_url=data.get(CONF_ENDPOINT_URL),
        access_key=data[CONF_ACCESS_KEY_ID],
        secret_key=data[CONF_SECRET_ACCESS_KEY],
        region=region,
        bucket=data[CONF_BUCKET],
    )

    try:
        # Start wrapper in executor - all blocking I/O happens in worker thread
        await hass.async_add_executor_job(wrapper.start)
    except ClientError as err:
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="invalid_credentials",
        ) from err
    except ParamValidationError as err:
        if "Invalid bucket name" in str(err):
            raise ConfigEntryError(
                translation_domain=DOMAIN,
                translation_key="invalid_bucket_name",
            ) from err
        raise
    except ValueError as err:
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="invalid_endpoint_url",
        ) from err
    except ConnectionError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
        ) from err

    entry.runtime_data = wrapper

    def notify_backup_listeners() -> None:
        for listener in hass.data.get(DATA_BACKUP_AGENT_LISTENERS, []):
            listener()

    entry.async_on_unload(entry.async_on_state_change(notify_backup_listeners))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: S3CompatibleConfigEntry) -> bool:
    """Unload a config entry."""
    wrapper = entry.runtime_data
    await hass.async_add_executor_job(wrapper.stop)
    return True
