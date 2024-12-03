from tkinter import END
from tkinter import Entry, messagebox

from apis.api_cm import (
    api_get_empty,
    api_set_empty_cont,
    api_update_empty,
)
from apis.api_pmss import api_get_lot_data, api_set_lot_data
from db.session import get_db
from db.repository.casing import (
    check_cont_exists,
    check_cont_full,
    create_reel_data,
    delete_reel_data,
    get_cont_id_with_reel,
    get_cont_scan_reels,
    get_scan_reel,
    get_scan_reels_cnt,
    get_incomplete_cont,
)


def clearValue(widget: any) -> None:
    widget.after_idle(lambda: delete_entry(widget))
    widget.focus()


def delete_entry(entry_value: Entry) -> None:
    entry_value.delete(0, END)
    entry_value.configure(validate="key")


def check_state(lot_input: str, cont_input: str, in_db: bool = False) -> bool:

    lot_cont_exists = set(check_cont_exists(next(get_db()), cont_input))

    if not lot_cont_exists:
        return not in_db

    if len(lot_cont_exists) == 1:
        if lot_input in lot_cont_exists:
            return in_db
        else:
            raise ValueError(
                f"Container: {cont_input} in another lot: {''.join(map(str,lot_cont_exists))}."
            )
    raise ValueError(f"Container: {cont_input} tied to multiple lot in database.")


def check_cache(keys, cache):

    miss_key = []
    for k in keys:
        if not cache[k]:
            miss_key.append(k)

    if miss_key:
        raise ValueError(
            f"Please ensure {', '.join(miss_key)} entry boxes are correct."
        )


def lotNo(wos_entry: dict, lot_input: str, cache: dict) -> tuple[int, list[dict]]:

    check_cache(["optcode"], cache)

    # Check if operator code has input
    opt_code = wos_entry["OptCode"].get()
    if len(opt_code) != 7:
        raise ValueError("Please Scan Operator ID First.")

    # API call to server if lot exists
    json = api_get_lot_data(lot_input)
    if json["code"] != "0":
        raise LookupError(json["message"])

    lot_data = json["data"]
    reel_per_box = int(lot_data["reelPerBox"])
    reel_ids = lot_data.pop("ReelID")

    # Get scanned reels from cached data
    reel_count = get_scan_reels_cnt(next(get_db()), lot_input)

    # Update the WOS GUI with information retrieved
    for key, value in lot_data.items():
        if key in wos_entry.keys() and "label" in wos_entry[key].winfo_name():
            if "noOfReel" == key:
                value = f"{reel_count} / {value}"
            wos_entry[key].config(text=value)

    cache["lot"] = True
    wos_entry["contid"].focus()

    return reel_per_box, reel_ids


def contId(
    wos_entry: dict, lot_input: str, cont_input: str, reel_per_box: int, cache: dict
) -> None:

    check_cache(["optcode", "lot"], cache)

    # API call to server if lot exists
    json = api_get_lot_data(lot_input)
    if json["code"] != "0":
        raise LookupError(json["message"])

    # Check if cont_id exists and same as lot input in database
    _ = check_state(lot_input, cont_input, True)

    # Retrieve uncomplete cont with reels below reelperbox from server
    incomplete_cont = get_incomplete_cont(next(get_db()), lot_input, reel_per_box)
    if incomplete_cont:
        cont_id, reel_count = incomplete_cont
        if cont_id != cont_input:
            raise ValueError(
                f"Please complete Container {cont_id} filled with {reel_count} reels.",
            )

    # Check if scanning into cont more than reelperbox from server
    cont_full = check_cont_full(next(get_db()), lot_input, cont_input, reel_per_box)
    if cont_full:
        raise ValueError(f"Scanning more reels to full container: {cont_input}.")

    # Check server if container exists and empty, reset based on input
    json = api_get_empty(cont_input)
    if json:
        res = True if json[0]["kbv016"] == "0" else False
        if not res:
            # TODO Messagebox make bigger and vibrant
            if not messagebox.askyesno(
                title="Reset Container if not empty",
                message="Is Container Empty?",
            ):
                raise ValueError(f"Wrong container ID: {cont_input} scanned.")
            api_set_empty_cont(cont_input)
    else:
        raise LookupError(f"Container ID: {cont_id} not found in system.")

    cache["contid"] = True
    wos_entry["Reelid"].focus()


