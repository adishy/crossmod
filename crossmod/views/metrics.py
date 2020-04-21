import crossmod
import flask
import os
import glob
from crossmod.db import CrossmodDB, SubredditSettingsTable
from crossmod.environments import CrossmodConsts

@crossmod.app.route('/metrics/<metric>/<subreddit>', methods=['GET', 'POST'])
def show_metric(metric = None, subreddit = None):
    metric = metric.replace(".", "")
    metric_types = os.listdir(CrossmodConsts.METRICS_OUTPUT_DIRECTORY)
    metrics_output_directory = os.path.join(CrossmodConsts.METRICS_OUTPUT_DIRECTORY, metric)
    if metric is None or subreddit is None or metric not in metric_types or len(os.listdir(metrics_output_directory)) == 0:
        return flask.abort(404)
    metric_output_file = max(glob.glob(metrics_output_directory + f"/{subreddit}_*"), key=os.path.getctime)
    print(metric_output_file)
    response = flask.send_file(metric_output_file, mimetype="image/png")
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@crossmod.app.route('/metrics/', methods=['GET', 'POST'])
def all_available_metrics():
    db = CrossmodDB()
    all_subreddit_names = [x.subreddit for x in db.database_session.query(SubredditSettingsTable.subreddit).all()]
    if len(all_subreddit_names) == 0:
        return "No subreddits are being monitored"
    current_subreddit = all_subreddit_names[0] 
    if flask.request.method == "POST":
        if 'change_current_subreddit' in flask.request.form:
            to_change = flask.request.form.get('subreddit_to_change_to')
            if to_change in all_subreddit_names:
                current_subreddit = to_change
    response = {
        "metrics": [
                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_total_comments', subreddit = current_subreddit),
                            "description": f"x-axis: Time (days) y-axis: Number of comments each day in r/{current_subreddit})"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_crossmod_reports', subreddit = current_subreddit),
                            "description": f"x-axis: Time (days) y-axis: Number of comments reported by Crossmod each day in r/{current_subreddit}"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_moderator_removals', subreddit = current_subreddit),
                            "description": f"x-axis: Time (days) y-axis: Number of comments removed by human moderators each day, Number of comments removed by Automoderator each day in r/{current_subreddit}"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_reports_with_removals', subreddit = current_subreddit),
                            "description": f"x-axis: Time (days) y-axis: Number of comments that are reported/removed i.e. Number of Crossmod reports, Number of Human Removals, Number of Automod Removals for each day in r/{current_subreddit}"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_report_removal_sequences', subreddit = current_subreddit),
                            "description": f"x-axis: Time (days) y-axis: Number of comments reported by Crossmod that were removed by human moderators or Automod in r/{current_subreddit}"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'agreement_score_vs_comments', subreddit = current_subreddit),
                            "description": f"x-axis: Number of comments with agreement score > given agreement score threshold y -axis: Agreement score thresholds in r/{current_subreddit}"
                        }
                    ]
    }
    return flask.render_template('metrics.html', **response, current_subreddit = current_subreddit, all_subreddits = all_subreddit_names)