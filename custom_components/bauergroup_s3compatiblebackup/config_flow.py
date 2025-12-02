"""Config flow for the S3 Compatible Backup integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from aiobotocore.session import AioSession
from botocore.exceptions import ClientError, ConnectionError, ParamValidationError
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import (
    CONF_ACCESS_KEY_ID,
    CONF_BUCKET,
    CONF_ENDPOINT_URL,
    CONF_PREFIX,
    CONF_REGION,
    CONF_SECRET_ACCESS_KEY,
    DEFAULT_PREFIX,
    DEFAULT_REGION,
    DOMAIN,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_SECRET_ACCESS_KEY): TextSelector(
            config=TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_BUCKET): cv.string,
        vol.Required(CONF_ENDPOINT_URL): TextSelector(
            config=TextSelectorConfig(type=TextSelectorType.URL)
        ),
        vol.Required(CONF_REGION, default=DEFAULT_REGION): cv.string,
        vol.Optional(CONF_PREFIX, default=DEFAULT_PREFIX): cv.string,
    }
)

STEP_REAUTH_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_SECRET_ACCESS_KEY): TextSelector(
            config=TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
    }
)

STEP_RECONFIGURE_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_SECRET_ACCESS_KEY): TextSelector(
            config=TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_BUCKET): cv.string,
        vol.Required(CONF_ENDPOINT_URL): TextSelector(
            config=TextSelectorConfig(type=TextSelectorType.URL)
        ),
        vol.Required(CONF_REGION): cv.string,
        vol.Optional(CONF_PREFIX): cv.string,
    }
)


class S3CompatibleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for S3 Compatible Backup."""

    VERSION = 1

    _reauth_entry: ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Check for duplicate entries with same bucket and endpoint
            self._async_abort_entries_match(
                {
                    CONF_BUCKET: user_input[CONF_BUCKET],
                    CONF_ENDPOINT_URL: user_input[CONF_ENDPOINT_URL],
                }
            )

            try:
                session = AioSession()
                async with session.create_client(
                    "s3",
                    endpoint_url=user_input[CONF_ENDPOINT_URL],
                    aws_secret_access_key=user_input[CONF_SECRET_ACCESS_KEY],
                    aws_access_key_id=user_input[CONF_ACCESS_KEY_ID],
                    region_name=user_input.get(CONF_REGION, DEFAULT_REGION),
                ) as client:
                    await client.head_bucket(Bucket=user_input[CONF_BUCKET])
            except ClientError:
                errors["base"] = "invalid_credentials"
            except ParamValidationError as err:
                if "Invalid bucket name" in str(err):
                    errors[CONF_BUCKET] = "invalid_bucket_name"
            except ValueError:
                errors[CONF_ENDPOINT_URL] = "invalid_endpoint_url"
            except ConnectionError:
                errors[CONF_ENDPOINT_URL] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_BUCKET], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                STEP_USER_DATA_SCHEMA, user_input
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Handle re-authentication when credentials become invalid."""
        self._reauth_entry = self._get_reauth_entry()
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle re-authentication confirmation."""
        errors: dict[str, str] = {}

        if user_input is not None:
            assert self._reauth_entry is not None
            entry_data = self._reauth_entry.data

            try:
                session = AioSession()
                async with session.create_client(
                    "s3",
                    endpoint_url=entry_data[CONF_ENDPOINT_URL],
                    aws_secret_access_key=user_input[CONF_SECRET_ACCESS_KEY],
                    aws_access_key_id=user_input[CONF_ACCESS_KEY_ID],
                    region_name=entry_data.get(CONF_REGION, DEFAULT_REGION),
                ) as client:
                    await client.head_bucket(Bucket=entry_data[CONF_BUCKET])
            except ClientError:
                errors["base"] = "invalid_credentials"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    self._reauth_entry,
                    data_updates={
                        CONF_ACCESS_KEY_ID: user_input[CONF_ACCESS_KEY_ID],
                        CONF_SECRET_ACCESS_KEY: user_input[CONF_SECRET_ACCESS_KEY],
                    },
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=self.add_suggested_values_to_schema(
                STEP_REAUTH_DATA_SCHEMA,
                {CONF_ACCESS_KEY_ID: self._reauth_entry.data[CONF_ACCESS_KEY_ID]}
                if self._reauth_entry
                else None,
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is not None:
            # Check for duplicate entries with same bucket and endpoint (excluding current entry)
            self._async_abort_entries_match(
                {
                    CONF_BUCKET: user_input[CONF_BUCKET],
                    CONF_ENDPOINT_URL: user_input[CONF_ENDPOINT_URL],
                }
            )

            try:
                session = AioSession()
                async with session.create_client(
                    "s3",
                    endpoint_url=user_input[CONF_ENDPOINT_URL],
                    aws_secret_access_key=user_input[CONF_SECRET_ACCESS_KEY],
                    aws_access_key_id=user_input[CONF_ACCESS_KEY_ID],
                    region_name=user_input.get(CONF_REGION, DEFAULT_REGION),
                ) as client:
                    await client.head_bucket(Bucket=user_input[CONF_BUCKET])
            except ClientError:
                errors["base"] = "invalid_credentials"
            except ParamValidationError as err:
                if "Invalid bucket name" in str(err):
                    errors[CONF_BUCKET] = "invalid_bucket_name"
            except ValueError:
                errors[CONF_ENDPOINT_URL] = "invalid_endpoint_url"
            except ConnectionError:
                errors[CONF_ENDPOINT_URL] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    data_updates=user_input,
                    title=user_input[CONF_BUCKET],
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                STEP_RECONFIGURE_DATA_SCHEMA, reconfigure_entry.data
            ),
            errors=errors,
        )
