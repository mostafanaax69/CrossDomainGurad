#!/bin/python3
import logging
import os
import socket
import sys
import threading
import time


class ClientGateway:
    def __init__(self):
        self.host = '0.0.0.0'
        self.PORT = 49209
        self.Gatewaysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Gatewaysocket.bind((self.host, self.PORT))
        self.Gatewaysocket.listen(5)

    def send_to_client(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='gateway_logs_out',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("passing respones to client from gatway")
        self.logger = logging.getLogger('Sending responses')
        while True:
            data = sys.stdin.readline()
           # self.logger.debug(f"Sending :\n{data[:-1]}")
            self.Gatewaysocket.sendall(str.encode(data))
            time.sleep(10)

    def receive_from_client(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='gateway_logs_in',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("passing client requests to others")
        logging.getLogger('passing Requests from client')
        connection, address = self.Gatewaysocket.accept()

        while True:
            data = connection.recv(1024).decode()
            self.logger.debug(f"Receiving: {data}")
            os.system(f"echo -en \"{data}\"")
            # socket should be closed by  connection.close we will check later


if __name__ == "__main__":
    gateway = ClientGateway()
    thread_send_to_client=threading.Thread(target=gateway.send_to_client,args=())
    thread_recieve_from_client=threading.Thread(target=gateway.receive_from_client,args=())
    thread_recieve_from_client.start()
    thread_send_to_client.start()
    thread_recieve_from_client.join()
    thread_send_to_client.join()
