from typing import Any, Union, Callable

from pony import orm

from test_saver.db_handlers import TestPonySerializer
from test_saver.models import TestDTO, TestSuiteDTO


class TestSuiteSerializer:
    def __init__(
        self,
        msg: Any,
        db: orm.Database,
        db_handler_class: Union[TestPonySerializer, Callable] = TestPonySerializer,
    ):
        self.data = msg
        self.db_handler_class = db_handler_class
        self.db = db
        # clean architecture, save us from sticking to one ORM

    def decode_data(self):
        tests_dto = [TestDTO(
            test_code=test["test_code"],
            result=test["result"],
            test_suite_id=self.data["test_suite_id"],
        ) for test in self.data["tests"]]

        return TestSuiteDTO(
            test_suite_id=self.data["test_suite_id"],
            url=self.data["url"],
            tests=tests_dto,
        )

    def save_to_db(self):
        dto = self.decode_data()
        serializer = self.db_handler_class(db=self.db, dto=dto)
        serializer.save()
