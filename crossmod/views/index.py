import crossmod
from crossmod.helpers.index_helper import current_overall_stats
from flask import render_template

@crossmod.app.route('/', methods=['GET'])
def index():
    return render_template('index.html', stats = current_overall_stats())