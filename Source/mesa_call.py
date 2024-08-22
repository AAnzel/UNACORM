import json
import time
import requests


# Attributes for API calling
url = 'https://mesa.mosla.de/api/all'
header = {'content-type': 'application/json;charset=UTF-8'}
with open("mesa.json") as json_file:  # Config file for API
    config_api = json.load(json_file)


# Running API
def run_requests(res_all, entry_list, c, payload, header, url):
    """This function is used for running the MESA API

    Args:
        res_all (list): container for API result
        entry_list (list): encoded dna sequence
        c (int): initial number for length of dna list
        payload (dict): API config
        header (dict): API header
        url (str): MESA API URL

    Returns:
        time_used (number): length of API run
    """
    start_time = time.time()
    try:
        for j in range(0, len(entry_list)):
            payload['sequence'] = entry_list[j]
            res = requests.post(url, data=json.dumps(payload), headers=header)
            res_all.append(res)
            c += 1
    except Exception:
        print("Max retries, going to sleep for 100 sec.")
        print("j= " + str(j))
        time.sleep(100)
        run_requests(j, res_all, entry_list, c, payload, header, url)
    time_used = time.time() - start_time

    return time_used


# Setup parameter and call API
def api_call(encoded_dna, storage_length):
    """This function is used for calling MESA API and setup input parameter

    Args:
        encoded_dna (list): encoded DNA sequence
        storage_length (str): length of storage

    Returns:
        modified_sequence (str): modified sequence sequence
    """
    entry_list = encoded_dna
    payload = config_api
    payload['asHTML'] = False
    payload["key"] = "9z5NOwZE5QEmU2h4-sAPIx7VhlGOxoEroK5Li2CjyaI"
    payload["err_simulation_order"]["Storage/PCR"][0][
        "cycles"] = storage_length
    c = 0
    res_all = list()
    time_used = run_requests(res_all, entry_list, c, payload, header, url)
    print(time_used)

    for ent in res_all:
        result = ent.json()

    for key, value in result.items():
        modified_sequence = result[key]["res"]["modified_sequence"]
    return modified_sequence
