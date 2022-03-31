import requests

def get_hotmail(api):

    get = requests.get(('http://dongvanfb.com/api/buyaccount.php?apiKey={0}&type=1&amount=1').format(api)).json()
    account = str(get['accounts'])

    for i in range(len(account)):
        if account[i] == '|':
            mail = account[:i]
            password = account[i+1:]
    return mail, password

def get_code_hotmail(api,mail,password):

    get = requests.get(('http://fbvip.org/api/ordercode.php?apiKey={0}&type=1&user={1}&pass={2}').format(api,mail,password)).json()
    id = get['id']
    code = requests.get(('http://fbvip.org/api/getcode.php?apiKey=7b537fb6a4d5d1dafbd4750ecbf29f74&id={0}').format(id)).json()
    return code['code']


print(get_hotmail("7b537fb6a4d5d1dafbd4750ecbf29f74"))