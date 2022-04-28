#!/bin/python3
import threading
import sys
import logging
import os


fifoCB = open("/home/user/Desktop/fifo/fifoCB", "r+b", buffering=0)
fifoBC = open("/home/user/Desktop/fifo/fifoBC", "r+b", buffering=0)
logging.basicConfig(filename="/home/user/Desktop/CrossDomainGuard/CDSFiles/C_part.log", level=logging.INFO)

def sendToB():
    while True:
        data = sys.stdin.readline()
        logging.info(data)
        fifoCB.write(str.encode(data))
        fifoCB.flush()



def readFromB():
    while True:
        data = fifoBC.readline().decode()
        logging.info(data)
        os.system("echo -en \"" + data + "\"")




if __name__ == "__main__":
    threadCtoB = threading.Thread(target=sendToB,args=())
    threadBtoC = threading.Thread(target=readFromB,args=())
    threadCtoB.start()
    threadBtoC.start()
    threadCtoB.join()
    threadBtoC.join()

