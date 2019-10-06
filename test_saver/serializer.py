from typing import Any, Union, Callable

from pony import orm

from test_saver.db_handlers import TestPonySerializer
from test_saver.models import TestDTO


class TestSerializer:
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
        return TestDTO(
            code=self.data["code"],
            result=self.data["result"],
            suite_id=self.data["suite_id"],
        )

    def save_to_db(self):
        dto = self.decode_data()
        serializer = self.db_handler_class(db=self.db, dto=dto)
        serializer.save()
