import crossmod
from crossmod.environments.consts import CrossmodConsts
from crossmod.db import CrossmodDB
from crossmod.db.tables import SubredditSettingsTable
from crossmod.db.tables import ApiKeyTable

import flask
from flask import request

from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import select
import strgen  # For generating new API KEY


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

        elif 'generate_key' in request.form:
            input_email = request.form['email']
            
            new_key = strgen.StringGenerator("[\w\d]{40}").render()
            print(f"Generating new API key associated under '{input_email}' and adding to ApiKeyTable:")
            print(f"New Key: {new_key}")
            db.write(ApiKeyTable,
                     email = input_email,
                     api_key = new_key,
                     access_level = 0)
        
            data = db.database_session.execute(select('*').select_from(ApiKeyTable)).fetchall()
            for row in data:
                print(row)

            # Send Email
            with open('/home/ubuntu/crossmod-dev/crossmod-updating-api/crossmod/views/key_gen_email_template.txt', 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
            message_template = Template(template_file_content)
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login('crossmoderator@gmail.com', 'Crossmoderator12345')
            msg = MIMEMultipart()
            message = message_template.substitute(API_KEY=new_key)
            msg['From']='crossmoderator@gmail.comm'
            msg['To']=input_email
            msg['Subject']="Your Crossmod API Key"
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            del msg
            s.quit()

            # Print all emails and keys onto the html file
             
        # PRG Pattern: https://en.wikipedia.org/wiki/Post/Redirect/Geti

        return flask.redirect(flask.url_for('settings'))

    subreddits = [row for row in db.database_session.query(SubredditSettingsTable).all()]
    context = { 'subreddits': subreddits }
    return flask.render_template('settings.html', **context)
