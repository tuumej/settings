#!/bin/bash

## init script
# 1. Install jq package 
# 2. Install ncloud cli
# 3. nas ( mkdir / mount )
# 4. apache/tomcat ( mkdir in nas - logs_ + serverName / start)
#

# 1. Install jq package
# sudo apt-get install -y jq

# 2. Install ncloud cli
# wget https://www.ncloud.com/api/support/download/files/cli/CLI_1.1.14_20230525.zip

# 3. nas ( mkdir / mount )
## nas acl에 서버 등록
# ~/sh/nasAcl.sh
# mkdir /mnt/nas
# mount -t nfs -o vers=3 nas주소:/nas이름 /마운트경로
# 예시> sudo mount -t nfs -o vers=3 169.254.84.52:/n2586308_imsinas01 /mnt/nas

# 4. apache/tomcat (mkdir in nas - logs_ + serverName / start)

# sudo mkdir /mnt/nas/logs/apache_$HOSTNAME
# ~/apache2/bin/apacheclt start

# sudo mkdir /mnt/nas/logs/tomcat_$HOSTNAME
# ~/tomcat9/bin/catalina.sh start
