"""REST API for resource."""
import flask
import audioAPI


@audioAPI.app.route('/api', methods=["GET"])
def get_resource():
    """Display information."""
    context = {
        "post": "/post",
        "download": "/download",
        "list": "/list",
        "info": "/info"
    }
    return flask.jsonify(**context)
