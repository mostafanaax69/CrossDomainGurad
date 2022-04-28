#!/bin/python3

import json
import CrossDomainGuard.MessageChecker.dataStructures as ds
import CrossDomainGuard.MessageChecker.ProcessMessagePayload as ProcessMessagePayload
import CrossDomainGuard.MessageChecker.RequestMessageRebuilder as RequestMessageRebuilder
import CrossDomainGuard.MessageChecker.ResponseMessageRebuilder as ResponseMessageRebuilder

http_types_request = ["POST", "GET", "DELETE"]
OP_types_request = ["transaction", "refund", "details", "cancel"]
http_types_responses = ["NO_CONTENT", "OK", "FAIL", "NO_SUCH_REQUEST", "NO_SUCH_OPERATION", "NO_SUCH_HTTPVER",
                        "Missing_FIELDS"]
HTTP_HEADERS_FIELDS = ["Message-ID", "Content-Type", "Accept", "Host", "Accept-Charset", "Content-Lengeth", "Payload"]
http_types_responses_status = ["200", "500", "400", "403","404"]
error_messages = ["REQUEST_NOT_SUPPORTED,OPERATION_NOT_SUPPORTED"]
http_ver = 'HTTP/1.1'
msg_host = 'cdg.creditcard.com'
issuer_dict = [
    "Mastercard",
    "Visa Card",
    "Visa Master Card"]


def CREATE_ERROR_IN_HEADERS(MessageID):
    http_res = f"HTTP/1.1 500 WRONG_HEADERS\n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json\n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


def CREATE_ERROR_IN_FIRST_LINE(MessageID):
    http_res = f"HTTP/1.1 500 FIRST_LINE_ERROR\n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json\n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


def CREATE_ERROR_IN_VALUES(MessageID):
    http_res = f"HTTP/1.1 500 WRONG_HEADERS_VALUES\n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json \n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


def CREATE_ERROR_IN_MESSAGE_ID(MessageID):
    http_res = f"HTTP/1.1 500 WRONG_MESSAGE_ID\n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json \n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


def Create_NOT_FOUND_HTTP(self, MessageID):
    http_res = f"HTTP/1.1 500 NO_SUCH_HTTPVER \n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json \n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


def Create_NOT_Missing_HTTP_Fields(self, MessageID):
    http_res = f"HTTP/1.1 500 Missing_FIELDS \n" \
               f"Message-ID: {MessageID}\n" \
               f"Content-Type:application/json \n " \
               f"Accept: application/json\n" \
               f"Host: {msg_host}\n" \
               f"Accept-Charset: utf-8\n"

    return http_res


################### outter functions for checking stuff such as bank and acc num ###########
def are_eq(a, b):
    return set(a).__eq__(set(b)) and len(a) == len(b)


def checkBank(bank, bankcode):
    if bank not in ds.supportedBanks.keys(): return False
    if not bankcode == ds.bankCode[bank]: return False


def checkAccountNumber(accountnum, bank, creditcardnum, country):
    if not len(accountnum) == 9: return False
    creditcardlast2digits = creditcardnum[-2:]
    legitAccNum = country + creditcardlast2digits + ds.supportedBanks[bank] + ds.bankCode[bank]
    if not legitAccNum == accountnum: return False


######################################## Message Processing checking if the message stands the requirments

