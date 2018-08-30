#-*- coding: utf-8 -*-
import asyncio
import serial_asyncio
import click
import random
from functools import partial


com = '/dev/cu.usbmodem1411'
baudrate = 9600


class Reader(asyncio.Protocol):
    """
    """

    def __init__(self, queue):
        """Store the queue.
        """
        super().__init__()
        self.transport = None
        self.buf = None
        self.queue = queue

    def connection_made(self, transport):
        """Store the serial transport and prepare to receive data.
        """
        self.transport = transport
        self.buf = bytes()
        print('port opend', transport)

    def data_received(self, data):
        """Store characters until a newline is received.
        """
        self.buf += data
        if b'\r' in self.buf:
            lines = self.buf.split(b'\r')
            recv, self.buf = lines[-2:]  # whatever was left over
            data = recv.strip()
            asyncio.ensure_future(self.queue.put(data))
            self.buf.strip()
            print(f'producing: {id(data)}')

    def connection_lost(self, exc):
        print('Reader closed')


async def consume(queue):
    """Get serail data with async
    """
    while True:
        data = await queue.get()
        print(f'consuming: {id(data)}')
        await asyncio.sleep(random.random())
        queue.task_done()


loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)

produce = partial(Reader, queue)
producer_coro = serial_asyncio.create_serial_connection(
    loop, produce, com, baudrate
)
consumer_coro = consume(queue)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()
