import crossmod
from crossmod.environments.consts import CrossmodConsts
from crossmod.db import CrossmodDB
from crossmod.db.tables import SubredditSettingsTable
import flask
from flask import request

@crossmod.app.route('/settings/', methods=['GET', 'POST'])
def settings():
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

        elif 'add_key' in request.form:
            print("Adding a key to api table")
            #db.write()
        # PRG Pattern: https://en.wikipedia.org/wiki/Post/Redirect/Get
        return flask.redirect(flask.url_for('settings'))

    subreddits = [row for row in db.database_session.query(SubredditSettingsTable).all()]
    context = { 'subreddits': subreddits }
    return flask.render_template('settings.html', **context)
