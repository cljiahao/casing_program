from apis.api_cm import api_get_empty, api_update_empty
from apis.api_pmss import api_get_lot_data, api_set_lot_data


def check_lot_exists(lot_no: str) -> dict[str, str | list[str]]:
    """Checks if the lot exists by making an API call to retrieve lot data."""

    json = api_get_lot_data(lot_no)
    if json["code"] != "0":
        raise LookupError(json["message"])

    return json["data"]


def check_cont_empty(cont_id: str) -> bool:
    """Checks if the container is empty by making an API call."""

    json = api_get_empty(cont_id)
    if not json:
        raise LookupError(f"Container ID: {cont_id} not found in system")

    return json[0]["kbv016"] == "0"


def check_set_lot_data(lot_data: dict[str, str | list[str]]) -> None:
    """Sets the lot data by making an API call to update the system."""
    print(lot_data)
    json = api_set_lot_data(lot_data)
    if json["code"] != "0":
        raise LookupError(json["message"])


def set_cont_not_empty(end_lot_cont_ids: list[str]) -> None:
    """Sets the containers as not empty by updating the system."""

    json = api_update_empty(end_lot_cont_ids)
    if json:
        raise LookupError("Something went wrong updating container")
    # if json["code"] != "0":
    #     raise LookupError(json["message"])
