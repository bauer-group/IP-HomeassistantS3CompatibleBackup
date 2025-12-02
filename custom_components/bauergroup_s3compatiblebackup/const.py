"""Constants for the S3 Compatible Backup integration."""

from collections.abc import Callable
from typing import Final

from homeassistant.util.hass_dict import HassKey

DOMAIN: Final = "bauergroup_s3compatiblebackup"

CONF_ACCESS_KEY_ID = "access_key_id"
CONF_SECRET_ACCESS_KEY = "secret_access_key"
CONF_ENDPOINT_URL = "endpoint_url"
CONF_BUCKET = "bucket"
CONF_REGION = "region"

DEFAULT_REGION = "us-east-1"

DATA_BACKUP_AGENT_LISTENERS: HassKey[list[Callable[[], None]]] = HassKey(
    f"{DOMAIN}.backup_agent_listeners"
)
