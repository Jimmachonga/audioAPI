"""
audioAPI index view.

URLs include:
/
"""
import flask
import audioAPI
import hashlib
import uuid


@audioAPI.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    user = flask.session['username']
    # Add database info to context
    context = {"logname": user}
    return flask.render_template("index.html", **context)


@audioAPI.app.route('/accounts/login/', methods=['GET'])
def login():
    """Display / route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("login.html")


@audioAPI.app.route('/accounts/logout/', methods=['GET'])
def logout():
    """Display / route."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))

@audioAPI.app.route('/accounts/create/')
def show_create():
    """Display / route."""
    if 'username' in flask.session:
        return flask.url_for('show_index')
    return flask.render_template("create.html")

@audioAPI.app.route('/accounts/', methods=['POST'])
def account_actions():
    """Display / route."""
    target_url = flask.request.args.get('target')
    if not target_url:
        target_url = '/'

    if flask.request.form.get('operation') == "login":
        password = flask.request.form.get('password')
        if not password:
            flask.abort(400)
        username = flask.request.form.get('username')
        if not username:
            flask.abort(400)

        # Connect to database
        conn = audioAPI.model.get_db()
        # Query database
        cur = conn.execute(
            "SELECT password FROM users "
            "WHERE users.username = ?",
            (username, )
        )
        d_password = cur.fetchall()
        if d_password:
            d_password = d_password[0]['password']
        else:
            flask.abort(403)

        algorithm = 'sha512'
        salt = d_password.split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_saltd = salt + password
        hash_obj.update(password_saltd.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        if d_password != password_db_string:
            print(password_db_string)
            print(d_password)
            flask.abort(403)

        flask.session['username'] = username
        return flask.redirect(target_url)
    
    if flask.request.form.get('operation') == "create":
        password = flask.request.form.get('password')
        if not password:
            flask.abort(400)
        username = flask.request.form.get('username')
        if not username:
            flask.abort(400)
        fullname = flask.request.form.get('fullname')
        email = flask.request.form.get('email')

        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_saltd = salt + password
        hash_obj.update(password_saltd.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Connect to database
        conn = audioAPI.model.get_db()
        # Query database
        cur = conn.execute(
            "INSERT INTO users(username, fullname, email, password) VALUES"
            "(?, ?, ?, ?)",
            (username, fullname, email, password_db_string, )
        )

        flask.session['username'] = username
        return flask.redirect(target_url)
    return ''
