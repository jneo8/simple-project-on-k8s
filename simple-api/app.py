# coding: utf-8

import datetime
import platform

from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    hostname = platform.node()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return f'You hit "{hostname}" at {now}, path: {request.path}'


@app.route('/health')
def hello():
    return 'OK'


@app.errorhandler(404)
def page_not_found(exc):
    return f'Page not found: {request.path}', 404
