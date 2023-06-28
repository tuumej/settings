"""
-----------------------------
파일명         : server_info.py
생성일자       : 2023-06-26
생성자         : ljw
최종수정일자   : 2023-06-26
최종수정자     :
파일설명       : 서버 정보 조회(count/spec/OS/InstanceID)
------------------------------

"""

import sys
import os
import hashlib
import hmac
import base64
import requests
import json
import time
from datetime import datetime

timestamp = int(time.time() * 1000)

# api info
access_key = "8z6s0NSPFKlSohYUb0QT"
secret_key = "bJtTFuI1q0GQjX8mxnQvjYWw0YZJPaUQffrZzwYo"
secret_key = bytes(secret_key, "UTF-8")

#api_server = "https://cw.apigw.ntruss.com"
api_server = "https://ncloud.apigw.ntruss.com"
api_url = "/vserver/v2/getServerInstanceList"
api_url = api_url + "?responseFormatType=json"
api_method = "GET"

# message info
message = api_method + " " + api_url + "\n" + str(timestamp)  + "\n" + access_key
message = bytes(message, "UTF-8")

signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())


# http header
http_header = {
  "x-ncp-apigw-signature-v2" : signingKey,
  "x-ncp-apigw-timestamp" : str(timestamp),
  "x-ncp-iam-access-key" : access_key,
}

# call
server_response = requests.get(api_server + api_url, headers=http_header)
#print(type(server_response.text))
server_data = json.loads(server_response.text)

#print(data["getServerInstanceListResponse"]["totalRows"])

# server info

server_cnt = server_data["getServerInstanceListResponse"]["totalRows"]

#server_data = data["getServerInstanceListResponse"]["serverInstanceList"]
#print(server_data)

tmp = server_data["getServerInstanceListResponse"]["serverInstanceList"]
server_info_tmp = ""

for i in range(server_cnt):
  if i == 0:
    server_info_tmp += "{ \"serverCount\" : \""
    server_info_tmp += str(server_cnt)
    server_info_tmp += "\", \"serverInfo\" : "
    server_info_tmp += "[ "

  server_info_tmp += "{ \"serverInstanceNo\" : \""
  server_info_tmp += tmp[i]["serverInstanceNo"]
  server_info_tmp += "\", \"serverOperation\" : \""
  server_info_tmp += tmp[i]["platformType"]["codeName"]
  server_info_tmp += "\", \"serverName\" : \""
  server_info_tmp += tmp[i]["serverName"]
  server_info_tmp += "\", \"serverSpectCode\" : \""
  server_info_tmp += tmp[i]["serverSpecCode"]
  server_info_tmp += "\", \"serverInstanceStatusName\" : \""
  server_info_tmp += tmp[i]["serverInstanceStatusName"]
  server_info_tmp += "\" }"

  if i == server_cnt-1:
    server_info_tmp += "]}"
  else:
    server_info_tmp += ", "

"""
server_info 데이터 정보

serverInfo : 
  serverInstanceNo, 
  serverOperation, 
  serverName, 
  serverSpectCode, 
  serverInstanceStatusName

"""
server_info = json.loads(server_info_tmp)
#print(server_info)
