import requests,json

def getNumber(api):

    param = "&apikey={0}&action=create-request&serviceId=1&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['sdt'], number['requestId']

def getOTP(api,requestid):

    param = "&apikey={0}&action=data-request&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp
def getMail(api):

    param = "&apikey={0}&action=create-request&serviceId=3&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['email'], number['requestId']

def getOTPMail(api,requestid):

    param = "&apikey={0}&action=data-request-tempmail&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp

def get_number_VOTP(api):

    get = requests.get(("https://api.viotp.com/request/get?token={0}&serviceId=7").format(api)).json()

    number = get['data']['phone_number']
    id = get['data']['request_id']

    return number, id

def get_otp_VOTP(api,id):

    get = requests.get(('https://api.viotp.com/session/get?requestId={0}&token={1}').format(id,api)).json()

    #otp = get['data']['Code']

    return get


#print(getNumber("cb88587449e021accb66b5b99648f1fb"))
#print(getOTP("cb88587449e021accb66b5b99648f1fb",getNumber("cb88587449e021accb66b5b99648f1fb")[1]))
#print(getMail("cb88587449e021accb66b5b99648f1fb"))

number, id = get_number_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523')

print(get_otp_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523', id))