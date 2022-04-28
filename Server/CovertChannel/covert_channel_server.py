#!/bin/python3
import numpy as np
import time

covertMsg = "0000000111111100000001111111111111100000000000000" # actual message 0101100

def multiply_process():
    A = np.random.randint(low=1, high=2, size=(700,700))
    B = np.random.randint(low=1, high=2, size=(700, 700))
    np.dot(A, B)


def send():
    multiply_process()
    time.sleep(1.3)
    for char in covertMsg:
        if char == '1':
            multiply_process()
        else:
            time.sleep(1.3) # calcuated before 


if __name__ == '__main__':
    send()



