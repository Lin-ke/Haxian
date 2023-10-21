# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from flask import render_template
from conduit.app import create_app
from conduit.config import Config

app = create_app(Config)

@app.route("/")
def hello():
    return render_template('index.html')
    #return "Hi, this is Haxian! We are Hiters, nice to meet you!"