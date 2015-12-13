from . import aws
from . import exc
import uuid
from bloop import Engine, UUID, Boolean, Column, ConstraintViolation
engine = Engine(session=aws.session)


def default(kwargs, key, value):
    kwargs[key] = kwargs.get(key, value)


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
        with exc.on_botocore("Failed to generate unique key_name"):
            retries = 5
            while retries:
                obj = cls(key_name=uuid.uuid4(), admin_key=uuid.uuid4())
                try:
                    engine.save(obj, condition=Blob.NOT_EXISTS)
                except ConstraintViolation:
                    retries -= 1
                else:
                    return obj
            raise exc.OperationFailed

engine.bind()
