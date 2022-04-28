#!/bin/python3
import logging
import threading
import socket
from SimpleCreditCardProtocol import MessageRequest
import time

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

dictionary_details_request = {
    'Transaction':
        {
            "Transaction_ID": "T22412345678",
            "Payment_Reciever": "Yosef Yassin",
        },
}

    dictionary_refund_request = {
        'Transaction':
            {
                "Transaction_ID": "T22412345678",
                "amount": "50",
                "Payment_Reciever": "Yosef Yassin",
            },
    }
    
dictionary_cancel_request = {
    'Transaction':
        {
            "Transaction_ID": "T22412345678",
            "Payment_Receiver": "Yosef Yassin",
        },
}

msg_uri_trans_cancel = "/payment/cancel"
msg_uri_refund = "/payment/refund"
msg_uri_trans_payment = "/payment/transaction"
msg_uri_trans_details = "/payment/details"

messeage_request = MessageRequest.ClientRequest()
Payment_request = messeage_request.Create_Payment_Request(dictionary_payment_request, msg_uri_trans_payment,
                                                          msg_host="cdg.creditcard.com")
Payment_request2 = messeage_request.Create_Payment_Request(dictionary_payment_request,
                                                           msg_uri_trans_payment,
                                                           msg_host="cdg.creditcard.com")
Details_request = messeage_request.Create_Details_Request(dictionary_details_request, msg_uri_trans_details,
                                                          msg_host="cdg.creditcard.com")
Refund_request = messeage_request.Create_Refund_Request(dictionary_refund_request, msg_uri_refund,
                                                        msg_host="cdg.creditcard.com")
Cancel_request = messeage_request.Create_cancel_Request(dictionary_cancel_request, msg_uri_trans_cancel,
                                                        msg_host="cdg.creditcard.com")


class ClientTest:
    def __init__(self):
        IP = '127.0.0.1'
        PORT = 49209
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))

    TESTS = [
        f"{Payment_request}***\n",
        f"{Details_request}***\n",
        f"{Refund_request}***\n",
        f"{Details_request}***\n",
        f"{Cancel_request}***\n",
        f"{Details_request}***\n",
    ]

    def send_to_gateway(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='logs_out',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("Running Request Testing")
        self.logger = logging.getLogger('Sending Requests')
        for test in self.TESTS:
            logging.debug(f"Sending :\n{test}")
            #print(test)
            self.sock.send(str.encode(test))
            time.sleep(5)

    def receive_from_gateway(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='logs_in',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("Running Request Testing")
        #self.logger = logging.getLogger('Recieving Requests')
        while True:
            #print("recieving")
            data = self.sock.recv(1024).decode()
            logging.debug(f"Receiving: {data[:-1]}")
            #print(data)


if __name__ == "__main__":
    test1 = ClientTest()
    thread_send_to_client=threading.Thread(target=test1.send_to_gateway(),args=())
    thread_recieve_from_client=threading.Thread(target=test1.receive_from_gateway(),args=())
    thread_recieve_from_client.start()
    thread_send_to_client.start()
    thread_recieve_from_client.join()
    thread_send_to_client.join()
