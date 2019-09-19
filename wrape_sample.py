#-*- coding: utf-8 -*-
from serial import Serial
from utility.syncasync import *

import asyncio
import time
import random
import logging
import sys


#url = '/dev/cu.usbmodem14101'
url = '/dev/ttys005'
port = 9600


async def produce(queue, url, **kwargs):
    log = logging.getLogger('produce')
    log.info('running_producer')
    ser = Serial(url, baudrate=9600)
    while True:
        msg = await get(ser)
        log.info(f"produce id: {id(msg)}, device:{msg.split(',')[2:4]}, msg:{repr(msg)}")
        await queue.put(msg)
        await asyncio.sleep(random.randint(0,3))


async def consume(queue):
    """
    consume serial data from queue
    """
    log = logging.getLogger('comsume')
    log.info('running_comsume')
    while True:
        # wait for an data from producer
        data = await queue.get()
        # process the data
        log.info(f"consuming id: {id(data)}")
        # simulate i/o operation using sleep
        #await asyncio.sleep(random.randint(0,3))
        await asyncio.sleep(3)
        # Notify the queue that the item has been processed
        queue.task_done()


@sync_to_async
def get(ser):
    msg = ser.read_until(b'\r\n')
    return msg.rstrip().decode('utf-8')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)3s %(name)5s: %(message)s',
        stream=sys.stderr,
    )
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    producer_coro = produce(queue, url, baudrate=port)
    consumer_coro = consume(queue)
    loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
    loop.run_forever()
    loop.close()
