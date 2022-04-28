#!/bin/python3
import json


class ServerResponse:
    def __init__(self):
        pass

    def Create_Payment_Response_OK(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res= f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"
        return http_res


    def Create_Payment_Response_fail(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res= f"HTTP/1.1 403 FAIL\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"
        return http_res

    def Create_Details_response(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{length}\n" \
                   f"Payload:{msg_payload}\n"

        return http_res


    def Create_Details_response_fail(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res

    def Create_Refund_response(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_Refund_response_fail(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_Refund_response_fail_notAllowedAmount(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 403 FAIL\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res

    def Create_cancel_response(self, msg_dict, msg_host,MessageID):

        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 204 NO_CONTENT\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_cancel_response_fail(self, msg_dict, msg_host,MessageID):
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 FAIL\n" \
                   f"Message-ID: {MessageID}\n" \
                   f"Content-Type: application/json\n" \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}"

        return http_res


if __name__ == "__main__":
    pass
