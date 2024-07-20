from repository.crud.base import BaseCRUDRepository
from repository.models.user import User


class UserRepo(BaseCRUDRepository[User]):
    model = User

