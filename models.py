from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary(255), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
