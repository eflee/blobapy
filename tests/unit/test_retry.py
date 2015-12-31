import pytest
import time
import blobapy.exc
import blobapy.retry


@pytest.fixture
def patch_sleep(monkeypatch):
    sleep_args = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleep_args.append(s))
    return {"calls": sleep_args}


def test_exponential_returns_func_result():
    passed_args = []
    passed_kwargs = {}
    expected_result = "return value"

    def func(*args, **kwargs):
        passed_args.extend(args)
        passed_kwargs.update(kwargs)
        return expected_result

    args = [object(), "foo"]
    kwargs = {"foo": object(), "bar": False}
    result = blobapy.retry.exponential(func, args=args, kwargs=kwargs)

    assert result == expected_result
    assert args == passed_args
    assert kwargs == passed_kwargs


def test_exponential_correct_backoff(patch_sleep):
    class Retryable(Exception):
        pass
    calls = 0

    def func():
        nonlocal calls
        calls += 1
        if calls <= 3:
            raise Retryable
        return True

    result = blobapy.retry.exponential(func, ignore=Retryable,
                                       backoff_coeff=35, backoff_base=3)
    assert result
    assert patch_sleep["calls"] == [0.105, 0.315, 0.945]


def test_exponential_unexpected():
    class Unrecoverable(Exception):
        pass

    def func():
        raise Unrecoverable()

    with pytest.raises(Unrecoverable):
        blobapy.retry.exponential(func)


def test_exponential_max_attempts(patch_sleep):
    class Retryable(Exception):
        pass

    def func():
        raise Retryable

    with pytest.raises(blobapy.exc.OperationFailed):
        blobapy.retry.exponential(func, ignore=Retryable)
    assert patch_sleep["calls"] == [0.1, 0.2, 0.4, 0.8]


def test_exponential_ignore_multiple(patch_sleep):
    class R1(Exception):
        pass

    class R2(Exception):
        pass
    calls = 0

    def func():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise R1
        elif calls == 2:
            raise R2
        return True

    assert blobapy.retry.exponential(func, ignore=[R1, R2])
    assert patch_sleep["calls"] == [0.1, 0.2]
