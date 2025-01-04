"""Unofficial python API for the Ksenia Lares alarm."""

from .base_api import BaseApi
from .ip_api import IpAPI

def get_api(config: dict) -> BaseApi:
    """
    Get and initialize the correct API class based on the `api_version` given. 
    Args:
            config (dict): A dictionary containing the following keys:
                - api_version (str): IP for IP range or 4 for Lares 4.0.

    """
    version = config.get("api_version")
    if version == "IP":
        return IpAPI(config)

    if version == "IP":
        raise ValueError("Lares 4.0 API not yet supported")

    raise ValueError(f"Unsupported API version: {version}")
