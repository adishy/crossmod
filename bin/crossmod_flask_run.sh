#!/bin/bash
# insta485db

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# if [ ! -f var/insta485.sqlite3 ]; then
#     ./bin/insta485db create
# fi

export FLASK_DEBUG=True
export FLASK_APP=crossmod
export CROSSMOD_SETTINGS=config.py

gunicorn crossmod:app --bind 0.0.0.0:8300 -w 5 --preload
