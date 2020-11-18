import crossmod
from crossmod.helpers.index_helper import current_overall_stats
from flask import render_template, redirect

@crossmod.app.route('/', methods=['GET'])
def index():
    return render_template('index.html', stats = current_overall_stats())

@crossmod.app.route('/db', methods=['GET'])
def db_monitor():
    return redirect("http://crossmod.ml:5000", code=302)

@crossmod.app.route('/notebooks', methods=['GET'])
def notebooks():
    return redirect("https://crossmod.ml:8888", code=302)

@crossmod.app.route('/notebook_metrics/<path:filename>', methods=['GET'])
def notebook_metrics(filename):
    return crossmod.app.send_static_file(filename)

