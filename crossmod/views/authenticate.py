from crossmod.helpers.authenticate_helper import *
import crossmod
import flask


@crossmod.app.route('/accounts/login/', methods = ['GET', 'POST'])
def login():
    if 'email' in flask.session:
        return flask.redirect(flask.url_for('settings'))
    if flask.request.method == 'POST':
        db = CrossmodDB()
        email = flask.request.form['email']
        password = flask.request.form['password']
        if not confirm_password(db, email, password):
            flask.abort(403)
        flask.session['email'] = email
        return flask.redirect(flask.url_for('settings'))
    context = { "csrf_token": generate_csrf_token() }
    return flask.render_template('login.html', **context)


@crossmod.app.route('/accounts/logout/', methods = ['GET', 'POST'])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@crossmod.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Create a user by storing their details in the database."""
    if 'email' in flask.session:
        return flask.redirect(flask.url_for("login"))

    db = CrossmodDB()

    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']

        if account_exists(db, email):
            print("Account already exists")
            flask.abort(409)

        if password == "":
            flask.abort(400)

        create_account(db, email, password)
        flask.session['email'] = email

        return flask.redirect(flask.url_for('settings'))
    
    context = { "csrf_token": generate_csrf_token() }
    return flask.render_template("create.html", **context)