from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary(255), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(32), nullable=False)


class Products(db.Model):
    __tablename__ = 'products.products'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary(255), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

class SaleOrders(db.Model):
    __tablename__ = 'sale_orders.sale_orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    customer = db.relationship('Customer', backref=db.backref('sale_orders', lazy=True))