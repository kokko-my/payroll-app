# flaskr/__init__.py
import os
from flask import Flask


basedir = os.path.abspath(os.path.dirname(__name__))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'myapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from flaskr.views import bp
    app.register_blueprint(bp)
    return app
