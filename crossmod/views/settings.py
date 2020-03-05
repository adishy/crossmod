import crossmod
from crossmod.environments.consts import CrossmodConsts
from crossmod.db.tables import SubredditSettingsTable
import flask
from flask import request

@crossmod.app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST': 
        if 'activate_moderation' in request.form:
            print("Activate moderation")
            subreddit_name = request.form['subreddit']
            row = crossmod.db_interface.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = True
            crossmod.db_interface.database_session.commit()

        elif 'deactivate_moderation' in request.form:
            print("Deactivate moderation")
            subreddit_name = request.form['subreddit']
            row = crossmod.db_interface.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = False
            crossmod.db_interface.database_session.commit()

        elif 'add_subreddit' in request.form:
            print("Adding subreddit")
            print(f"Request subreddit {request.form['subreddit']}")
            print(f"Request subreddit {request.form['subreddit_classifiers']}")
            print(f"Request subreddit {request.form['norm_classifiers']}")
            print(f"Request subreddit {request.form['perform_action']}")
            subreddit = flask.escape(request.form['subreddit'])
            subreddit_classifiers = flask.escape(request.form['subreddit_classifiers'])
            if subreddit_classifiers == "":
                subreddit_classifiers = CrossmodConsts.SUBREDDIT_LIST
            norm_classifiers = flask.escape(request.form['macro_norm_classifiers'])
            if norm_classifiers == "":
                norm_classifiers = CrossmodConsts.NORM_LIST
            perform_action = False
            if request.form.get('perform_action'):
                perform_action = True
            crossmod.db_interface.write(SubredditSettingsTable, 
                                        subreddit = subreddit, 
                                        subreddit_classifiers = subreddit_classifiers,
                                        norm_classifiers = norm_classifiers)

    subreddits = [row for row in crossmod.db_interface.database_session.query(SubredditSettingsTable).all()]
    context = { 'subreddits': subreddits }
    return flask.render_template('settings.html', **context)