from pony import orm

from test_saver.exceptions import TestSuiteNotExist
from test_saver.models import TestDTO, SecTestSuite, SecTest


class TestPonySerializer:
    def __init__(self, db: orm.Database, dto: TestDTO):
        self.db = db
        self.dto = dto

    @orm.db_session
    def save(self):
        try:
            sec_test_suite = SecTestSuite[self.dto.suite_id]
        except orm.core.ObjectNotFound:
            raise TestSuiteNotExist(
                f"sec_test_suite with given id: {self.dto.suite_id} does not exist"
            )
        SecTest(result=self.dto.result, code=self.dto.code, suite=sec_test_suite)
        orm.commit()
