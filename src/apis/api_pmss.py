import os
import json
import requests

from core.config import service_settings

# Define URLs for API endpoints
url_get_lot = f"{service_settings.PMSS_API_URL}/PMSS/rest/robotic/getLotStartData"
url_complete_lot = f"{service_settings.PMSS_API_URL}/PMSS/rest/robotic/completeLot"
url_update_cont = f"{service_settings.PMSS_API_URL}/mnt/vol2/dockerdata/pmss/users/pmss/conet/robotic/recv"

# Common headers for API requests
headers = {"Content-Type": "application/json"}

# Specify connect and request timeout
timeout = (5, 10)


def api_get_lot_data(lot_no: str) -> dict:
    """Fetches lot data for the given lot number."""

    payload = json.dumps({"dsn": "orMesPMSS", "lotNo": lot_no})

    try:
        response = requests.request(
            "POST", url_get_lot, headers=headers, data=payload, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("PMSS Server unable to be reached")

    return response.json()


def api_set_lot_data(data: dict) -> dict:
    """Sets or updates lot data."""

    payload = json.dumps({"dsn": "orMesPMSS", "data": data})

    try:
        response = requests.request(
            "POST", url_complete_lot, headers=headers, data=payload, timeout=timeout
        )
    except requests.ReadTimeout:
        raise TimeoutError("PMSS Server unable to be reached")

    return response.json()


def api_update_cont(file_path: str) -> bool:
    """Uploads a container file and verifies the upload size."""

    files = {"file": open(file_path, "rb")}

    try:
        resp = requests.post(url_update_cont, files=files, timeout=timeout)
        print(resp.content)
    except requests.ReadTimeout:
        raise TimeoutError("PMSS Server unable to be reached")

    return int(resp.content) == os.stat(file_path).st_size
