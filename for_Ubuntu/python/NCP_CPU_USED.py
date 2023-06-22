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
access_key = "E3F92A2DADB3CBD49CD2"
secret_key = "7322F05727836BF6544818A44B82B2E7FD322FDC"
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
datetimeStart = '2023-05-01 00:00:00'
datetimeEnd = '2023-05-31 00:00:00'

# convert datetime to timestamp
resultdttStart = time.mktime(datetime.strptime(datetimeStart,'%Y-%m-%d %H:%M:%S').timetuple())
resultdttEnd = time.mktime(datetime.strptime(datetimeEnd,'%Y-%m-%d %H:%M:%S').timetuple())

# timestamp to datetime
end_time  = time.time_ns()
start_time = end_time - 86400000
timeStart = str(start_time)
timeEnd = str(end_time)
instanceNo =

payload = {
  "timeEnd": resultdttEnd,
  "timeStart": resultdttStart,
  "prodName": "System/Server",
  "metric": "avg_cpu_used_rto",
  "interval": "Min1",
  "aggregation": "AVG",
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
f.write(str(data))
f.close()
