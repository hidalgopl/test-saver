import pytest
from pony import orm

from test_saver.models import TestSuiteDTO as DTO
from test_saver.serializer import TestSuiteSerializer as Serializer


@pytest.fixture(autouse=True)
def db():
    yield orm.Database()


def test_decode_data():
    data = {
        "test_suite_id": "fake-test-suite-id",
        "url": "https://www.testwebsite.com",
        "tests": [
            {
                "test_suite_id": "fake-test-suite-id",
                "result": "failed",
                "test_code": "SEC0001",
                "timestamp": "fake-timestamp",
            }
        ],
        "timestamp": "fake-timestamp",
        "user_id": "234",
    }
    s = Serializer(msg=data, db=db)
    decoded = s.decode_data()
    assert isinstance(decoded, DTO)


def test_decode_missing_data():
    data = {"code": "SEC001", "suite_id": 1}
    s = Serializer(msg=data, db=db)
    with pytest.raises(KeyError):
        s.decode_data()
