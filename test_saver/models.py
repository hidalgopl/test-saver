from dataclasses import dataclass

from pony import orm

db = orm.Database()


class SecTestSuite(db.Entity):
    url = orm.Required(str)
    tests = orm.Set("SecTest")


@dataclass
class TestDTO:
    code: str
    result: int
    suite_id: int


class SecTest(db.Entity):
    result = orm.Required(int)
    code = orm.Required(str)
    suite = orm.Required(SecTestSuite)
