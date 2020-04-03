"""Helper functions related to the authenticate view."""

import uuid
import hashlib
import os
import shutil
import secrets
import tempfile
import flask
from crossmod.db import CrossmodDB
from crossmod.db.tables import UsersTable


def confirm_password(db, form_email, form_password):
    """Return true if the form password matches the password in the db."""
    def get_password_hash(algorithm, salt, form_password):
        """Return the hexdigest."""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update((salt + form_password).encode('utf-8'))
        return hash_obj.hexdigest()

    row = db.database_session.query(UsersTable).filter(UsersTable.email == form_email).one_or_none()

    if row is None:
        return False

    password_hash = row.password_hash
    password_components = password_hash.split('$')

    return password_components[2] == get_password_hash(
        password_components[0], password_components[1], form_password)


def account_exists(db, email):
    """Determine if a username exists in the database (for logging in)."""
    row = db.database_session.query(UsersTable).filter(UsersTable.email == email).one_or_none()
    return row is not None


def create_password(password):
    """Create a salted and hashed password to store in the database."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    print("Password database string:", password_db_string)
    return password_db_string


def create_account(db, email, password):
    """Write a new user to the database."""
    new_user = UsersTable(email = email, password_hash = create_password(password))
    db.database_session.add(new_user)
    db.database_session.commit()
    

def delete_user_in_db(db, email):
    """Remove a user from the database."""
    # Get users files
    db.database_session.query(UsersTable).filter(UsersTable.email == email).delete()
    db.database_session.commit()

def generate_csrf_token():
    flask.session['csrf_token'] = secrets.token_hex(16)

def check_csrf_token(request):
    csrf_token = request.form.get('csrf_token')
    return csrf_token is not None and csrf_token == flask.session['csrf_token']

def check_and_refresh_csrf(request):
    valid = check_csrf_token(request)
    generate_csrf_token()
    return valid