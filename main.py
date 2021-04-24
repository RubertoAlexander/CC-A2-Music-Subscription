from flask.templating import render_template
from app import app

@app.route('/')
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host="127.0.0.1", port=80)
