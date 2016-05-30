from flask import Flask, render_template, request
import db
import logging
import json

app = Flask(__name__)

@app.route('/')
def index():
    search = request.args.get('search')
    if search is None:
        return app.send_static_file('html/index.html')
    else:
        results = db.search(search, start=0, count=20)
        results = map(db.getDoubanBasic, results)
        return app.send_static_file('html/list.html')

@app.route('/movie/<id>')
def movie(id):
    return app.send_static_file('html/movie.html')

@app.route('/api/search')
def search_api():
    search = request.args.get('search')
    results = db.search(search, start=0, count=20)
    results = map(db.getDoubanBasic, results)
    results = filter(lambda x: not x is None, results)
    for item in results:
        del item['_id']
    return json.dumps(results)

@app.route('/api/movie/<id>')
def movie_api(id):
    return id
