import functools
from . import aws
from . import exc
from . import retry
client = aws.session.client("s3")
NO_URL = "Failed to generate presigned url"


def _authorize(operation_name, key_name, expiration=900):
    with exc.on_botocore(NO_URL):
        return retry.exponential(
            _s3_authorize, (operation_name, key_name, expiration))


def _s3_authorize(operation_name, key_name, expiration):
    return client.generate_presigned_url(
        operation_name,
        {'Key': key_name, 'Bucket': 'blobapy-objects'},
        ExpiresIn=expiration)

authorize_put = functools.partial(_authorize, "put_object")
authorize_get = functools.partial(_authorize, "get_object")
