#!/bin/python3
import socket
import numpy as np

def spam_requests(message_to_send, connection):  ### overloading cpu to hold leba 
    while True:
        connection.send(message_to_send.encode())
        A = np.random.randint(low=1, high=2, size=(1000, 1000))
        B = np.random.randint(low=1, high=2, size=(1000, 1000))
        np.dot(A, B)


if __name__ == '__main__':
    message = "hi i am spamming haha"
    IP = '127.0.0.1'
    PORT = 49209
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    spam_requests(message, sock)
