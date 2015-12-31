import uuid
from bloop import Engine, UUID, Boolean, Column, ConstraintViolation
from . import aws
from . import exc
from . import retry
engine = Engine(session=aws.session)


def default(kwargs, key, value):
    """If `key` is missing from a dict, set it to `value`"""
    kwargs[key] = kwargs.get(key, value)


NO_UNIQUE = "Failed to generate unique key_name"


class Blob(engine.model):
    class Meta:
        table_name = "blobapy-blob"

    key_name = Column(UUID, hash_key=True, name='k')
    admin_key = Column(UUID, name='a')
    deleted = Column(Boolean, name='d')

    NOT_EXISTS = key_name.is_(None)

    def __init__(self, **kwargs):
        default(kwargs, "deleted", False)
        super().__init__(**kwargs)

    @classmethod
    def unique(cls):
        with exc.on_botocore(NO_UNIQUE):
            return retry.exponential(
                cls._generate, ignore=ConstraintViolation)

    @classmethod
    def _generate(cls):
        obj = cls(key_name=uuid.uuid4(), admin_key=uuid.uuid4())
        engine.save(obj, condition=Blob.NOT_EXISTS)
        return obj

engine.bind()
