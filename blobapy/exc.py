import botocore.exceptions
import contextlib


class OperationFailed(Exception):
    pass


@contextlib.contextmanager
def on_botocore(msg):
    """raises OperationFailed if a BotoCoreError occurrs"""
    try:
        yield
    except botocore.exceptions.BotoCoreError:
        # TODO: Log exception
        raise OperationFailed(msg)
