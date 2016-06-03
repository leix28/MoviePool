from flask import Flask

app = Flask(__name__)

from . import route #make decorators work

from db import downloader

@app.before_first_request
def application_initialize():
    downloader.initDownloader()