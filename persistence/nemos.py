from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Nemo(db.Model):
    __tablename__ = 'nemos'

    id = db.Column(db.Integer, primary_key=True)
    nemo = db.Column(db.String(50), nullable=False)
    lastPrice = db.Column(db.String(50), nullable=False, default="0.0")
    registerDateTime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Nemo('{self.nemo}', '{self.lastPrice}', '{self.registerDateTime}')"


# Translates a SQLAlchemy model instance into a dictionary
def from_sql(row):
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# To run first time and create database and table
def create_database(app):
    db.init_app(app)
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("All tables created")


def list():
    return list(map(from_sql, Nemo.query.all()))


def read(id):
    result = Nemo.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    nemo = Nemo(**data)
    db.session.add(nemo)
    db.session.commit()
    return from_sql(nemo)


def update(data, id):
    nemo = Nemo.query.get(id)
    for k, v in data.items():
        setattr(nemo, k, v)
    db.session.commit()
    return from_sql(nemo)


def delete(id):
    Nemo.query.filter_by(id=id).delete()
    db.session.commit()


if __name__ == '__main__':
    create_database()
