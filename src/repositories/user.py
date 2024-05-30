from sqlalchemy.orm import Session
from database.schema import UserSchema
from ports.repositories import Repository
from domain import User


class UserRepository(Repository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: User) -> User:
        user = UserSchema(first_name=entity.first_name, last_name=entity.last_name)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return User(**vars(user))

    def delete(self, id: int) -> None:
        self.session.query(UserSchema).filter_by(id=id).delete()
        self.session.commit()
        self.session.flush()

    def find_by_id(self, id: int) -> User:
        user = self.session.query(UserSchema).get(id)
        return self.__to_entity(user) if user else None

    def find_all(self, **filters) -> list[User]:
        users = self.session.query(UserSchema).filter_by(**filters).all()

        return [UserRepository.__to_entity(user) for user in users] if users else []

    def update(self, id: int, entity: User) -> None:
        user = UserSchema(
            id=id,
            first_name=entity.first_name,
            last_name=entity.last_name,
        )

        self.session.merge(user)
        self.session.commit()

    @staticmethod
    def __to_entity(user: UserSchema) -> User:
        return User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            created_on=user.created_on,
        )
