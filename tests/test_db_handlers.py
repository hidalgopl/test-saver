from pony import orm

from test_saver.db_handlers import TestPonySerializer
from test_saver.models import db, TestSuiteDTO, SecTest, TestDTO
import pytest


@pytest.fixture
def db_test_instance():
    db.bind(provider="sqlite", filename=":memory:", create_db=True)
    db.generate_mapping(check_tables=True, create_tables=True)
    yield db


def test_pony_orm_save(db_test_instance):
    dto = TestSuiteDTO(
        test_suite_id="1234",
        url="https://www.erurl.com",
        tests=[TestDTO(test_code="SEC0001", result="failed", test_suite_id=1234)],
        user_id="user_id",
    )
    with orm.db_session:
        t = TestPonySerializer(db_test_instance, dto)
        t.save()
        db_obj = SecTest.get(code="SEC0001")
    assert db_obj.suite.url == "https://www.erurl.com"
    assert db_obj.suite.user_id == "user_id"
    assert db_obj.suite.id == "1234"
