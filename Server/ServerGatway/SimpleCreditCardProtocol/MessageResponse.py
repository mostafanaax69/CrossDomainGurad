#!/bin/python3
import json


class ServerResponse:
    def __init__(self):
        self.MessageID ="empty"

    def Create_Payment_Response_OK(self, msg_dict, msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res= f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"
        return http_res


    def Create_Payment_Response_fail(self, msg_dict, msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res= f"HTTP/1.1 403 fail\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"
        return http_res

    def Create_Details_response(self, msg_dict,msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_Details_response_fail(self, msg_dict,msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 fail\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type:application/json \n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{length}\n" \
                   f"{msg_payload}\n"

        return http_res

    def Create_Refund_response(self, msg_dict,  msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 200 OK\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_Refund_response_fail_transNotFound(self, msg_dict,  msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 fail\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type:application/json \n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{length}\n" \
                   f"{msg_payload}\n"

        return http_res


    def Create_Refund_response_fail_notAllowedAmount(self, msg_dict,msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 403 fail\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type:application/json \n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{length}\n" \
                   f"{msg_payload}\n"

        return http_res

    def Create_cancel_response(self, msg_dict, msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 204 No Content\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type: application/json\n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth: {length}\n" \
                   f"Payload: {msg_payload}\n"

        return http_res


    def Create_cancel_response_fail_transNotFound(self, msg_dict,msg_host):
        self.MessageID = "empty"
        msg_payload = json.dumps(msg_dict, indent=3)
        length = len(msg_payload)
        http_res = f"HTTP/1.1 404 fail\n" \
                   f"Message-ID: {self.MessageID}\n" \
                   f"Content-Type:application/json \n " \
                   f"Accept: application/json\n" \
                   f"Host: {msg_host}\n" \
                   f"Accept-Charset: utf-8\n" \
                   f"Content-Lengeth:{length}\n" \
                   f"{msg_payload}\n"

        return http_res


if __name__ == "__main__":
    pass
