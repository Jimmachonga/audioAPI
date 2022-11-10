"""audioAPI development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = ("b'C\xa3\x8f\xe9\xba\xde\x1f\x05\xc7\xe4H\xc76\x16'"
              "'j\xed\x88\xabD\xa4\xdd\xbd\x03\x8f'")
SESSION_COOKIE_NAME = 'login'
# File Upload to var/uploads/
AUDIOAPI_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = AUDIOAPI_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'mp4', 'm4a'])
MAX_CONTENT_LENGTH = 100 * 1024 * 1024
# Database file is var/audioAPI.sqlite3
DATABASE_FILENAME = AUDIOAPI_ROOT/'var'/'audioAPI.sqlite3'
