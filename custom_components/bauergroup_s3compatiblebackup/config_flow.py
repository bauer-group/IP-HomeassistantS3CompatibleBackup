"""Config flow for the S3 Compatible Backup integration."""

from __future__ import annotations

from typing import Any

from aiobotocore.session import AioSession
from botocore.exceptions import ClientError, ConnectionError, ParamValidationError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
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
    CONF_REGION,
    CONF_SECRET_ACCESS_KEY,
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
    }
)


class S3CompatibleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for S3 Compatible Backup."""

    VERSION = 1

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
