import pytest
import ksenia_lares

def test_init_for_IP():
    config = {
        "api_version": "IP",
        "username": "test_user",
        "password": "test_pass",
        "host": "192.168.1.1",
        "port": 8080,
    }

    api = ksenia_lares.get_api(config)

    assert isinstance(api, ksenia_lares.IpAPI)