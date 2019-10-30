import asyncio
import logging
import ujson

from nats.aio.client import Client as NATS

from test_saver.configuration import load_config
from test_saver.models import db
from test_saver.nats_client import NATSHandler
from test_saver.serializer import TestSerializer

log = logging.getLogger(__name__)


async def message_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = ujson.loads(msg.data.decode())
    serializer = TestSerializer(db=db, msg=data)
    try:
        serializer.save_to_db()
        log.info(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )
    except KeyError:
        log.info("msg malformed")


async def run(nats_url, nats_subject):
    nats_client = NATSHandler(
        nats_url,
        logger=log
    )
    # # Simple publisher and async subscriber via coroutine.
    await nats_client.sub(nats_subject, handler=message_handler)


# async def graceful_shutdown(nats_client):
#     await nats_client.graceful_shutdown()

if __name__ == "__main__":
    config = load_config()
    db.bind(
        provider="sqlite",
        filename="{}{}{}".format(config.db_host, config.db_user, config.db_pass),
        create_db=True,
    )
    db.generate_mapping(create_tables=True)
    log.info("db binded")
    loop = asyncio.get_event_loop()
    nats_url = f"{config.nats_host}:{config.nats_port}"
    try:
        loop.create_task(
            run(
                nats_url=nats_url,
                nats_subject=config.nats_subject,
            )
        )
        loop.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        # loop.run_until_complete(graceful_shutdown(nc))
        loop.close()

