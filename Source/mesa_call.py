import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Anyabolu"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


# Attributes for API calling

_UNACORM_IS_IN_DOCKER_CONTAINER = os.environ.get(
    "UNACORM_IS_IN_DOCKER_CONTAINER", ""
).lower() in ("yes", "y", "on", "true", "1")

if _UNACORM_IS_IN_DOCKER_CONTAINER:
    _STRING_MESA_URL = "http://host.docker.internal:5000/api/all"
else:
    _STRING_MESA_URL = "http://127.0.0.1:5000/api/all"
_STRING_MESA_KEY = "UNACORM_ADMIN_API_KEY"
_DICT_MESA_HEADER = {"content-type": "application/json;charset=UTF-8"}
_INT_MAX_RETRY_FOR_SESSION = 2
_FLOAT_BACK_OFF_FACTOR = 0.3
_LIST_ERROR_CODES = (500, 502, 504)
with open("mesa.json") as json_file:  # Config file for API
    _DICT_MESA_CONFIG_API = json.load(json_file)


def tuple_mesa_available():
    try:
        response = requests.options(_STRING_MESA_URL)
        if response.ok:  # alternatively you can use response.status_code == 200
            _STRING_MESSAGE = "Success — MESA API is accessible"
            return (True, _STRING_MESSAGE, "")
        else:
            _STRING_MESSAGE = (
                "Failure — MESA API is accessible but something is not right."
            )
            _STRING_ERROR = str(response.status_code)

            return (False, _STRING_MESSAGE, _STRING_ERROR)
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
    ) as e:
        _STRING_MESSAGE = "Failure — Unable to establish connection with MESA."
        _STRING_ERROR = str(e)
        return (False, _STRING_MESSAGE, _STRING_ERROR)
    except Exception as e:
        _STRING_MESSAGE = "Failure — Unknown error occurred with MESA."
        _STRING_ERROR = str(e)
        return (False, _STRING_MESSAGE, _STRING_ERROR)


def requests_retry_session(
    retries=_INT_MAX_RETRY_FOR_SESSION,
    backoff_factor=_FLOAT_BACK_OFF_FACTOR,
    status_force_list=_LIST_ERROR_CODES,
    session=requests.Session(),
):
    session = session
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=_FLOAT_BACK_OFF_FACTOR,
        status_forcelist=status_force_list,
        allowed_methods=frozenset(["GET", "POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def string_api_call(list_encoded_dna, int_storage_length):
    """
    string_api_call function sends a POST method to MESA containing the
    original DNA sequence and a set of parameters and returns a modified DNA
    sequences

    Args:
        list_encoded_dna (list): a list that cotains only one encoded DNA
        sequence
        int_storage_length (int): length of storage in years

    Returns:
        modified_sequence (str): modified sequence sequence
    """
    dict_payload = _DICT_MESA_CONFIG_API
    dict_payload["asHTML"] = False
    dict_payload["key"] = _STRING_MESA_KEY
    dict_payload["err_simulation_order"]["Storage/PCR"][0]["cycles"] = (
        int_storage_length
    )
    dict_payload["sequence"] = list_encoded_dna

    mesa_response = requests.post(
        _STRING_MESA_URL,
        data=json.dumps(dict_payload),
        headers=_DICT_MESA_HEADER,
    )

    dict_result = mesa_response.json()
    string_modified_sequence = ""

    string_modified_sequence = dict_result[list_encoded_dna[0]][
        "modified_sequence"
    ]

    return string_modified_sequence
