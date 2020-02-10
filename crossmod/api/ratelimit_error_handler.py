import crossmod
from flask import make_response, jsonify

## Exceeded call rate message ##
@crossmod.app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(error="API call rate limit exceeded %s" % e.description)
        , 429
    )
