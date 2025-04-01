from app import app, db
from server.models import Customer, Item, Review

class TestSerialization:
    '''models in models.py'''

    @classmethod
    def setup_class(cls):
        '''Setup method to create the database tables.'''
        with app.app_context():
            db.create_all()

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            i = Item(name='Laptop')  # Ensure an item exists
            db.session.add(i)
            db.session.commit()
            r = Review(comment='great!', customer=c, item=i)  # Assign an item
            db.session.add(r)
            db.session.commit()
            customer_dict = c.to_dict()

            assert customer_dict['id']
            assert customer_dict['name'] == 'Phil'
            assert customer_dict['reviews']
            assert 'customer' not in customer_dict['reviews']

    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            c = Customer(name='Phil')  # Ensure a customer exists
            db.session.add(c)
            db.session.commit()
            r = Review(comment='great!', customer=c, item=i)  # Assign both customer and item
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()
            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert item_dict['reviews']
            assert 'item' not in item_dict['reviews']

    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()
            assert review_dict['id']
            assert review_dict['customer']['id'] == c.id  # Check customer_id directly
            assert review_dict['item']['id'] == i.id
            assert review_dict['comment'] == 'great!'
            assert 'reviews' not in review_dict['customer']
            assert 'reviews' not in review_dict['item']
