#!/bin/python3
import time
import json
import random
import threading
import logging
import MessageChecker.ProcessMessage as processMessage




logging.basicConfig(filename="/home/user/Desktop/CrossDomainGuard/CDSFiles/B_part.log", level=logging.INFO)


fifoAB = open("/home/user/Desktop/fifo/fifoAB", "r+b", buffering=0)
fifoBA = open("/home/user/Desktop/fifo/fifoBA", "r+b", buffering=0)
fifoBC = open("/home/user/Desktop/fifo/fifoBC", "r+b", buffering=0)
fifoCB = open("/home/user/Desktop/fifo/fifoCB", "r+b", buffering=0)



def create_fake(paylod,length,fake_id):
    fake_msg = f"GET /payment/details HTTP/1.1\n" \
               f"Message-ID: {fake_id}\n" \
               f"Content-Type: application/json\n " \
               f"Accept: application/json\n" \
               f"Host: cdg.creditcard.com\n" \
               f"Accept-Charset: utf-8\n" \
               f"Content-Lengeth: {length}\n" \
               f"Payload: {paylod}\n" \
               f"***\n"

    return fake_msg





class Guard:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.noise_lock = threading.Lock()
        self.noise_dict = {
            'Transaction Details':
                {
                    "Transaction_ID": "T22412345678",
                    "Payment_Reciever": "Yosef Yassin",
                },
        }
        
        self.fake_messages_id = []
        self.noise_flag = False
        

    def create_fake_message_id(self):
        fake_id = random.randint(5000000001, 5999999999)
        return fake_id

    def transfer_data(self, source):
        if source == 'C':
            transfer_fifo_from = fifoCB
            transfer_fifo_to = fifoBA
            destination = 'A'
            process_source = "Server"

        else:
            transfer_fifo_from = fifoAB
            transfer_fifo_to = fifoBC
            destination = 'C'
            process_source = "Client"

        data = ""
        nextLine = ""
        while nextLine != ('***' + "\n"):
            data += nextLine
            nextLine = transfer_fifo_from.readline().decode()
            logging.info(f"{data}\n")

        message_id = int(data.split('\n')[1].split(' ')[1])
        if 5000000000 < message_id < 6000000000:
            return
        message_proccesing = processMessage.MessageProcessing()
        result = message_proccesing.proccessMessage(data, process_source)
        if source == "C":
            if result[1] == False:
                return
        if source == "A":
            if result[1] == False:
                if result[0] == "Drop":
                    return
                transfer_fifo_to = fifoBA
                result[0] += f"{'***'}\n"
                with self.noise_lock:
                    self.noise_flag = False
                with self.thread_lock:
                    logging.info(
                        f"Client Request Packet Was Dropped:\n{result[0]}")  # result[0] is the message to be sent
                    transfer_fifo_to.write(str.encode(data))
                    transfer_fifo_to.flush()
                    return
        result[0] += f"{'***'}\n"
        if result[1]:  ## check according to process when complete
            with self.noise_lock:
                self.noise_flag = False
            with self.thread_lock:
                logging.info(
                    f"{result[0]}\n is fine sending it from {source} to {destination}")  # result[0] is the message to be sent
                transfer_fifo_to.write(str.encode(data))
                transfer_fifo_to.flush()


    def noise(self):
        time.sleep(4)
        if self.noise_flag:
            with self.thread_lock:
                msg_payload = json.dumps(self.noise_dict, indent=3)
                length = len(msg_payload)
                fake_id = self.create_fake_message_id()
                msg = create_fake(msg_payload,length,fake_id)
                fifoBC.write(str.encode(msg))
                fifoBC.flush()

    def sendfromA(self):
        while True:
            self.transfer_data(source='A')

    def sendfromC(self):
        while True:
            self.transfer_data(source='C')




        with self.noise_lock:
            self.noise_flag = True

    def sendNoise(self):
        while True:
            self.noise()


if __name__ == '__main__':
    guard = Guard()
    thread_AtoC = threading.Thread(target=guard.sendfromA, args=())
    thread_CtoA = threading.Thread(target=guard.sendfromC, args=())
    thread_noise = threading.Thread(target=guard.sendNoise, args=())
    thread_AtoC.start()
    thread_CtoA.start()
    thread_noise.start()
    thread_AtoC.join()
    thread_CtoA.join()
    thread_noise.join()
