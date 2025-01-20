"""DingTalk bot notification service."""
import base64
import hashlib
import hmac
import json
import time
import urllib.parse
import logging
import requests
import voluptuous as vol

from homeassistant.const import (
    CONF_NAME,
    CONF_ACCESS_TOKEN,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

_LOGGER = logging.getLogger(__name__)
CONF_SECRET = "secret"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
    vol.Optional(CONF_SECRET): cv.string,
    vol.Optional(CONF_NAME): cv.string
})

def get_service(hass, config, discovery_info=None):
    """Get the DingTalk notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    secret = config.get(CONF_SECRET)
    name = config.get(CONF_NAME)
    return DingTalkNotificationService(access_token, secret, name)

class DingTalkNotificationService(BaseNotificationService):
    """Implementation of the notification service for DingTalk."""

    def __init__(self, access_token, secret=None, name=None):
        """Initialize the service."""
        self._access_token = access_token
        self._secret = secret
        self._name = name

    def _get_sign(self):
        """Get signed URL."""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self._secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self._secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def send_message(self, message="", **kwargs):
        """Send message to DingTalk."""
        url = f'https://oapi.dingtalk.com/robot/send?access_token={self._access_token}'
        
        if self._secret is not None:
            timestamp, sign = self._get_sign()
            url = f'{url}&timestamp={timestamp}&sign={sign}'

        title = kwargs.get("title", "Home Assistant")
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{title}\n{message}"
            }
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            _LOGGER.debug("Message sent to DingTalk successfully")
        except requests.exceptions.RequestException as error:
            _LOGGER.error("Error sending message to DingTalk: %s", error)