class MessageProcessing:
    def __init__(self):
        self.headers = []
        self.headers_alone = []
        self.request_line = []
        self.Message_ID = ''
        self.payLoadLength = 0
        self.payloadDic = {}

    ############# Parsing the payload

    def parsePayload(self, dic):
        payLoad = dic['Payload']
        self.payLoadLength = len(payLoad)
        self.payloadDic = json.loads(payLoad)

    #####################PROCESSING THE MESSAGE

    def proccessMessage(self, msg, src):
        ######## SPLITTING THE MESSAGE

        lines = msg.split("\n", 7)

        if len(lines) != 8:
            resp = CREATE_ERROR_IN_HEADERS('ERROR')
            return resp, False
        request_header = lines[0]
        lines = lines[1:]
        dic = dict(map(lambda x: x.split(': ', 1), lines))

        self.Message_ID = dic['Message-ID']

        ####Checking the first line
        if not self.checkFirstLine(request_header, src):
            if src == 'Client':
                resp = CREATE_ERROR_IN_FIRST_LINE(self.Message_ID)
                return resp, False
            return 'Drop', False

        ############# CHECKING HTTP HEADERS
        if not self.checkMessageFields(dic):
            if src == 'Client':
                resp = CREATE_ERROR_IN_HEADERS(self.Message_ID)
                return resp, False
            return 'Drop', False

        self.parsePayload(dic)

        ############ CHECKING HTTP VALUES
        if not self.validateHttpVals(dic):
            if src == 'Client':
                resp = CREATE_ERROR_IN_VALUES(self.Message_ID)
                return resp, False
            return 'Drop', False

        ############# CHECKING MESSAGE ID REQUIRMENTS
        if not self.checkMessageID(self.Message_ID):
            if src == 'Client':
                resp = CREATE_ERROR_IN_MESSAGE_ID(self.Message_ID)
                return resp, False
            return 'Drop', False

        ############ PROCESSING THE PAYLOAD BODY
        lineWords = request_header.split(' ')
        if src == 'Client':
            uriSplitted = lineWords[1].split('/')
            payLoad = ProcessMessagePayload.PayloadProcessing()
            payLoadRes = payLoad.processPayload(self.payloadDic, uriSplitted[2], src,
                                                self.Message_ID)
        else:
            uriSplitted = ''
            payLoad = ProcessMessagePayload.PayloadProcessing()
            payLoadRes = payLoad.processPayload(self.payloadDic, uriSplitted, src,
                                            self.Message_ID)
        if payLoadRes[1] == False:
            if src == 'Client':
                return payLoadRes[0], False
            return 'Drop', False

        ############# REBUILDING THE MESSAGE REQUEST TO MAKE SURE THERE IS NOT PLAYING WITH THE FIELDS PLACES
        if src == 'Client':
            client_re = RequestMessageRebuilder.RequestRebuilder()
            if uriSplitted[2] == 'transaction':
                return client_re.Create_Payment_Request(dic['Payload'], self.payLoadLength, self.Message_ID), True
            if uriSplitted[2] == 'details':
                return client_re.Create_Details_Request(dic['Payload'], self.payLoadLength, self.Message_ID), True
            if uriSplitted[2] == 'refund':
                return client_re.Create_Refund_Request(dic['Payload'], self.payLoadLength, self.Message_ID), True
            if uriSplitted[2] == 'cancel':
                return client_re.Create_cancel_Request(dic['Payload'], self.payLoadLength, self.Message_ID), True

        if src == 'Server':
            server_response_builder = ResponseMessageRebuilder.ResponseBuilder()
            OperationType = list(self.payloadDic.keys())[0].split(" ")
            if OperationType[1] == 'Details':
                return server_response_builder.Create_Details_response(dic['Payload'], self.payLoadLength,
                                                                       self.Message_ID), True

            if OperationType[1] == 'Payment':
                return server_response_builder.Create_Payment_Response_OK(dic['Payload'], self.payLoadLength,
                                                                          self.Message_ID), True
            if OperationType[1] == 'Refund':
                return server_response_builder.Create_Refund_response(dic['Payload'], self.payLoadLength,
                                                                      self.Message_ID), True
            if OperationType[1] == 'Cancel':
                return server_response_builder.Create_cancel_response(dic['Payload'], self.payLoadLength,
                                                                      self.Message_ID), True

    #################### MESSAGE ID CHECKERS
    def checkMessageID(self, MessageID):
        if not len(MessageID) == 10: return False
        return True

    ########## checking the headers vals
    def validateHttpVals(self, dic):
        if not dic['Content-Type'] == 'application/json': return False
        if not dic['Accept'] == 'application/json': return False
        if not dic['Host'] == 'cdg.creditcard.com': return False
        if not dic['Accept-Charset'] == 'utf-8': return False
        if not dic['Content-Lengeth'] == str(self.payLoadLength): return False

        return True

    def checkMessageFields(self, dic):
        # checking if HTTP request have all the required fields

        return are_eq(HTTP_HEADERS_FIELDS, (dic.keys()))

    def checkFirstLine(self, line, src):
        # check if message is request and operation is supported
        if (src == 'Client'):
            lineWords = line.split(' ')
            if not len(lineWords) == 3: return False
            if lineWords[0] not in http_types_request: return False
            uri_split = lineWords[1].split('/')
            if not len(uri_split) == 3: return False
            if uri_split[2] not in OP_types_request: return False
            if (lineWords[2] != http_ver): return False

            return True

        if (src == 'Server'):
            lineWords = line.split(' ')
            if not len(lineWords) == 3: return False
            if lineWords[2] not in http_types_responses: return False
            if lineWords[1] not in http_types_responses_status: return False
            if (lineWords[0] != http_ver): return False
            return True


