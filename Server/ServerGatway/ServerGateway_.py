#!/bin/python3
import logging
import os
import socket
import sys
import threading


class ServerGateway:
    def __init__(self):
        self.host = '0.0.0.0'
        self.PORT = 49166
        self.Gatewaysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Gatewaysocket.bind((self.host, self.PORT))
        self.Gatewaysocket.listen(5)

    def send_to_server(self):
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
            #self.logger.debug(f"Sending :\n{data[:-1]}")
            self.Gatewaysocket.accept()
            self.Gatewaysocket.send(str.encode('data'))

    def receive_from_server(self):
        # implemnting logger to track the message
        logging.basicConfig(filename='gateway_logs_in',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("passing client requests to others")
        self.logger = logging.getLogger('passing Requests from client')
        connection, address = self.Gatewaysocket.accept()
        while True:
            data = connection.recv(1024).decode()
            #self.logger.debug(f"Receiving: {data[:-1]}")
            #os.system(f"echo -en \"{data}\"")
            # socket should be closed by  connection.close we will check later


if __name__ == "__main__":
    gateway = ServerGateway()
    thread_recieve_from_server = threading.Thread(target=gateway.receive_from_server, args=())
    thread_send_to_server = threading.Thread(target=gateway.send_to_server, args=())
    thread_recieve_from_server.start()
    thread_send_to_server.start()
    thread_recieve_from_server.join()
    thread_send_to_server.join()
