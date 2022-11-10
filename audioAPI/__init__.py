"""audioAPI package initializer."""
import flask
# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
# Read settings from config module (audioAPI/config.py)
app.config.from_object('audioAPI.config')

app.config.from_envvar('AUDIOAPI_SETTINGS', silent=True)

import audioAPI.api  # noqa: E402  pylint: disable=wrong-import-position
import audioAPI.views  # noqa: E402  pylint: disable=wrong-import-position
import audioAPI.model  # noqa: E402  pylint: disable=wrong-import-position
