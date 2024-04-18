import requests

from credentials import s_site


def check_connection():
    try:
        requests.get(s_site, timeout=10)
        result = True
    except (requests.exceptions.Timeout
            and requests.exceptions.HTTPError
            and requests.exceptions.RequestException
            ):
        result = False

    return result
