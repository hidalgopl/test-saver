from dataclasses import dataclass
from datetime import datetime
from secrets import token_urlsafe

from test_saver import database
import orm
import sqlalchemy

from pony import orm as pony_orm

db = pony_orm.Database()


def rand_s():
    return token_urlsafe(16)


class SecTestSuite(db.Entity):
    id = pony_orm.PrimaryKey(str, default=rand_s)
    url = pony_orm.Required(str)
    tests = pony_orm.Set("SecTest")
    created = pony_orm.Required(datetime, default=datetime.utcnow)
    modified = pony_orm.Required(datetime, default=datetime.utcnow)
    user_id = pony_orm.Required(str)


@dataclass
class TestDTO:
    test_code: str
    result: str
    test_suite_id: int


@dataclass
class TestSuiteDTO:
    test_suite_id: str
    url: str
    tests: list
    user_id: str


class SecTest(db.Entity):
    result = pony_orm.Required(int)
    code = pony_orm.Required(str)
    suite = pony_orm.Optional(SecTestSuite)
    created = pony_orm.Required(datetime, default=datetime.utcnow)
    modified = pony_orm.Required(datetime, default=datetime.utcnow)


metadata = sqlalchemy.MetaData()


class SecTestSuiteA(orm.Model):
    __metadata__ = metadata
    __tablename__ = "sectestsuite"
    __database__ = database
    id = orm.String(primary_key=True, max_length=256)
    url = orm.String(max_length=256)
    created = orm.DateTime()
    modified = orm.DateTime()
    user_id = orm.String(max_length=256)


class SecTestA(orm.Model):
    __metadata__ = metadata
    __tablename__ = "sectest"
    __database__ = database
    id = orm.Integer(primary_key=True)
    result = orm.Integer()
    code = orm.String(max_length=25)
    suite = orm.ForeignKey(SecTestSuiteA)
    created = orm.DateTime()
    modified = orm.DateTime()
