# -*- coding:utf-8 -*-

import os
os.environ["LAMBDA_ARN"] = "arn::dummy"

from awslambda.macro import handler

def test_macro():
    ret = handler({
        "region": "us-east-1", 
        "accountId": "123456789012", 
        "fragment": {
            "Resources": {
                "JSON": {
                    "Type": "JSON::String",
                    "Properties": {
                        "Test": {
                            "Foo": "Bar",
                            "Hoge": "Fuga"
                        }
                    }
                }
            }
        }, 
        "transformId": "$TRANSFORM_ID", 
        "params": {}, 
        "requestId": "$REQUEST_ID",
        "templateParameterValues": {}
    }, {})

    assert ret == {
        "status": "success",
        "requestId": "$REQUEST_ID",
        "fragment": {
            "Resources": {
                "JSON": {
                    "Type": "Custom::JSONString",
                    "Version": "1.0",
                    "Properties": {
                        "Test": {
                            "Foo": "Bar",
                            "Hoge": "Fuga"
                        },
                        "ServiceToken": "arn::dummy"
                    }
                }
            }
        }
    }
