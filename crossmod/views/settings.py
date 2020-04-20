from crossmod.environments.consts import CrossmodConsts
from crossmod.db import CrossmodDB
from crossmod.db.tables import SubredditSettingsTable, UsersTable, UpdateStatusTable
from crossmod.helpers.authenticate_helper import admin_user
from flask import request
import flask
import json
import crossmod

@crossmod.app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if 'email' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    db = CrossmodDB()
    if request.method == 'POST': 
        if 'activate_moderation' in request.form:
            print("Activate moderation")
            subreddit_name = request.form['subreddit']
            row = db.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = True
            db.database_session.commit()

        elif 'deactivate_moderation' in request.form:
            print("Deactivate moderation")
            subreddit_name = request.form['subreddit']
            row = db.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = False
            db.database_session.commit()

        elif 'add_subreddit' in request.form:
            print("Adding subreddit")
            subreddit = flask.escape(request.form['subreddit'])
            subreddit_classifiers = flask.escape(request.form['subreddit_classifiers'])
            if subreddit_classifiers == "":
                subreddit_classifiers = ",".join(CrossmodConsts.SUBREDDIT_LIST)
            norm_classifiers = flask.escape(request.form['norm_classifiers'])
            if norm_classifiers == "":
                norm_classifiers = ",".join(CrossmodConsts.NORM_LIST)
            perform_action = False
            if request.form.get('perform_action'):
                perform_action = True
            db.write(SubredditSettingsTable, 
                     subreddit = subreddit, 
                     subreddit_classifiers = subreddit_classifiers,
                     norm_classifiers = norm_classifiers,
                     perform_action = perform_action)
                                
        elif 'remove_subreddit' in request.form:
            print("Removing subreddit")
            subreddit = flask.escape(request.form['subreddit'])
            db.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit).delete()
            db.database_session.commit()

        elif 'make_admin' in request.form:
            print("Adding admin user")
            email = flask.escape(request.form['email'])
            row = db.database_session.query(UsersTable).filter(UsersTable.email == email).one_or_none()
            if row is not None:
                row.admin = True
                db.database_session.commit()
        
        elif 'update_removal_config' in request.form:
            print("Updating Removal Config")
            agreement_score_threshold = float(flask.escape(request.form.get('agreement_score_threshold')))
            norm_violation_score_threshold = float(flask.escape(request.form.get('agreement_score_threshold')))
            updated_config = { "agreement_score_threshold": agreement_score_threshold, 
                               "norm_violation_score_threshold": norm_violation_score_threshold}
            row = db.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit).one_or_none()
            if row is not None:
                row.removal_config = json.dumps(updated_config)
                db.database_session.commit() 
        
        # PRG Pattern: https://en.wikipedia.org/wiki/Post/Redirect/Get
        return flask.redirect(flask.url_for('settings'))

    admin = False
    if 'email' in flask.session and len(flask.session['email']) > 0: 
        print("Email in session", flask.session['email'])
        admin = admin_user(db, flask.session['email'])

    context = { 'subreddits': db.database_session.query(SubredditSettingsTable).all(), 
                'admin_user': admin,
                'non_admin_users': db.database_session.query(UsersTable).filter(UsersTable.admin == False).all(),
                'db_update_status': db.database_session.query(UpdateStatusTable).all()
                }
    return flask.render_template('settings.html', **context)