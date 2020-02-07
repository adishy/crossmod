import crossmod
from flask import render_template

@crossmod.app.route('/', methods=['GET'])
def index():
    return render_template('index.html')