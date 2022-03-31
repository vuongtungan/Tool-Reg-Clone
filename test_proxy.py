import requests

def get_current_proxy(api):

    param = {
        "api_key": api
    }
    request = requests.post("https://tmproxy.com/api/proxy/get-current-proxy", json=param).json()
    proxy = request['data']['https']

    return proxy

def get_new_proxy(api):

    param = {
        "api_key": api
    }
    request = requests.post("https://tmproxy.com/api/proxy/get-new-proxy", json=param).json()
    proxy = request['data']['https']

    return proxy

def check_ip_refresh(api):

    param = {
        "api_key": api
    }
    request = requests.post("https://tmproxy.com/api/proxy/get-new-proxy", json=param).json()

    if request['data']['https'] == '':
        return False
    return True

proxy = check_ip_refresh('c86fbeaca7eb5a4b2fb07d3697410bab')
print(proxy)
