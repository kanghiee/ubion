from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('link_page.html')

@app.route('/test')
def test():
    return render_template('main_page.html')

app.run(debug=True)