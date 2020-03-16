import logging
import os
from dataclasses import dataclass

from test_saver.exceptions import ConfigError

log = logging.getLogger(__name__)


@dataclass
class Config:
    nats_host: str
    nats_port: str
    nats_subject: str
    nats_user: str
    nats_pass: str
    db_host: str
    db_user: str
    db_pass: str
    db_name: str
    rollbar_token: str


def load_config() -> Config:
    try:
        config = Config(
            nats_host=os.environ["NATS_HOST"],
            nats_port=os.environ["NATS_PORT"],
            nats_subject=os.environ["NATS_SUBJECT"],
            nats_user=os.environ["NATS_USER"],
            nats_pass=os.environ["NATS_PASS"],
            db_host=os.environ["DB_HOST"],
            db_user=os.environ["DB_USER"],
            db_pass=os.environ["DB_PASS"],
            rollbar_token=os.environ["ROLLBAR_TOKEN"]
        )
    except KeyError:
        raise ConfigError("please set all required env variables")
    print(f"running with: {config}")
    return config
