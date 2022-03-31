#! /bin/bash
#

phone=$1
message=$2
server="http://192.168.31.222:8081/api/v1/notify/sms"

curl -H "Content-Type:application/json" -X POST "$server" --data "{\"app\": \"std\", \"tos\": [\"$phone\"], \"content\": {\"msg\":\"$message\"}}"
