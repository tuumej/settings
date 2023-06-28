"""
-----------------------------
파일명         : monitor.py
생성일자       : 2023-06-23
생성자         : ljw
최종수정일자   : 2023-06-27
최종수정자     : 
설명           : 
- NCP 공공 기관용
- 서버 리소스 사용량 조회(cpu,mem,diski)
------------------------------
"""
import os
import sys
import hashlib
import hmac
import base64
import requests
import json
import time
from datetime import datetime

# 다른 py 파일을 import 시 경로를 못찾는 문제 해결.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from customer.cnu_server_info import *

## 01. 데이터 조회

now = datetime.now()

timeEnd = now.timestamp() 
timeStart = now.timestamp() - 120

timestampMin1 = now.timestamp() - 60

dt = datetime.fromtimestamp(timestampMin1)
dt_str = str(dt.strftime('%Y-%m-%d %H:%M:00'))

timestamp = int(time.time() * 1000)

# metric list
m_list = ['avg_cpu_used_rto', 'mem_usert', 'avg_fs_usert']

# aggregation list
#ag_list = ['MIN', 'MAX', 'AVG']
ag_list = ['AVG']

# api info
access_key = ""
secret_key = ""
secret_key = bytes(secret_key, "UTF-8")

api_server = "https://cw.apigw.gov-ntruss.com"
api_url = "/cw_fea/real/cw/api/data/query"
api_url = api_url + "?responseFormatType=json"
api_method = "POST"

# message info
message = api_method + " " + api_url + "\n" + str(timestamp) + "\n" + access_key
message = bytes(message, "UTF-8")

signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

# http header
http_header = {
  "x-ncp-apigw-signature-v2" : signingKey,
  "x-ncp-apigw-timestamp" : str(timestamp),
  "x-ncp-iam-access-key" : access_key,
}

# payload data
cw_key = "567435234753253376"

# main exe
server_resource_used = ''

for i in range(int(server_info["serverCount"])):
  if i == 0:
    server_resource_used += "[{"
  else:
    server_resource_used += "{"

  # 실행 중인 서버
  if server_info["serverInfo"][i]["serverInstanceStatusName"] == "running":
    for j in range(len(m_list)):
      for k in range(len(ag_list)):
        # payload
        payload = {
          "timeEnd": timeEnd,
          "timeStart": timeStart,
          "prodName": "System/Server(VPC)",
          "metric": m_list[j],
          "interval": "Min1",
          "aggregation": ag_list[k],
          "cw_key": cw_key,
          "dimensions": {
            "instanceNo": server_info["serverInfo"][i]["serverInstanceNo"] 
          }
        }
     
        # call
        monitor_response = requests.post(api_server + api_url, headers=http_header, json=payload)
        monitor_data = json.loads(monitor_response.text)
        print(monitor_data)    
        # write
        monitor_tmp = eval(str(monitor_data))
     
        for n in range(len(monitor_tmp)):
          print(monitor_tmp)
          tmp = datetime.fromtimestamp(monitor_tmp[n][0]/1000)
          if str(tmp) == dt_str:
            server_resource_used += "\"" + m_list[j] + "\" : \""
            server_resource_used += str(monitor_tmp[n][1]) + "\""
            # comma
            if j < len(m_list)-1:
              server_resource_used += ", "
  # 정지 중인 서버
  else:
    server_resource_used += "\"avg_cpu_used_rto\" : \"-\", "
    server_resource_used += "\"mem_usert\" : \"-\", "
    server_resource_used += "\"avg_fs_usert\" : \"-\" "
               
  if i == int(server_info["serverCount"])-1:
    server_resource_used += "}]"
  else:
    server_resource_used += "}, "


print(server_resource_used)
#print(str(dt.strftime('%Y-%m-%d %H:%M:%S')))


