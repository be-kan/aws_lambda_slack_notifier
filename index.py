import boto3
import os
import json
from base64 import b64decode
from urlparse import parse_qs
import logging

# kmsを利用して、検証用Tokenを用意
kms = boto3.client('kms')
expected_token = kms.decrypt(CiphertextBlob=b64decode(os.environ['ENCRYPTED_EXPECTED_TOKEN']))['Plaintext']

# ログを記録
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    req_body = event['body']
    params = parse_qs(req_body)
    token = params['token'][0]

    # Tokenを検証
    if token != expected_token:
        logger.error("Request token (%s) does not match exptected", token)
        raise Exception("Invalid request token")

    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=auto_scaling_group_names)

    # Auto Scaling Groupの名前やサイズを取得
    AsgName = response.get('AutoScalingGroups')[0]['AutoScalingGroupName']
    MinSize = response.get('AutoScalingGroups')[0]['MinSize']
    MaxSize = response.get('AutoScalingGroups')[0]['MaxSize']
    DesiredCapacity = response.get('AutoScalingGroups')[0]['DesiredCapacity']
    InstanceCount = len(response.get('AutoScalingGroups')[0]['Instances'])
    InstanceIdList = []
    for i in range(InstanceCount):
        InstanceIdList.append(response.get('AutoScalingGroups')[0]['Instances'][i]['InstanceId'])

    text = "AsgName:%s  MinSize:%s  MaxSize:%s  DesiredCapacity:%s  InstanceCount:%s  InstanceIdList:%s"% (AsgName, MinSize, MaxSize, DesiredCapacity, InstanceCount, InstanceIdList)

    # in_channelを指定することで、チャネル全員が見れるようにする
    response = {
        "response_type": "in_channel",
        "text": text,
    }

    return response
