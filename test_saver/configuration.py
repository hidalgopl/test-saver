from loguru import logger
import os
from dataclasses import dataclass

from test_saver.exceptions import ConfigError


@dataclass
class Config:
    nats_host: str
    nats_subject: str
    db_host: str
    db_user: str
    db_pass: str
    rollbar_token: str


def load_config() -> Config:
    try:
        config = Config(
            nats_host=os.environ["NATS_HOST"],
            nats_subject=os.environ["NATS_SUBJECT"],
            db_host=os.environ["DB_HOST"],
            db_user=os.environ["DB_USER"],
            db_pass=os.environ["DB_PASS"],
            rollbar_token=os.environ["ROLLBAR_TOKEN"]
        )
    except KeyError:
        raise ConfigError("please set all required env variables")
    logger.info(f"running with: {config}")
    return config
