import json
import logging
import uuid
import urllib.request

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def cfn_response(url, body):
    data = json.dumps(body).encode()
    headers = {
        'content-type': 'application/json',
        'content-length': str(len(data)),
    }
    req = urllib.request.Request(url, method='PUT', data=data, headers=headers)
    with urllib.request.urlopen(req) as res:
        res.read()  # skip the body


def handler(event, context):
    data = {}
    for k, v in event['ResourceProperties'].items():
        data[k] = json.dumps(v, separators=(',', ':'), sort_keys=True)
    resourceId = event.get('PhysicalResourceId') or str(uuid.uuid4())
    ret = {
        'Status': 'SUCCESS',
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': data,
        'PhysicalResourceId': resourceId,
    }
    cfn_response(event['ResponseURL'], ret)
