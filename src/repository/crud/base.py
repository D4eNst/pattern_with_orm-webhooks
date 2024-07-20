from typing import TypeVar, Type, Generic, Sequence, Any, Optional, Union, Dict

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseCRUDRepository(Generic[T]):
    model: Type[T] = None

    def __init__(self, async_session: AsyncSession):
        super().__init__()
        self.async_session = async_session

    async def commit_changes(self):
        await self.async_session.commit()

    async def rollback_changes(self):
        await self.async_session.rollback()

    async def refresh_objects(self, instance: T):
        await self.async_session.refresh(instance=instance)

    async def close_session(self):
        await self.async_session.close()

    def _stmt_insert(self, values: Union[Dict[str, Any], Sequence[Dict[str, Any]]]):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        insert_stmt = (
            insert(self.model)
            .returning(self.model)
        )
        if isinstance(values, dict):
            return insert_stmt.values(**values)
        return insert_stmt.values(values)

    def _stmt_all(self):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        return select(self.model)

    def _stmt_filter(self, *filters, **filter_by):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        filter_stmt = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        return filter_stmt

    def _stmt_get(self, *filters, **filter_by):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        get_stmt = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        return get_stmt

    def _stmt_update(self, *filters, **kwargs):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        update_stmt = (
            update(table=self.model)
            .where(*filters)
            .values(**kwargs)
            .returning(self.model)
        )
        return update_stmt

    def _stmt_delete(self, *filters):
        """
        Override this method to change the logic, add filters, sorting, ect
        """
        delete_stmt = (
            delete(table=self.model)
            .filter(*filters)
            .returning(self.model)
        )
        return delete_stmt

    async def create(self, commit: bool = True, **kwargs) -> T:
        """
        Create a new instance of the model using the provided keyword arguments, and optionally commit the changes.

        Args:
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.
            **kwargs: Keyword arguments representing the values to be inserted into the new instance.

        Returns:
            T: The newly created instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Create a new user with specified attributes and commit changes\n
            created_user = await user_repo.create(name='Alice', age=30)\n

            # Create a new post with specified attributes without committing changes
            created_user = await user_repo.create(name='Bob', age=25)\n
            ...\n
            await user_repo.commit_changes()
        """
        insert_stmt = self._stmt_insert(kwargs)

        query = await self.async_session.execute(insert_stmt)
        created_user = query.scalar()

        if commit:
            await self.commit_changes()

        return created_user

    async def create_many(self, rows: Sequence[Dict[str, Any]], commit: bool = True) -> Sequence[T]:
        """
        Create multiple instances of the model using the provided dictionaries representing object attributes,
        and optionally commit the changes.

        Args:
            rows (Sequence[dict[str, Any]]): A sequence of dictionaries representing attribute values for
                                             the new objects.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            Sequence[T]: A sequence of the newly created instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Create multiple users with specified attributes and commit changes\n
            rows = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]\n
            created_users = await user_repo.create_many(rows)\n

            # Create multiple posts with specified attributes without committing changes\n
            rows = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]\n
            created_posts = await user_repo.create_many(rows, commit=False)\n
            ...\n
            await user_repo.commit_changes()
        """
        insert_stmt = self._stmt_insert(rows)

        query = await self.async_session.execute(insert_stmt)
        created_users = query.scalars()

        if commit:
            await self.commit_changes()

        return created_users.all()

    async def create_obj(self, new_obj: T, commit: bool = True) -> T:
        """
        Create a new instance of the model using the provided object, and optionally commit the changes.

        Args:
            new_obj (T): An instance of the model containing data for the new object.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            T: The newly created instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n

            # Create a new user object and commit changes\n
            user = User(name='Alice', age=30)\n
            created_user = await user_repo.create_obj(user)

            # Create a new user object without committing changes\n
            user = User(name='Bob', age=25)\n
            created_user = await user_repo.create_obj(user, commit=False)\n
            ...\n
            await user_repo.commit_changes()
        """
        insert_values = {
            attr.key: getattr(new_obj, attr.key)
            for attr in self.model.__table__.columns
            if attr.key in new_obj.__dict__
        }
        return await self.create(commit, **insert_values)

    async def create_many_obj(self, objs: Sequence[T], commit: bool = True) -> Sequence[T]:
        """
        Create multiple instances of the model using the provided objects, and optionally commit the changes.

        Args:
            objs (Sequence[T]): A sequence of instances of the model containing data for the new objects.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            Sequence[T]: A sequence of the newly created instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Create multiple user objects and commit changes\n
            users = [User(name='Alice', age=30), User(name='Bob', age=25)]\n
            created_users = await user_repo.create_many_obj(users)

            # Create multiple user objects without committing changes\n
            users = [User(name='Charlie', age=35), User(name='David', age=40)]\n
            created_users = await user_repo.create_many_obj(users, commit=False)\n
            ...\n
            await user_repo.commit_changes()
        """
        rows = [
            {
                attr.key: getattr(new_obj, attr.key)
                for attr in self.model.__table__.columns
                if attr.key in new_obj.__dict__
            }
            for new_obj in objs
        ]

        return await self.create_many(rows, commit)

    async def all(self) -> Sequence[T]:
        """
        Retrieve all instances of the model from the database.

        Returns:
            Sequence[T]: A sequence of all instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Retrieve all users from the database\n
            all_users = await db_session.all(User)\n
        """
        stmt = self._stmt_all()
        query = await self.async_session.execute(statement=stmt)
        result = query.scalars()
        return result.all()

    async def filter(self, *filters, **filter_by) -> Sequence[T]:
        """
        Retrieve instances of the model from the database that match the provided filters.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            **filter_by: Filter conditions provided as keyword arguments.
                         These filter conditions are in the form of column_name=value.

        Returns:
            Sequence[T]: A sequence of instances of the model matching the provided filters.

        Examples:
            user_repo = UserRepo(async_session)

            # Get users instance with id=1\n
            user = await user_repo.filter(id=1)

            # Get users instance with name='Alice' and age > 30\n
            user = await db_session.filter(User.age > 30, name='Alice')
        """
        filter_stmt = self._stmt_filter(*filters, **filter_by)
        query = await self.async_session.execute(statement=filter_stmt)
        result = query.scalars()
        return result.all()

    async def get_or_none(self, *filters, **filter_by) -> Optional[T]:
        """
        Retrieve a single instance of the model that matches the provided filters,
        or return None if no such instance exists.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            **filter_by: Filter conditions provided as keyword arguments.
                         These filter conditions are in the form of column_name=value.

        Returns:
            Optional[T]: An instance of the model matching the provided filters, or None.

        Examples:
            user_repo = UserRepo(async_session)

            # Get a user instance with id=1\n
            user = await user_repo.get_or_none(id=1)

            # Get a user instance with name='Alice' and age > 30\n
            user = await db_session.get_or_none(User.age > 30, name='Alice')
        """
        get_stmt = self._stmt_get(*filters, **filter_by)
        query = await self.async_session.execute(statement=get_stmt)
        result = query.scalars().one_or_none()
        return result

    async def get(self, *filters, **filter_by) -> T:
        """
        Retrieve a single instance of the model that matches the provided filters,
        or raise an EntityDoesNotExistError if no such instance exists.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            **filter_by: Filter conditions provided as keyword arguments.
                         These filter conditions are in the form of column_name=value.

        Returns:
            T: An instance of the model matching the provided filters.

        Examples:
            user_repo = UserRepo(async_session)

            # Get a user instance with id=1\n
            user = await user_repo.get(id=1)

            # Get a user instance with name='Alice' and age > 30\n
            user = await db_session.get(User.age > 30, name='Alice')
        """
        get_stmt = self._stmt_get(*filters, **filter_by)
        query = await self.async_session.execute(statement=get_stmt)
        result = query.scalars().one()
        return result

    async def update(self, *filters, commit: bool = True, **kwargs) -> T:
        """
        Update a single instance of the model in the database that matches the provided filters with
        the specified values.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.
            **kwargs: Values to be updated for the matching instance.

        Returns:
            T: The updated instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Update a single user with id=1 to set their age to 30 and role to 'admin'\n
            updated_user = await user_repo.update(User.id == 1, age=30, role='admin')

        Note:
            If you are updating a single object and need to commit the changes immediately, you can use the
            `commit_changes()` method. However, if you are updating multiple objects with the same changes,
            it is recommended to use the `update_many()` method to reduce the number of SQL queries.
        """
        update_stmt = self._stmt_update(*filters, **kwargs)
        query = await self.async_session.execute(statement=update_stmt)
        updated_object = query.scalars().one()

        if commit:
            await self.commit_changes()

        return updated_object

    async def update_many(self, *filters, commit: bool = True, **kwargs) -> Sequence[T]:
        """
        Update multiple instances of the model in the database that match the provided filters
        with the specified values.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.
            **kwargs: Values to be updated for the matching instances.

        Returns:
            Sequence[T]: A sequence of the updated instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Update all users with age less than 30 to set their status to "young"\n
            updated_users = await user_repo.update_many(User.age < 40, status="young")

        Note:
            If you are updating a single object and need to commit the changes immediately, you can use the
            `commit_changes()` method. However, if you are updating multiple objects with the same changes,
            it is recommended to use the `update_many()` method to reduce the number of SQL queries.
        """
        update_stmt = self._stmt_update(*filters, **kwargs)
        query = await self.async_session.execute(statement=update_stmt)
        updated_objects = query.scalars()

        if commit:
            await self.commit_changes()

        return updated_objects.all()

    async def update_by_id(self, id: int, commit: bool = True, **kwargs) -> T:
        """
        Update an instance of the model in the database with the specified id with the provided values.

        Args:
            id (int): The id of the instance to update.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.
            **kwargs: Values to be updated for the instance.

        Returns:
            T: The updated instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Update user with id=1 to set their age to 30 and role to 'admin'\n
            updated_user = await user_repo.update_by_id(1, age=30, role='admin')
        """
        return await self.update(self.model.id == id, commit=commit, **kwargs)

    async def delete(self, *filters, commit: bool = True) -> T:
        """
        Delete a single instance of the model from the database that matches the provided filters.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            T: The deleted instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Delete a single user with id=1\n
            deleted_user = await user_repo.delete(User.id == 1)
        """
        delete_stmt = self._stmt_delete(*filters)
        query = await self.async_session.execute(statement=delete_stmt)
        deleted_object = query.scalars().one()

        if commit:
            await self.commit_changes()

        return deleted_object

    async def delete_many(self, *filters, commit: bool = True) -> Sequence[T]:
        """
        Delete multiple instances of the model from the database that match the provided filters.

        Args:
            *filters: Additional filter conditions provided as SQLAlchemy expressions.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            Sequence[T]: A sequence of the deleted instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Delete all users with age less than 30\n
            deleted_users = await user_repo.delete_many(User.age < 30)
        """
        delete_stmt = self._stmt_delete(*filters)
        query = await self.async_session.execute(statement=delete_stmt)
        deleted_objects = query.scalars()

        if commit:
            await self.commit_changes()

        return deleted_objects.all()

    async def delete_by_id(self, id: int, commit: bool = True) -> T:
        """
        Delete an instance of the model from the database with the specified id.

        Args:
            id (int): The id of the instance to delete.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            T: The deleted instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Delete a user with id=1\n
            deleted_user = await user_repo.delete_by_id(1)
        """
        return await self.delete(self.model.id == id, commit=commit)

    async def delete_obj(self, deleted_obj: T, commit: bool = True) -> T:
        """
        Delete an instance of the model from the database.

        Args:
            deleted_obj (T): The instance of the model to delete.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            T: The deleted instance of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Delete a specific user object\n
            user = await user_repo.get(id=1)\n
            deleted_user = await user_repo.delete_obj(user)
        """
        return await self.delete(self.model.id == deleted_obj.id, commit=commit)

    async def delete_many_obj(self, deleted_objs: Sequence[T], commit: bool = True) -> Sequence[T]:
        """
        Delete multiple instances of the model from the database.
        The id field is used as a filter for deletion

        Args:
            deleted_objs (Sequence[T]): A sequence of instances of the model to delete.
            commit (bool, optional): Whether to commit the changes to the database. Defaults to True.

        Returns:
            Sequence[T]: A sequence of the deleted instances of the model.

        Examples:
            user_repo = UserRepo(async_session)\n
            # Delete multiple user objects\n
            users = await user_repo.filter(User.age < 20)\n
            deleted_users = await db_session.delete_many_obj(users)
        """
        id_to_delete = [deleted_obj.id for deleted_obj in deleted_objs]
        return await self.delete_many(self.model.id.in_(id_to_delete), commit=commit)
