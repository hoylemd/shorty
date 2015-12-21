import hashlib
import sqlite3
from contextlib import closing
from flask import Flask, request, g, redirect

app = Flask(__name__)
# configuration
DATABASE = 'tmp.db'
DEBUG = True
SECRET_KEY = 'marhmallows'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def after_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def actually_create_shortcode(url):
    shortcode = hashlib.sha224(url).hexdigest()
    try:
        g.db.execute(
            'insert into urls (hash, full_url) values (?, ?)',
            [shortcode, url]
        )
        g.db.commit()
    except sqlite3.IntegrityError:
        pass
    return shortcode


@app.route('/', methods=['POST'])
def create_url():
    url = request.form['url']
    return actually_create_shortcode(url)


@app.route('/<shortcode>', methods=['GET'])
def follow_url(shortcode):
    cursor = g.db.execute(
        'select full_url from urls where hash=?',
        [shortcode]
    )
    g.db.commit()
    row = cursor.fetchone()
    return redirect(row[0])


if __name__ == '__main__':
    app.run()
