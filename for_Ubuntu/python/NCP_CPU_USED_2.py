import hashlib
import hmac
import base64
import requests
import time
import json
from datetime import datetime

## 01  unix timestamp Settings
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

## 02 NCP API Key Settings
access_key = "8z6s0NSPFKlSohYUb0QT"
secret_key = "bJtTFuI1q0GQjX8mxnQvjYWw0YZJPaUQffrZzwYo"
secret_key = bytes(secret_key, "UTF-8")

## 03 API 호출  정보
api_server = "https://cw.apigw.ntruss.com"
api_url = "/cw_fea/real/cw/api/data/query"
api_url = api_url + "?responseFormatType=json"
api_method = "POST"

## 04 전송 메세지 생성
message = api_method + " " + api_url + "\n" + timestamp + "\n" + access_key
message = bytes(message, "UTF-8")

## 05 전송 메세지 hmac 암호화
signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

## 06 http header Settings
http_header = {
  "x-ncp-apigw-signature-v2" : signingKey,
  "x-ncp-apigw-timestamp" : timestamp,
  "x-ncp-iam-access-key" : access_key,
}

## 07 payload Settings
# datetime variable

now=datetime.now()
#datetimeStart='2023-06-22 17:01:00'
#datetimeEnd='2023-06-22 17:02:00'
datetimeStart=now.date()
datetimeEnd=now.date()
nn = now.timestamp()

# convert datetime to timestamp
#resultdttStart=time.mktime(datetime.strptime(datetimeStart,'%Y-%m-%d %H:%M:%S').timetuple())
#resultdttEnd=time.mktime(datetime.strptime(datetimeEnd,'%Y-%m-%d %H:%M:%S').timetuple())

# timestamp to datetime

payload = {
#  "timeEnd": resultdttEnd+60000,
#  "timeStart": resultdttStart,
  "timeEnd": nn,
  "timeStart": nn-60,
  "prodName": "System/Server",
  "metric": "avg_cpu_used_rto",
  "interval": "Min1",
  "aggregation": "MAX",
  "cw_key": "460438474722512896",
  "dimensions": {
    "instanceNo": "17313154",
  }
}

## 08 execute call
response = requests.post(api_server + api_url, headers=http_header, json=payload)

data = json.loads(response.text)

## 09 write file n filter
f = open("avg_cpu.txt","w")
d = eval(str(data))

import datetime

for i in range(len(d)):
  dt = datetime.datetime.fromtimestamp(d[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S')
  txt = str(dt) + ' : ' + str(d[i][1]) + '\n'
  f.write(txt)
  print(dt, ":", d[i][1])

f.close()
