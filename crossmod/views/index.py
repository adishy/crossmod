from flask import render_html

@crossmod.app.route('/', methods=['GET'])
def index():
    return render_html('index.html')