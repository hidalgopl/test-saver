import pytest
from pony import orm

from test_saver.models import TestDTO as DTO
from test_saver.serializer import TestSerializer as Serializer


@pytest.fixture
def db(autouse=True):
    yield orm.Database()


def test_decode_data():
    data = {
        "code": "SEC#001",
        "result": 1,
        "suite_id": 1
    }
    s = Serializer(msg=data, db=db)
    decoded = s.decode_data()
    assert isinstance(decoded, DTO)


def test_decode_missing_data():
    data = {
        "code": "SEC#001",
        "suite_id": 1
    }
    s = Serializer(msg=data, db=db)
    with pytest.raises(KeyError):
        s.decode_data()


# def test_wrong_data_type():
#     data = {
#         "code": "SEC#001",
#         "result": "1", # should be int
#         "suite_id": 1
#     }
#     s = Serializer(msg=data, db=db)
#     dto = s.decode_data()
#     assert isinstance(dto.result, int)
