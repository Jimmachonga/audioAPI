"""REST API for authentication."""
import hashlib
import flask
import audioAPI


class InvalidUsage(Exception):
    """Handles exceptions."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialize."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert to json."""
        rando = dict(self.payload or ())
        rando['message'] = self.message
        rando['status_code'] = self.status_code
        return rando


@audioAPI.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle error."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def login():
    """Display / route."""
    if 'username' in flask.session:
        return
    if not flask.request.authorization:
        raise InvalidUsage('Forbidden', status_code=403)
    password = flask.request.authorization['password']
    if not password:
        raise InvalidUsage('Forbidden', status_code=403)
    username = flask.request.authorization['username']
    if not username:
        raise InvalidUsage('Forbidden', status_code=403)

    # Connect to database
    connection = audioAPI.model.get_db()
    # Query database
    cur = connection.execute(
        "SELECT password FROM users "
        "WHERE users.username = ?",
        (username, )
    )
    db_password = cur.fetchall()
    if db_password:
        db_password = db_password[0]['password']
    else:
        raise InvalidUsage('Forbidden', status_code=403)

    algorithm = 'sha512'
    salt = db_password.split('$')[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    if db_password != password_db_string:
        print(password_db_string)
        print(db_password)
        raise InvalidUsage('Forbidden', status_code=403)

    flask.session['username'] = username
