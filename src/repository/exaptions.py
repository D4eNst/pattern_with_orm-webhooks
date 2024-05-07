class EntityDoesNotExistError(Exception):
    def __init__(self, msg=None, model=None):
        if not msg and model:
            msg = f"Object {model.__name__} does not exist!"
            super().__init__(msg)
        else:
            default_msg = "Object does not exist!"
            super().__init__(default_msg if msg is None else msg)
