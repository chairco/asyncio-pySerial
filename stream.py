#-*- coding: utf-8 -*-
import asyncio
import serial_asyncio
import random


# serial setting
url = '/dev/cu.usbmodem1411'
port = 9600

async def produce(queue, **kwargs):
    """get serial data use recv() define format with non-blocking 
    """
    reader, writer = await serial_asyncio.open_serial_connection(url=url, **kwargs)
    buffers = recv(reader)
    async for buf in buffers:
        # TODO: can handle data format here
        print(f"produce id: {id(buf)}")
        await asyncio.sleep(random.random())
        await queue.put(buf)


async def recv(r):
    """
    Handle stream data with different StreamReader: 
    'read', 'readexactly', 'readuntil', or 'readline'
    """
    while True:
        msg = await r.readuntil(b'\r')
        yield msg.rstrip().decode('utf-8')


async def consume(queue):
    """
    consume serial data from queue
    """
    while True:
        # wait for an data from producer
        data = await queue.get()
        # process the data
        print(f"consuming id: {id(data)}")
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())
        # Notify the queue that the item has been processed
        queue.task_done()


loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
producer_coro = produce(queue, baudrate=port)
consumer_coro = consume(queue)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()
