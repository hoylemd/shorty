import hashlib
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return hashlib.sha224(url).hexdigest()

    # do get stuff
    abort(400)


if __name__ == '__main__':
    app.run()
