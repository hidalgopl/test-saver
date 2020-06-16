import asyncio
from loguru import logger
import rollbar
import ujson

from test_saver import database
from test_saver.configuration import load_config
from test_saver.models import db
from test_saver.nats_client import NATSHandler
from test_saver.serializer import TestSuiteSerializer
from test_saver.db_handlers import TestORMSerializer


async def message_handler(msg):
    subject = msg.subject
    data = ujson.loads(msg.data.decode())
    serializer = TestSuiteSerializer(db=db, db_handler_class=TestORMSerializer, msg=data)
    try:
        await serializer.save_to_db()
        logger.info(
            f"Received a message on {subject}"
        )
    except KeyError as e:
        logger.info(f"msg malformed: {msg}")


async def run(loop, nats_url, nats_subject, rollbar):
    await database.connect()
    nats_client = NATSHandler(nats_url, loop=loop)
    await nats_client.connect()
    try:
        await nats_client.sub(nats_subject, message_handler)
    except Exception as e:
        logger.error(e)
        rollbar.report_exc_info()


if __name__ == "__main__":
    config = load_config()
    rollbar.init(
        config.rollbar_token,
        "production"
    )
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(
            run(loop=loop, nats_url=config.nats_host, nats_subject=config.nats_subject, rollbar=rollbar)
        )
        loop.run_forever()
    except KeyboardInterrupt:
        logger.error("keyboard interrupt")
    finally:
        loop.close()
