"""The S3 Compatible Backup integration."""

from __future__ import annotations

import asyncio
import logging
from typing import cast

from aiobotocore.client import AioBaseClient as BotoClient
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

type S3CompatibleConfigEntry = ConfigEntry[BotoClient]


_LOGGER = logging.getLogger(__name__)


def _verify_s3_credentials(
    endpoint_url: str | None,
    access_key: str,
    secret_key: str,
    region: str,
    bucket: str,
) -> None:
    """Verify S3 credentials in executor to avoid blocking the event loop.

    This creates a temporary client in a separate thread with its own event loop.
    All blocking operations (botocore data loading, SSL certificate loading)
    happen here, warming the OS-level caches for subsequent client creation.
    """

    async def _verify() -> None:
        session = AioSession()
        async with session.create_client(
            "s3",
            endpoint_url=endpoint_url,
            aws_secret_access_key=secret_key,
            aws_access_key_id=access_key,
            region_name=region,
        ) as client:
            await client.head_bucket(Bucket=bucket)

    asyncio.run(_verify())


async def async_setup_entry(hass: HomeAssistant, entry: S3CompatibleConfigEntry) -> bool:
    """Set up S3 Compatible Backup from a config entry."""

    data = cast(dict, entry.data)
    region = data.get(CONF_REGION, DEFAULT_REGION)

    try:
        # Verify credentials in executor to avoid blocking the event loop
        # with botocore's synchronous I/O operations (listdir, file reads, SSL loading)
        await hass.async_add_executor_job(
            _verify_s3_credentials,
            data.get(CONF_ENDPOINT_URL),
            data[CONF_ACCESS_KEY_ID],
            data[CONF_SECRET_ACCESS_KEY],
            region,
            data[CONF_BUCKET],
        )

        # Create the actual client for runtime use
        # OS-level caches are now warm from the verification step
        session = AioSession()
        # pylint: disable-next=unnecessary-dunder-call
        client = await session.create_client(
            "s3",
            endpoint_url=data.get(CONF_ENDPOINT_URL),
            aws_secret_access_key=data[CONF_SECRET_ACCESS_KEY],
            aws_access_key_id=data[CONF_ACCESS_KEY_ID],
            region_name=region,
        ).__aenter__()
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

    entry.runtime_data = client

    def notify_backup_listeners() -> None:
        for listener in hass.data.get(DATA_BACKUP_AGENT_LISTENERS, []):
            listener()

    entry.async_on_unload(entry.async_on_state_change(notify_backup_listeners))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: S3CompatibleConfigEntry) -> bool:
    """Unload a config entry."""
    client = entry.runtime_data
    await client.__aexit__(None, None, None)
    return True
