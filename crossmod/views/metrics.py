import crossmod
import flask
import os
import glob
from crossmod.environments import CrossmodConsts

@crossmod.app.route('/metrics/<metric>/', methods=['GET', 'POST'])
def show_metric(metric = None):
    metric = metric.replace(".", "")
    metric_types = os.listdir(CrossmodConsts.METRICS_OUTPUT_DIRECTORY)
    metrics_output_directory = os.path.join(CrossmodConsts.METRICS_OUTPUT_DIRECTORY, metric)
    if metric is None or len(metric) == 0 or metric not in metric_types or len(os.listdir(metrics_output_directory)) == 0:
        return flask.abort(404)
    metric_output_file = max(glob.glob(metrics_output_directory + "/*"), key=os.path.getctime)
    print(metric_output_file)
    response = flask.send_file(metric_output_file, mimetype="image/png")
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@crossmod.app.route('/metrics/', methods=['GET', 'POST'])
def all_available_metrics():
    response = {
        "metrics": [
                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_total_comments'),
                            "description": "x-axis: Time (days) y-axis: Number of comments each day in r/Futurology)"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_crossmod_reports'),
                            "description": "x-axis: Time (days) y-axis: Number of comments reported by Crossmod each day in r/Futurology"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_moderator_removals'),
                            "description": "x-axis: Time (days) y-axis: Number of comments removed by human moderators each day, Number of comments removed by Automoderator each day"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_reports_with_removals'),
                            "description": "x-axis: Time (days) y-axis: Number of comments that are reported/removed i.e. Number of Crossmod reports, Number of Human Removals, Number of Automod Removals for each day"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'rate_of_report_removal_sequences'),
                            "description": "x-axis: Time (days) y-axis: Number of comments reported by Crossmod that were removed by human moderators or Automod"
                        },

                        {
                            "url": flask.url_for('show_metric', metric = 'agreement_score_vs_comments'),
                            "description": "x-axis: Number of comments with agreement score > given agreement score threshold y -axis: Agreement score thresholds"
                        }
                    ]
    }
    if flask.request.method == "POST":
        return flask.jsonify(response)
    return flask.render_template('metrics.html', **response)