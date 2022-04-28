#!/bin/python3
import time
import numpy as np

AVERAGE = 1.2264744901657105 #i choose this number after doing a lot of tries
MSG_LEN = 49 # 49 bit message every 7 bits is 1 letter origannly , in order to correct errors ( i take the message and test it out side did not have the time to write a code that takes the 7 bits and calcuate the majority
    # tried to send 0101100


def multiply_process():
        #here i am calcuating how much time does multi op takes time
        #with that i can know to the time it takes to do a multi operation
        #and after that to take the average of the time
        A = np.random.randint(low=1, high=2, size=(700,700))
        B = np.random.randint(low=1, high=2, size=(700, 700))
        np.dot(A, B)


def calculate_avg_time():
    #calucating the time average
    sum_elapsed = 0
    for i in range(100):
        start = time.time()
        multiply_process()
        end = time.time()
        print(f"time passed  : {end - start} ")
        sum_elapsed += end - start
    return sum_elapsed / 100


def get_message():
    msg_flag = False
    while True:
        start = time.time()
        multiply_process()
        end = time.time()
        diff = end - start
        print(diff)
        #1.1 was chooses because it has the best accuracy , tried some other numbers as well
        if diff > AVERAGE * 1.1:
            start = time.time()
            multiply_process()
            end = time.time()
            if end - start <= AVERAGE * 1.1:
                msg_flag = True

        if msg_flag:
            break

    i = 0
    message_binary = ""
    print("Getting Message")
    while i < MSG_LEN:
        start = time.time()
        multiply_process()
        end = time.time()
        print(f" time passed : {end - start}")
        if end - start > AVERAGE * 1.1:
            message_binary += '1'
        else:
            message_binary += '0'
        i += 1

    print(f"binary message : {message_binary}")


if __name__ == '__main__':
    AVERAGE = calculate_avg_time()
    print(f"Average to execute is : {AVERAGE}")
    get_message()
