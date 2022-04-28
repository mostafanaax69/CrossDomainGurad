#!/usr/bin/python3

import sys
import os
import threading
import logging

fifoAB = open("/home/user/Desktop/fifo/fifoAB", "r+b", buffering=0)
fifoBA = open("/home/user/Desktop/fifo/fifoBA", "r+b", buffering=0)
logging.basicConfig(filename="/home/user/Desktop/CrossDomainGuard/CDSFiles/A_part.log", level=logging.INFO)


def sendToB():
    while True:
        data = sys.stdin.readline()
        logging.debug("sending to B:")
        logging.info(data)
        fifoAB.write(str.encode(data))
        fifoAB.flush()


def readFromB():
    while True:
        data = fifoBA.readline().decode()
        logging.debug("reading from B:")
        logging.info(data)
        os.system("echo -en \"" + data + "\"")


if __name__ == "__main__":
    #in this file we took some help from the internet and other recourses on how to use fifos and how to read and write from and to outside the virutal machine
    #in qubes os , same logic in C 
    threadAtoB = threading.Thread(target=sendToB, args=())
    threadBtoA = threading.Thread(target=readFromB, args=())
    threadAtoB.start()
    threadBtoA.start()
    threadAtoB.join()
    threadBtoA.join()
