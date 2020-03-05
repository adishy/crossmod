import crossmod
from crossmod.db.tables import SubredditSettingsTable
import flask

@crossmod.app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if flask.request.method == 'POST': 
        if 'activate_moderation' in flask.request.form:
            print("Activate moderation")
            subreddit_name = flask.request.form['subreddit']
            row = crossmod.db_interface.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = True
            crossmod.db_interface.database_session.commit()

        elif 'deactivate_moderation' in flask.request.form:
            print("Deactivate moderation")
            subreddit_name = flask.request.form['subreddit']
            row = crossmod.db_interface.database_session.query(SubredditSettingsTable).filter(SubredditSettingsTable.subreddit == subreddit_name).one()
            row.perform_action = False
            crossmod.db_interface.database_session.commit()
        elif 'add_subreddit' in flask.request.form:
            print("Adding subreddit")
            print(f"Request subreddit {flask.request.form['subreddit']}")
            print(f"Request subreddit {flask.request.form['moderator_list']}")
            print(f"Request subreddit {flask.request.form['subreddit_classifiers']}")
            print(f"Request subreddit {flask.request.form['macro_norm_classifiers']}")
            print(f"Request subreddit {flask.request.form['perform_action']}")
            
    
    subreddits = [row for row in crossmod.db_interface.database_session.query(SubredditSettingsTable).all()]

    context = { 'subreddits': subreddits }

    return flask.render_template('settings.html', **context)