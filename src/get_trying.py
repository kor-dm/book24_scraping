from requests import get
from time import sleep

def try_get(url: str, headers: dict, repeat_count: int = 5):
    """
    Tries to get a response from the server several times
    """
    for i in range(repeat_count):
        response = get(url, headers = headers)
        if (response.status_code // 100 != 4 or response.status_code // 100 != 5): return response
        sleep(5)
    return response.status_code