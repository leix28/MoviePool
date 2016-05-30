from flask import Flask

app = Flask(__name__)

from . import route #make decorators work