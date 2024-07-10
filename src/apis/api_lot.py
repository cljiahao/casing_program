import os
import json
import requests

from core.config import settings


url_get_lot = f"{settings.PMSS_API_URL}/PMSS/rest/robotic/getLotStartData"
url_complete_lot = f"{settings.PMSS_API_URL}/PMSS/rest/robotic/completeLot"
url_update_cont = (
    f"{settings.PMSS_API_URL}/mnt/vol2/dockerdata/pmss/users/pmss/conet/robotic/recv"
)


def api_get_lot_data(lot_no: str):

    payload = json.dumps({"dsn": "orMesPMSS", "lotNo": lot_no})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url_get_lot, headers=headers, data=payload)

    return response.json()


def api_set_lot_data(data: dict):

    payload = json.dumps({"dsn": "orMesPMSS", "data": data})
    print(payload)
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url_complete_lot, headers=headers, data=payload)

    return response.json()


def api_update_cont(file_path: str):

    files = {"file": open(file_path, "rb")}
    resp = requests.post(url_update_cont, files=files)

    print(resp.content)

    return int(resp.content) == os.stat(file_path).st_size
