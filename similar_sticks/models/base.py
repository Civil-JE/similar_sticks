from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_database():
    db.create_all()
