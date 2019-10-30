import logging

from nats.aio.client import Client


class NATSHandler:
    def __init__(self, nats_url: str, logger: logging.Logger):
        self.nats_client = Client()
        self.nats_url = nats_url
        self.log = logger
        self.connect()

    @classmethod
    async def connect(cls):
        await cls.nats_client.connect(
            cls.nats_client,
            error_cb=cls.error_callback
        )

    async def error_callback(self, msg):
        self.log.exception(msg)

    async def sub(self, subject: str, handler: function):
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


    async
