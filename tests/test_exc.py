import botocore.exceptions
import pytest
from blobapy import exc


def test_context_wraps():
    msg = "Custom message"
    with pytest.raises(exc.OperationFailed) as excinfo:
        with exc.on_botocore(msg):
            raise botocore.exceptions.BotoCoreError()
    assert excinfo.type is exc.OperationFailed
    assert excinfo.value.args == (msg,)


def test_context_noraise():
    msg = "Custom message"
    with exc.on_botocore(msg):
        pass
