from flask_sqlalchemy import SQLAlchemy
from models.base import Base

db = SQLAlchemy(model_class=Base)

def init_db(app):
    db.init_app(app)