"""API for get."""
import flask
import audioAPI
from audioAPI.api.authentication import login
import sys
from pathlib import Path

@audioAPI.app.route('/download', methods=["GET"])
def download():
    """Download files."""
    login()

    user = flask.session['username']
    
    name = flask.request.args.get("name")

    return flask.send_from_directory(
        audioAPI.app.config['UPLOAD_FOLDER'] / Path(user), name, as_attachment=True
    )

@audioAPI.app.route('/list', methods=["GET"])
def list():
    """List files by properties."""
    duration = flask.request.args.get("maxduration", default=sys.float_info.max, type=float)
    bitrate = flask.request.args.get("minbitrate", default=0, type=float)
    size = flask.request.args.get("maxsize", default=sys.maxsize, type=int)
    login()

    user = flask.session['username']
    # Connect to database
    connection = audioAPI.model.get_db()
    # Query database
    cur = connection.execute(
        "SELECT filename FROM files "
        "WHERE owner = ? AND duration <= ? "
        "AND bitrate >= ? AND size <= ?",
        (user, duration, bitrate, size, )
    )
    posts = cur.fetchall()

    return flask.jsonify(posts)

@audioAPI.app.route('/info', methods=["GET"])
def info():
    """Display metadata."""
    name = flask.request.args.get("name")
    login()

    user = flask.session['username']
    # Connect to database
    connection = audioAPI.model.get_db()
    # Query database
    cur = connection.execute(
        "SELECT * FROM files "
        "WHERE owner = ? AND filename = ? ",
        (user, name, )
    )
    posts = cur.fetchall()

    return flask.jsonify(posts)
