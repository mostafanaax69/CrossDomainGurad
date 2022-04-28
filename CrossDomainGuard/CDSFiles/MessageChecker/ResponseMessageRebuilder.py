#!/bin/python3

import CrossDomainGuard.MessageChecker.dataStructures as ds

msg_host = 'cdg.creditcard.com'


class ResponseBuilder:

    def Create_Payment_Response_OK(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = "HTTP/1.1 200 OK\n" \
                   f"Message-ID: {msgID}\n" \
                   "Content-Type: application/json\n" \
                   "Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   "Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"
        return http_res

    def Create_Payment_Response_fail(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 403 FAIL\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"
        return http_res

    def Create_Details_response(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{payloadlen}\n" \
                   f"Payload:{payload}\n"

        return http_res

    def Create_Details_response_fail(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res

    def Create_Refund_response(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res

    def Create_Refund_response_fail(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res

    def Create_Refund_response_fail_notAllowedAmount(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 403 FAIL\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res

    def Create_cancel_response(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 204 NO_CONTENT\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res

    def Create_cancel_response_fail(self, payload, payloadlen, MessageID):
        msgID = ds.MessageIDFromClient[MessageID]
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {msgID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {payloadlen}\n" \
                   f"Payload: {payload}\n"

        return http_res


if __name__ == "__main__":
    pass
