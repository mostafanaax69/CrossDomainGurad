#!/bin/python3
import threading
import sys
import logging
import os



fifoAB = open("/home/user/Desktop/fifo/fifoAB", "r+b", buffering=0)
fifoBA = open("/home/user/Desktop/fifo/fifoBA", "r+b", buffering=0)
logging.basicConfig(filename="/home/user/Desktop/CrossDomainGuard/CDSFiles/A_part.log", level=logging.INFO)


def sendToB():
    while True:
        data = sys.stdin.readline()
        logging.info(data)
        fifoAB.write(str.encode(data))
        fifoAB.flush()




def readFromB():
    while True:
        data = fifoBA.readline().decode()
        logging.info(data)
        os.system("echo -en \"" + data + "\"")


if __name__ == "__main__":
    threadAtoB = threading.Thread(target=sendToB, args=())
    threadBtoA = threading.Thread(target=readFromB, args=())
    threadAtoB.start()
    threadBtoA.start()
    threadAtoB.join()
    threadBtoA.join()
