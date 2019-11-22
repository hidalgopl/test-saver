from dataclasses import dataclass
from datetime import datetime
from secrets import token_urlsafe
from uuid import UUID, uuid4

from pony import orm

db = orm.Database()


def rand_s():
    return token_urlsafe(16)


class SecTestSuite(db.Entity):
    id = orm.PrimaryKey(str, default=rand_s)
    url = orm.Required(str)
    tests = orm.Set("SecTest")


@dataclass
class TestDTO:
    test_code: str
    result: str
    test_suite_id: int


@dataclass
class TestSuiteDTO:
    test_suite_id : str
    url: str
    tests: list


class SecTest(db.Entity):
    result = orm.Required(int)
    code = orm.Required(str)
    suite = orm.Optional(SecTestSuite)
    created = orm.Required(datetime, default=datetime.utcnow)
    modified = orm.Required(datetime, default=datetime.utcnow)
