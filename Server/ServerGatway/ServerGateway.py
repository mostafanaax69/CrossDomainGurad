#!/bin/python3
import logging
import socket
import random
from SimpleCreditCardProtocol import MessageResponse


def TransactionBuilder():
    start = "T224"
    randNum = random.randint(10000000, 98999999)
    Transaction_id = start + f'{randNum}'


dictionary_details_response = {
    'Transaction Details':
        {
            "country_id": "IL", "currency_id": "ILS", "amount": "100", 'info':
            {
                "issuer": "MasterCard",
                "CreditCardNumber": "5555 5555 5555 4444",
                "consumer_name": "Mostafa Naamneh",
                "ccv": "552",
                "consumer_bank": "Mercantile",
                "bank_code": "133",
                "account_number": " IL44MR133"
            },
            "Payment_Receiver": "Yosef Yassin",
            "Transaction_Date": "2022-03-27",
            "Transaction_ID": "{T22412345677}"
        },
    'success': "True",
    'message': "OK",

}

dictionary_details_response_error = {
    'Transaction Error':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "false",
    'message': "Transaction not found",

}

dictionary_payment_response = {
    'Transaction Payment':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "True",
    'message': "OK",
}

dictionary_payment_response_error = {
    'Transaction':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "false",
    'message': "not allowed amount",
}

dictionary_refund_response = {
    'Transaction Refund':
        {
            "Transaction_ID": "T22412345677",
            "amount": "50",
        },
    'success': "True",
    'message': "OK",
}

dictionary_refund_response_error_amount = {
    'Transaction':
        {
            "Transaction_ID": "T22412345677",
            "amount": "50",
        },
    'success': "false",
    'message': "not allowed amount",
}

dictionary_refund_response_error_notFound = {
    'Transaction':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "false",
    'message': "Transaction not found",
}

dictionary_cancel_response = {
    'Transaction Cancel':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "True",
    'message': "OK",
}

dictionary_cancel_response_error = {
    'Transaction':
        {
            "Transaction_ID": "T22412345677",
        },
    'success': "false",
    'message': "Transaction not found",
}
message_response = MessageResponse.ServerResponse()
Test_Payment_response = message_response.Create_Payment_Response_OK(msg_dict=dictionary_payment_response,
                                                                    msg_host="cdg.creditcard.com")
Test_Payment_response_fail = message_response.Create_Payment_Response_OK(
    msg_dict=dictionary_payment_response_error,
    msg_host="cdg.creditcard.com")
Details_response = message_response.Create_Details_response(msg_dict=dictionary_details_response,
                                                            msg_host="cdg.creditcard.com")
Details_response_fail = message_response.Create_Details_response(
    msg_dict=dictionary_details_response_error,
    msg_host="cdg.creditcard.com")
Refund_response = message_response.Create_Refund_response(msg_dict=dictionary_refund_response,
                                                          msg_host="cdg.creditcard.com")
Refund_response_fail_amount = message_response.Create_Refund_response(
    msg_dict=dictionary_refund_response_error_amount,
    msg_host="cdg.creditcard.com")
Refund_response_fail_notfound = message_response.Create_Refund_response(
    msg_dict=dictionary_refund_response_error_notFound,
    msg_host="cdg.creditcard.com")
Cancel_response = message_response.Create_cancel_response(msg_dict=dictionary_cancel_response,
                                                          msg_host="cdg.creditcard.com")
Cancel_response_fail = message_response.Create_cancel_response(msg_dict=dictionary_cancel_response_error,
                                                               msg_host="cdg.creditcard.com")


class ServerTest:
    def __init__(self):
        self.MessageID = '0'
        self.requestType = 'req'
        self.resp = ''

    def CheckRequest(self, ReqType):
        OpType = ReqType.split('/')[2]
        resp = ''
        if (OpType == 'transaction'):
            self.resp = Test_Payment_response
        if (OpType == 'details'):
            self.resp = Details_response
        if (OpType == 'refund'):
            self.resp = Refund_response
        if (OpType == 'cancel'):
            self.resp = Cancel_response

    def send_to_outside(self):
        # implementing logger to track the message
        logging.basicConfig(filename='logs_out',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("Running Request Testing")
        self.logger = logging.getLogger('Sending Requests')
        self.CheckRequest(self.requestType)
        response = self.resp.replace("empty", self.MessageID)
        self.logger.debug(f"Sending :\n{self.resp}")
        response = response + "***\n"
        os.system(f"echo -en \"{response}\"")
        print(response)

    def receive_from_outside(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='logs_in',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("Running Request Testing")
        self.logger = logging.getLogger('Recieving Requests')
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

        while True:
            nextLine = ""
            RecReqeust = ""
            print(RecReqeust)
            while nextLine != ('***' + "\n"):
                RecReqeust += nextLine
                nextLine = sys.stdin.readline()
            # RecReqeust = testmsgreq
            RecReqeust = RecReqeust[:-1]
            self.MessageID = RecReqeust.split('\n')[1].split(' ')[1]
            self.requestType = RecReqeust.split(' ')[1]
            self.logger.debug(f"Receiving: {self.requestType}")
            print(RecReqeust)
            self.send_to_outside()


if __name__ == "__main__":
    test_server = ServerTest()
    test_server.receive_from_outside()
