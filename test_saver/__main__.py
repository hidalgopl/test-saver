import asyncio
import logging
import rollbar
import ujson

from test_saver.configuration import load_config
from test_saver.models import db
from test_saver.nats_client import NATSHandler
from test_saver.serializer import TestSuiteSerializer

log = logging.getLogger(__name__)


async def message_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = ujson.loads(msg.data.decode())
    serializer = TestSuiteSerializer(db=db, msg=data)
    try:
        print("saving to db")
        serializer.save_to_db()
        log.info(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )
        print("saved")
    except KeyError as e:
        print("msg malformed")
        print(e)
        log.info("msg malformed")


async def run(loop, nats_url, nats_subject, rollbar):
    nats_client = NATSHandler(nats_url, logger=log, loop=loop)
    await nats_client.connect()
    try:
        await nats_client.sub(nats_subject, message_handler)
    except Exception as e:
        log.error(e)
        rollbar.report_exc_info()


# async def graceful_shutdown(nats_client):
#     await nats_client.graceful_shutdown()

if __name__ == "__main__":
    config = load_config()
    db.bind(
        provider="postgres",
        user=config.db_user,
        password=config.db_pass,
        host=config.db_host,
    )
    rollbar.init(
        config.rollbar_token,
        "production"
    )
    db.generate_mapping()
    log.info("db binded")
    loop = asyncio.get_event_loop()
    nats_url = (
        f"{config.nats_user}:{config.nats_pass}@{config.nats_host}:{config.nats_port}"
    )
    print(f"using url: {nats_url}")
    try:
        loop.create_task(
            run(loop=loop, nats_url=nats_url, nats_subject=config.nats_subject, rollbar=rollbar)
        )
        loop.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        # loop.run_until_complete(graceful_shutdown(nc))
        loop.close()
