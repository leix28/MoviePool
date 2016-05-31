from flask import render_template, request
import db.db as db
import logging
import json

from . import app

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

@app.route('/api/resources/<id>')
def resources_api(id):
    return json.dumps(db.getMovieResources(id))
