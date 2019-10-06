import asyncio
import logging
import ujson

from nats.aio.client import Client as NATS

from test_saver.configuration import load_config
from test_saver.models import db
from test_saver.serializer import TestSerializer

log = logging.getLogger("test_saver")


async def run(loop, nats_host, nats_port, nats_subject):
    nc = NATS()
    nats_url = f"{nats_host}:{nats_port}"
    await nc.connect(nats_url, loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = ujson.loads(msg.data.decode())
        serializer = TestSerializer(db=db, msg=data)
        serializer.save_to_db()
        log.info(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe(nats_subject, cb=message_handler)


if __name__ == "__main__":
    config = load_config()
    db.bind(
        provider="sqlite",
        filename="{}{}{}".format(config.db_host, config.db_user, config.db_pass),
        create_db=True,
    )
    db.generate_mapping(create_tables=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run(
            loop,
            nats_host=config.nats_host,
            nats_port=config.nats_port,
            nats_subject=config.nats_subject,
        )
    )
    loop.close()
