# -*- coding:utf-8 -*-

import os
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from awslambda.resource import handler

class RequestHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        if self.headers['content-type'] != 'application/json':
            self.send_response(400)
            self.end_headers()

        content_length = int(self.headers['content-length'])
        content = self.rfile.read(content_length)
        self.server.add_content(content)

        data = b'succeed'
        self.send_response(200)
        self.send_header('content-type', 'text/plain; charset=utf-8')
        self.send_header('content-length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

class MyServer(HTTPServer):
    def __init__(self):
        super().__init__(('127.0.0.1', 0), RequestHandler)
        self._runner = None
        self._lock = threading.Lock()
        self._contents = []

    def start(self):
        self._runner = threading.Thread(target=self.serve_forever)
        self._runner.start()

    @property
    def url(self):
        address = self.server_address
        return "http://{0}:{1}".format(*address)

    def close(self):
        self.shutdown()
        self._runner.join()

    def add_content(self, content):
        with self._lock:
            self._contents.append(content)

    @property
    def contents(self):
        result = None
        with self._lock:
            result = self._contents.copy()
        return result

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

def test_resource():
    with MyServer() as ts:
        handler({
            "RequestType": "Create",
            "ResponseURL": ts.url,
            "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
            "RequestId": "unique id for this create request",
            "ResourceType": "Custom::JSONString",
            "LogicalResourceId": "MyTestResource",
            "ResourceProperties" : {
                "Test": {
                    "Foo": "Bar",
                    "Hoge": "Fuga"
                },
            },
        }, {})

        contents = ts.contents
        assert len(contents) == 1

        data = json.loads(contents[0])
        data["PhysicalResourceId"] = ""
        assert data == {
            "Data": {
                "Test": '{"Foo":"Bar","Hoge":"Fuga"}',
            },
            "LogicalResourceId": "MyTestResource",
            "PhysicalResourceId": "",
            "RequestId": "unique id for this create request",
            "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
            "Status": "SUCCESS",
        }
