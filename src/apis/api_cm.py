import json
import requests

from core.config import service_settings


url_reg_cont = f"{service_settings.CM_API_URL}/robotic/getRegisteredContainer/"
url_empty_cont = f"{service_settings.CM_API_URL}/robotic/getEmptyContainerStatus/"
url_update_cont = f"{service_settings.CM_API_URL}/robotic/updateContainerStatus"
url_set_empty = f"{service_settings.CM_API_URL}/robotic/emptyContainerStatus"

headers = {
    "Content-Type": "application/json",
    "x-api-key": service_settings.ROB_API_KEY,
}


def api_get_registered(cont_id: str):

    response = requests.request("GET", url_reg_cont + cont_id, headers=headers)
    json = response.json()

    return not json


def api_get_empty(cont_id: str):

    response = requests.request("GET", url_empty_cont + cont_id, headers=headers)
    json = response.json()
    print(json)

    return json


def api_update_empty(cont_id: str | list):
    if isinstance(cont_id, str):
        cont_id = [{"nov062": cont_id}]
    data = json.dumps(cont_id)

    response = requests.request("POST", url_update_cont, headers=headers, data=data)

    return response.json()


def api_set_empty_cont(cont_id: str | list):

    if isinstance(cont_id, str):
        cont_id = [{"nov062": cont_id}]
    data = json.dumps(cont_id)

    response = requests.request("POST", url_set_empty, headers=headers, data=data)

    return response.json()
