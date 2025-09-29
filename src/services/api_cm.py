import json
import requests

from core.config import service_settings

# Define URLs for API endpoints
url_reg_cont = f"{service_settings.CM_API_URL}/robotic/getRegisteredContainer/"
url_empty_cont = f"{service_settings.CM_API_URL}/robotic/getEmptyContainerStatus/"
url_update_cont = f"{service_settings.CM_API_URL}/robotic/updateContainerStatus"
url_set_empty = f"{service_settings.CM_API_URL}/robotic/emptyContainerStatus"

# Common headers for API requests
headers = {
    "Content-Type": "application/json",
    "x-api-key": service_settings.ROB_API_KEY,
}

# Specify connect and request timeout
timeout = (5, 10)


def api_get_registered(cont_id: str) -> bool:
    """Checks if a container is registered."""

    try:
        response = requests.request(
            "GET", url_reg_cont + cont_id, headers=headers, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("CM Server unable to be reached")

    return not response.json()


def api_get_empty(cont_id: str) -> dict:
    """Retrieves the empty status of a container."""

    try:
        response = requests.request(
            "GET", url_empty_cont + cont_id, headers=headers, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("CM Server unable to be reached")

    return response.json()


def api_update_empty(cont_id: str | list[dict]) -> dict:
    """Updates the empty status of a container."""

    if isinstance(cont_id, str):
        cont_id = [{"nov062": cont_id}]
    data = json.dumps(cont_id)

    try:
        response = requests.request(
            "POST", url_update_cont, headers=headers, data=data, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("CM Server unable to be reached")

    return response.json()


def api_set_empty_cont(cont_id: str | list[dict]) -> dict:
    """Sets the empty status of a container."""

    if isinstance(cont_id, str):
        cont_id = [{"nov062": cont_id}]
    data = json.dumps(cont_id)

    try:
        response = requests.request(
            "POST", url_set_empty, headers=headers, data=data, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("CM Server unable to be reached")

    return response.json()
