from . import aws

client = aws.session.client("s3")


def authorize_put(key_name):
    return _authorize_operation("put_object", key_name)


def authorize_get(key_name):
    return _authorize_operation("get_object", key_name)


def _authorize_operation(operation_name, key_name, expiration=900):
    url = client.generate_presigned_url(
        operation_name,
        {'Key': key_name, 'Bucket': 'blobapy-objects'},
        ExpiresIn=expiration)
    return url
