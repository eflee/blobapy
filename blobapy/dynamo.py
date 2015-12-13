from . import aws
import uuid
from bloop import Engine, UUID, Boolean, Column, ConstraintViolation
engine = Engine(session=aws.session)


def default(kwargs, key, value):
    kwargs[key] = kwargs.get(key, value)


class CreateFailed(Exception):
    pass


class Blob(engine.model):
    class Meta:
        table_name = "blobapy-blob"

    key_name = Column(UUID, hash_key=True, name='k')
    admin_key = Column(UUID, name='a')
    deleted = Column(Boolean, name='d')

    def __init__(self, **kwargs):
        default(kwargs, "deleted", False)
        super().__init__(**kwargs)

    @classmethod
    def unique(cls):
        retries = 5
        while retries:
            obj = cls(key_name=uuid.uuid4(), admin_key=uuid.uuid4())
            try:
                engine.save(obj, condition=_not_exists)
            except ConstraintViolation:
                retries -= 1
            else:
                return obj
        raise CreateFailed
engine.bind()

_not_exists = Blob.key_name.is_(None)
