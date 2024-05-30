class EntityException(Exception):

    def __init__(self, entity: str, *args, **kwargs):
        self.entity = entity

        super().__init__(f"{entity} exception.", *args, **kwargs)


class EntityNotExists(EntityException):
    pass


class EntityAlreadyExists(EntityException):
    pass