if __name__ == "__main__":
    dictionary_payment_request = {
        'Transaction':
            {
                "country_id": "IL", "currency_id": "ILS", "amount": "100", 'info':
                {
                    "issuer": "MasterCard",
                    "CreditCardNumber": "5555 5555 5555 4444",
                    "consumer_name": "Mostafa Naamneh",
                    "ccv": "552",
                    "consumer_bank": "Mercantile",
                    "bank_code": "133",
                    "account_number": "IL44MR133"
                },
                "Payment_Reciever": "Yosef Yassin",
                "Transaction_Date": "2022-03-27"
            },
    }

    dictionary_payment_response = {
        'Transaction Payment':
            {
                "Transaction_ID": "T22412345678",
            },
        'success': "True",
        'message': "OK",
    }
    dictionary_refund_request = {
        'Transaction':
            {
                "Transaction_ID": "T22412345678",
                "amount": "50",
                "Payment_Reciever": "Yosef Yassin",
            },
    }
    dictionary_cancel_response = {
        'Transaction Cancel':
            {
                "Transaction_ID": "T22412345678",
            },
        'success': "True",
        'message': "OK",
    }

    payload_cancel_response=json.dumps(dictionary_cancel_response,indent=3)
    length_cancel_payload= len(payload_cancel_response)

    payload_refund = json.dumps(dictionary_refund_request,indent=3)
    length_refund = len(payload_refund)
    payload = json.dumps(dictionary_payment_request, indent=3)
    length = len(payload)
    testmsgreq = "POST /payment/transaction HTTP/1.1\n" \
                 "Message-ID: 1111111111\n" \
                 "Content-Type: application/json\n" \
                 "Accept: application/json\n" \
                 "Host: cdg.creditcard.com\n" \
                 "Accept-Charset: utf-8\n" \
                 f"Content-Lengeth: {length}\n" \
                 f"Payload: {payload}"

    testmsgreq2 = "POST /payment/refund HTTP/1.1\n" \
                 "Message-ID: 1111111111\n" \
                 "Content-Type: application/json\n" \
                 "Accept: application/json\n" \
                 "Host: cdg.creditcard.com\n" \
                 "Accept-Charset: utf-8\n" \
                 f"Content-Lengeth: {length_refund}\n" \
                 f"Payload: {payload_refund}"

    respPayload = json.dumps(dictionary_payment_response, indent=3)
    length_resp_payload = len(respPayload)

    testmsgResp = "HTTP/1.1 200 OK\n" \
                  "Message-ID: 8075127482\n" \
                  "Content-Type: application/json\n" \
                  "Accept: application/json\n" \
                  "Host: cdg.creditcard.com\n" \
                  "Accept-Charset: utf-8\n" \
                  f"Content-Lengeth: {length_resp_payload}\n" \
                  f"Payload: {respPayload}"
    testmsgResp2 = "HTTP/1.1 404 FAIL\n" \
                  "Message-ID: 8075127482\n" \
                  "Content-Type: application/json\n" \
                  "Accept: application/json\n" \
                  "Host: cdg.creditcard.com\n" \
                  "Accept-Charset: utf-8\n" \
                  f"Content-Lengeth: {length_cancel_payload}\n" \
                  f"Payload: {payload_cancel_response}"

    pr = MessageProcessing()
    res = pr.proccessMessage(testmsgreq2, 'Client')
    print(res[0])
    print(res[1])
