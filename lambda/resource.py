import json, logging, uuid
from botocore.vendored import requests

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def cfn_response(url, body):
    data = json.dumps(body)
    headers = {'content-type' : '','content-length' : str(len(data))}
    requests.put(url, data=data, headers=headers)

def handler(event, context):
    data = {}
    for k, v in event['ResourceProperties'].items():
        data[k] = json.dumps(v, separators = (',', ':'), sort_keys = True)
    resouceId = event.get('PhysicalResourceId') or str(uuid.uuid4())
    ret = {
        'Status': 'SUCCESS',
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': data,
        'PhysicalResourceId': resouceId,
    }
    cfn_response(event['ResponseURL'], ret)
