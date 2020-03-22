import asyncio
import time

from pony import orm
from datetime import datetime

from test_saver import database
from test_saver.models import TestSuiteDTO, SecTestSuite, SecTest, SecTestA, SecTestSuiteA


class TestPonySerializer:
    def __init__(self, db: orm.Database, dto: TestSuiteDTO):
        self.db = db
        self.dto = dto

    @orm.db_session
    def save(self):
        # TODO  - get rid of this map
        suite = SecTestSuite(
            url=self.dto.url,
            id=self.dto.test_suite_id,
            created=datetime.utcnow(),
            modified=datetime.utcnow(),
            user_id=self.dto.user_id
        )
        r_map = {"passed": 0, "failed": 1, "error": 2}
        tests = [
            SecTest(
                result=r_map[test.result],
                code=test.test_code,
                suite=suite,
                created=datetime.utcnow(),
                modified=datetime.utcnow(),
            )
            for test in self.dto.tests
        ]

        orm.commit()


class TestORMSerializer:
    def __init__(self, dto: TestSuiteDTO):
        self.dto = dto

    # @database.transaction()
    async def save(self):
        r_map = {"passed": 0, "failed": 1, "error": 2}
        async with database.transaction():
            suite = await SecTestSuiteA.objects.create(
                url=self.dto.url,
                id=self.dto.test_suite_id,
                created=datetime.utcnow(),
                modified=datetime.utcnow(),
                user_id=self.dto.user_id
            )
        print(suite.id)
        # TODO
        async with database.transaction():
            suite = await SecTestSuiteA.objects.get(id=self.dto.test_suite_id)
            SecTestA.objects.
            for test in self.dto.tests:
                await SecTestA.objects.create(
                    created=datetime.utcnow(),
                    modified=datetime.utcnow(),
                    code=test.test_code,
                    result=r_map[test.result],
                    suite=suite
                )
