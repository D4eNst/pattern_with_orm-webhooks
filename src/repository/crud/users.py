from repository.crud.base import BaseCRUDRepository
from repository.models.test_model import User


class UserRepo(BaseCRUDRepository[User]):
    model = User

