#!/bin/bash
# NAS ACL LIST 추가하는 스크립트

myVpcNo='39407'
#myIp='10.0.3.8'
myIp=`hostname -I`
serverList=`~/sh/cli_linux/ncloud vserver getServerInstanceList --regionCode KR --vpcNo $myVpcNo --ip $myIp`
serverInstanceNo=`echo $serverList | jq '.getServerInstanceListResponse.serverInstanceList[0].serverInstanceNo'`

# ADD NAS acl list
~/sh/cli_linux/ncloud vnas addNasVolumeAccessControl --regionCode KR --nasVolumeInstanceNo 17605045 --accessControlRuleList "serverInstanceNo=$serverInstanceNo, writeAccess=true"
