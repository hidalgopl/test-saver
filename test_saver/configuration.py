import logging
import os
from dataclasses import dataclass

from test_saver.exceptions import ConfigError

log = logging.getLogger("test_saver")


@dataclass
class Config:
    nats_host: str
    nats_port: str
    nats_subject: str
    db_host: str
    db_user: str
    db_pass: str


def load_config() -> Config:
    try:
        config = Config(
            nats_host=os.environ["NATS_HOST"],
            nats_port=os.environ["NATS_PORT"],
            nats_subject=os.environ["NATS_SUBJECT"],
            db_host=os.environ["DB_HOST"],
            db_user=os.environ["DB_USER"],
            db_pass=os.environ["DB_PASS"],
        )
    except KeyError:
        raise ConfigError("please all required env variables")
    log.info(f"running with: {config}")
    return config
