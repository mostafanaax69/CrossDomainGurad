#!/bin/python3

import CrossDomainGuard.MessageChecker.dataStructures as ds
import random

msg_uri_trans_cancel = "/payment/cancel"
msg_uri_refund = "/payment/refund"
msg_uri_trans_payment = "/payment/transaction"
msg_uri_trans_details = "/payment/details"


class RequestRebuilder():

    def __init__(self):
        self.MessageID = random.randint(6000000001, 9900000000)
        self.host = "cdg.creditcard.com"

    def Create_Payment_Request(self, payload, payloadlen, msgID):
        self.MessageID += 1
        ds.MessageIDFromClient[msgID] = f"{self.MessageID}"
        http_req = f"POST {msg_uri_trans_payment} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {self.host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_req

    def Create_Details_Request(self, payload, payloadlen, msgID):
        self.MessageID += 1
        ds.MessageIDFromClient[msgID] = f"{self.MessageID}"
        http_req = f"GET {msg_uri_trans_details} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {self.host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_req

    def Create_Refund_Request(self, payload, payloadlen, msgID):
        self.MessageID += 1
        ds.MessageIDFromClient[msgID] = f"{self.MessageID}"
        print(ds.MessageIDFromClient)
        http_req = f"POST {msg_uri_refund} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {self.host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_req

    def Create_cancel_Request(self, payload, payloadlen, msgID):
        self.MessageID += 1
        ds.MessageIDFromClient[msgID] = f"{self.MessageID}"
        http_req = f"DELETE {msg_uri_trans_cancel} HTTP/1.1\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {self.host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"
        return http_req


if __name__ == "__main__":
    pass
