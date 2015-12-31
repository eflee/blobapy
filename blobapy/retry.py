import collections.abc
import time


def ensure_tuple(arg):
    if arg is None:
        return tuple()
    if isinstance(arg, collections.abc.Iterable):
        return tuple(arg)
    return (arg,)


def exponential(func, args=None, kwargs=None,
                attempts=5, backoff_coeff=50, backoff_base=2,
                ignore=None):
    """backoff is calculated in ms.

    Raises last exception if all retries fail"""
    attempt = 0
    args = args or []
    kwargs = kwargs or {}
    ignore = ensure_tuple(ignore)
    last_exc = None
    while True:
        attempt += 1
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            if not isinstance(exc, ignore):
                raise exc
            last_exc = exc
        if attempt < attempts:
            backoff = backoff_coeff * (backoff_base ** attempt) / 1000.0
            time.sleep(backoff)
        else:
            raise last_exc
