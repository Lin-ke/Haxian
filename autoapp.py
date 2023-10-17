# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from conduit.app import create_app
from conduit.config import Config

app = create_app(Config)

@app.route("/")
def hello():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsIm5hbWUiOiJ3ZWl5dXBlbmciLCJleHAiOjE2OTc2MjAwMjF9.6SCiGkpOGSay44pZzPw1DOCKRnyI_-EmRAAd5zelWZY"