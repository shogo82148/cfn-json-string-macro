import os

LAMBDA_ARN = os.environ["LAMBDA_ARN"]


def handle_template(request_id: str, template: object) -> object:
    for _, resource in template.get("Resources", {}).items():
        if resource["Type"] == "JSON::String":
            properties = resource.get("Properties", {})
            properties["ServiceToken"] = LAMBDA_ARN
            resource.update({
                "Type": "Custom::JSONString",
                "Version": "1.0",
                "Properties": properties,
            })
    return template


def handler(event, context):
    fragment: object = event["fragment"]
    status: str = "success"

    try:
        fragment = handle_template(event["requestId"], event["fragment"])
    except Exception:
        status = "failure"

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }
