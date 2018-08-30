# -*- coding: utf-8 -*-
import threading
import serial
import queue

port = '/dev/cu.usbmodem1411'
baud = 9600

ser = serial.Serial(port, baud, timeout=0)


def produce(ser, queue):
    """
    """
    while True:
        buffers = ''
        while True:
            buffers += ser.readline().decode()
            if '\r' in buffers:
                last_received, buffers = buffers.split('\r')[-2:]
                data = last_received.strip()
                print(f"prodcue: {id(data)}")
                queue.put(data)


def consume(queue):
    """
    """
    while True:
        data = queue.get()
        print(f"consume: {id(data)}")
        queue.task_done()


q = queue.Queue()
workers = [
    threading.Thread(target=produce, args=(ser, q, )),
    threading.Thread(target=consume, args=(q,))
]

for w in workers:
    w.start()

q.join()
