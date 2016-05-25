from flask import Flask, render_template, request
import db
import logging

app = Flask(__name__)

@app.route('/')
def hello_word():
    search = request.args.get('search')
    if search is None:
        return render_template('index.html')
    else:
        results = db.search(search, start=0, count=20)
        results = map(db.getDoubanBasic, results)
        return render_template('list.html', results=results)
