import crossmod
from flask import render_template

@crossmod.app.route('/client/', methods=['GET'])
def client():
    return render_template('client.html')