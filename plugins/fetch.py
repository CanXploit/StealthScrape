import requests
from plugins.log import log

def check_host(url):
    log("check")

    if "http://" not in url and "https://" not in url:
        url = "http://" + url  

    try:
        res = requests.get(url)
        if res.status_code == 200:
            log("check_alive")
        else:
            log("check_not_alive")
    except requests.exceptions.RequestException:
        log("check_not_alive")
