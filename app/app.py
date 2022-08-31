from flask import Flask

from config import Configuration

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_login import LoginManager

from flask_mail import Mail





app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)

mail = Mail(app)

login_manager = LoginManager(app)

from models import *
migrate = Migrate(app, db)

