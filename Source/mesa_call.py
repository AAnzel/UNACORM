import json
import time
import requests


__author__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian']
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian', 'Chisom Ezekannagha']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'AnzelA@rki.de'
__status__ = 'Stable'


# Attributes for API calling
string_url = 'https://mesa.mosla.de/api/all'
dict_header = {'content-type': 'application/json;charset=UTF-8'}
with open("mesa.json") as json_file:  # Config file for API
    dict_config_api = json.load(json_file)


# Running API
def run_requests(int_current, res_all, list_one_dna_strand, c, dict_payload,
                 dict_header, string_url):
    """This function is used for running the MESA API

    Args:
        res_all (list): container for API result
        list_one_dna_strand (list): encoded dna sequence
        c (int): initial number for length of dna list
        dict_payload (dict): API config
        dict_header (dict): API dict_header
        string_url (str): MESA API URL

    Returns:
        time_used (number): length of API run
    """
    start_time = time.time()

    for j in range(int_current, len(list_one_dna_strand)):
        dict_payload['sequence'] = list_one_dna_strand
        try:
            res = requests.post(string_url, data=json.dumps(dict_payload),
                                headers=dict_header)
            res_all.append(res)
            c += 1
        except Exception:
            print("Max retries, going to sleep for 100 sec.")
            print("j= " + str(j))
            time.sleep(100)
            run_requests(j, res_all, list_one_dna_strand, c, dict_payload,
                         dict_header, string_url)

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
    list_one_dna_strand = encoded_dna
    dict_payload = dict_config_api
    dict_payload['asHTML'] = False
    dict_payload["key"] = "9z5NOwZE5QEmU2h4-sAPIx7VhlGOxoEroK5Li2CjyaI"
    dict_payload["err_simulation_order"]["Storage/PCR"][0][
        "cycles"] = storage_length
    c = 0
    res_all = list()
    time_used = run_requests(
        0, res_all, list_one_dna_strand, c, dict_payload, dict_header,
        string_url)
    # print(time_used)
    dict_result = {}
    string_modified_sequence = ''

    for ent in res_all:
        dict_result = ent.json()

    for key, _ in dict_result.items():
        string_modified_sequence = dict_result[key]["res"]["modified_sequence"]

    return string_modified_sequence
