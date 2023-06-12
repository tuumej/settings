#!/bin/bash

# 사용중인 포트 확인

:<<"END"
# 0;30m  = black
# 0;31m  = red
# 0;32m  = green
# 0;33m  = orange
# 0;34m  = blue
# 0;35m  = purple
# 0;36m  = cyan
# 1;30m  = grey
# 1;31m  = light red
# 1;32m  = light green
# 1;33m  = yellow
# 1;35m  = gray
# 1;35m  = light bluegreen
END


while true;
time=`date`
cfnet=`sudo netstat -anlpt`
do
  echo -e "\e[1;33m$time\e[0m"
  echo -e "\e[1;32m$cfnet\e[0m"
  sleep 1;
  clear;
done
