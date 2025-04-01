from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.id for review in self.reviews]  # Include reviews in serialization
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    customer = db.relationship('Customer', backref='reviews')
    item = db.relationship('Item', backref='reviews')

    def __init__(self, comment, customer=None, item=None):
        self.comment = comment
        if customer is not None:
            self.customer = customer
        if item is not None:
            self.item = item

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': {'id': self.customer.id, 'name': self.customer.name} if self.customer else None,
            'item': {'id': self.item.id, 'name': self.item.name, 'price': self.item.price} if self.item else None
        }

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.id for review in self.reviews]  # Include reviews in serialization
        }
