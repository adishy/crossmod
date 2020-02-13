"""Crossmod package initializer."""
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import flask


# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
cors = CORS(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute", "600 per hour"]
)

# Read settings from config module (insta485/config.py)
app.config.from_object('crossmod.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/config/
app.config.from_envvar('CROSSMOD_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import crossmod.views  # noqa: E402  pylint: disable=wrong-import-position
import crossmod.ml # noqa: E402  pylint: disable=wrong-import-position
import crossmod.helpers # noqa: E402  pylint: disable=wrong-import-position
import crossmod.api # noqa: E402  pylint: disable=wrong-import-position

from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.helpers.consts import CrossmodConsts
clf_ensemble = CrossmodClassifiers(subreddits = CrossmodConsts.SUBREDDIT_LIST,
                                   norms = CrossmodConsts.NORM_LIST)
