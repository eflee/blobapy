import flask
from . import dynamo
from . import exc
from . import s3
app = flask.Flask(__name__)


@app.route("/authorize-get/<key_name>")
def get_object(key_name):
    """Return pre-signed URL for download"""
    url = s3.authorize_put(key_name)
    return flask.jsonify(url=url)


@app.route("/authorize-put")
def put_object():
    """Return pre-signed URL and key for upload; and delete auth token."""
    try:
        blob = dynamo.Blob.unique()
    except exc.OperationFailed:
        # TODO: Log exception
        flask.abort(500)
    url = s3.authorize_put(blob.key_name)
    return flask.jsonify(url=url, admin_key=blob.admin_key)
