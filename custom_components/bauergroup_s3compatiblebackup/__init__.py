"""The S3 Compatible Backup integration."""

from __future__ import annotations

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


async def async_setup_entry(hass: HomeAssistant, entry: S3CompatibleConfigEntry) -> bool:
    """Set up S3 Compatible Backup from a config entry."""

    data = cast(dict, entry.data)
    region = data.get(CONF_REGION, DEFAULT_REGION)

    try:
        session = AioSession()
        # pylint: disable-next=unnecessary-dunder-call
        client = await session.create_client(
            "s3",
            endpoint_url=data.get(CONF_ENDPOINT_URL),
            aws_secret_access_key=data[CONF_SECRET_ACCESS_KEY],
            aws_access_key_id=data[CONF_ACCESS_KEY_ID],
            region_name=region,
        ).__aenter__()
        await client.head_bucket(Bucket=data[CONF_BUCKET])
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
