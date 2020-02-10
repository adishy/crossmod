import crossmod
from crossmod.helpers.index_helper import current_overall_stats
from flask import render_template

@crossmod.app.route('/dashboard/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', stats = current_overall_stats())