def reelId(
    wos_entry: dict, reel_input: str, reel_per_box: int, reel_ids: list, cache: dict
) -> None:

    check_cache(cache.keys(), cache)

    lot_input = wos_entry["lotNo"].get()
    cont_input = wos_entry["contid"].get()
    value = wos_entry["noOfReel"].cget("text").split("/ ")[-1]
    clear = False

    # Check if reel_input in reel_ids from server
    if reel_input not in reel_ids:
        raise LookupError(f"Reel: {reel_input} not found in system.")

    # Check if reel scanned before into container
    cont_id = get_cont_id_with_reel(next(get_db()), lot_input, reel_input)
    if cont_id:
        raise ValueError(
            f"Reel already scanned before in {cont_id}.",
        )

    # Check if cont_id exists and same as lot input in database
    lot_cont_exists = check_state(lot_input, cont_input)
    if not lot_cont_exists and not cache["contid"]:
        raise LookupError(f"Container ID: {cont_input} not found in system.")

    # Add Reel Data into Database
    reel_data = {
        "lotNo": lot_input,
        "contid": cont_input,
        "ReelID": reel_input,
    }

    create_reel_data(next(get_db()), reel_data)

    # Get scanned reel count from database
    reel_count = get_scan_reels_cnt(next(get_db()), lot_input)
    value = f"{reel_count} / {value}"
    wos_entry["noOfReel"].config(text=value)

    # Check if container is now reelperbox from server
    cont_full = check_cont_full(next(get_db()), lot_input, cont_input, reel_per_box)
    if cont_full:
        clear = True

    # Clear entry for next scan
    clearValue(wos_entry["Reelid"])
    if clear:
        clearValue(wos_entry["contid"])


def reelValidation(lot_input: str, reel_ids: list) -> list[str]:

    # Get scanned reels from database
    reels = get_scan_reel(next(get_db()), lot_input)

    # Missing reels that has not been scanned
    miss_reels = [r for r in reels if r not in reel_ids]

    # Delete extra reels that has been scanned but not in server
    extra_reels = [r for r in reel_ids if r not in reels]
    for reel in extra_reels:
        delete_reel_data(next(get_db()), reel)

    return miss_reels


def endLot(lot_input: str, opt_code: str) -> bool:

    # API call to server if lot exists
    json = api_get_lot_data(lot_input)
    if json["code"] != "0":
        raise LookupError(json["message"])

    lot_data = json["data"]
    lot_data["OptCode"] = opt_code
    reel_ids = lot_data.pop("ReelID")

    validation = reelValidation(lot_input, reel_ids)
    if validation:
        raise ValueError(f"Reels not fully scanned. Missing {validation}.")

    # Get scanned reels and container based on input lot
    containers = get_cont_scan_reels(next(get_db()), lot_input)

    # Formatting for server end lot
    cont_dict = {}
    for cont in containers:
        if cont.contid in cont_dict.keys():
            cont_dict[cont.contid].append(
                {
                    "id": cont.ReelID,
                    "seq": f"{(len(cont_dict[cont.contid]) + 1) / 100:.2f}".split(".")[
                        -1
                    ],
                }
            )
        else:
            cont_dict[cont.contid] = [{"id": cont.ReelID, "seq": "01"}]

    cont_arr = []
    for j, key in enumerate(cont_dict):
        cont_arr.append(
            {
                "contid": key,
                "contSeq": f"{(j + 1) / 1000:.3f}".split(".")[-1],
                "Reelid": cont_dict[key],
            }
        )

    lot_data["Contid"] = cont_arr

    json = api_set_lot_data(lot_data)
    if json["code"] != "0":
        raise LookupError(json["message"])

    # Update container to server
    for cont_id in cont_dict:
        api_update_empty(cont_id)
    # Remove data from database
    for cont in containers:
        delete_reel_data(next(get_db()), cont.ReelID)

    #     dat_str = f"S20|{dt.now().strftime('%Y/%m/%d %H:%M:%S')}|{response["OptCode"]}|{contid}|1"
    #     dat_path = f"./data/{contid}.dat"
    #     write_dat(dat_path, dat_str)
    #     update_cont(dat_path)

    return True
