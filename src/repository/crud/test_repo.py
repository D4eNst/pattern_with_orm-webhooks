from repository.crud.base import BaseCRUDRepository
from repository.models.test_model import Test


class TestRepo(BaseCRUDRepository[Test]):
    model = Test

