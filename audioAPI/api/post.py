"""API for post."""
import flask
from audioAPI.api.authentication import login
import audioAPI
from werkzeug.utils import secure_filename
from tinytag import TinyTag
from pathlib import Path
import os

@audioAPI.app.route('/post', methods=['POST'])
def post_audio():
    """Post audio data."""
    
    login()

    user = flask.session['username']

    f = flask.request.files['file']

    filename = secure_filename(f.filename)

    # temp storage - use fs
    uploads_dir = audioAPI.app.config['UPLOAD_FOLDER'] / Path(user)

    os.makedirs(uploads_dir, exist_ok=True)

    filePath = uploads_dir / Path(filename)

    f.save(filePath)

    # get metadata
    audio = TinyTag.get(filePath)

    connection = audioAPI.model.get_db()
    # insert into database
    cur = connection.execute(
        "INSERT INTO files (owner, filename, duration, bitrate, size) VALUES"
        "(?, ?, ?, ?, ?)",
        (user, filename, audio.duration, audio.bitrate, audio.filesize,)
    )

    context = {
        "Status": "success"
    }

    return flask.make_response(flask.jsonify(**context), 201)