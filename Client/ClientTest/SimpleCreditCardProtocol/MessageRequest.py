#!/bin/python3
import random
import json


class ClientRequest:
    def __init__(self):
        self.MessageID = random.randint(1000000000, 4000000000)
        self.TransactionID = 0
        self.host = 'cdg.creditcard.com'

    # def Transictaion_id_builder(self,):

    def Create_Payment_Request(self, msg_dict, uri, msg_host):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        self.MessageID += 1
        http_req = f"POST {uri} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}"

        return http_req

    def Create_Details_Request(self, msg_dict, uri, msg_host):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        self.MessageID += 1
        http_req = f"GET {uri} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}"

        return http_req

    def Create_Refund_Request(self, msg_dict, uri, msg_host):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        self.MessageID += 1
        http_req = f"POST {uri} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}"

        return http_req

    def Create_cancel_Request(self, msg_dict, uri, msg_host):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        self.MessageID += 1
        http_req = f"DELETE {uri} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}"
        return http_req


if __name__ == "__main__":
    pass
