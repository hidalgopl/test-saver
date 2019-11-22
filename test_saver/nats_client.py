import logging
from typing import Callable

from nats.aio.client import Client


class NATSHandler:
    def __init__(self, nats_url: str, logger: logging.Logger, loop):
        self.nats_client = Client()
        self.nats_url = nats_url
        self.log = logger
        self.loop = loop

    async def connect(self):
        await self.nats_client.connect(
            self.nats_url,
            loop=self.loop,
            error_cb=self.error_callback
        )

    async def error_callback(self, msg):
        self.log.exception(msg)

    async def sub(self, subject: str, handler):
        await self.nats_client.subscribe(
            subject,
            cb=handler
        )

    async def pub(self, subject: str, msg: str):
        await self.nats_client.publish(
            subject=subject,
            payload=msg
        )

    async def graceful_shutdown(self):
        await self.nats_client.drain()
        await self.nats_client.close()
