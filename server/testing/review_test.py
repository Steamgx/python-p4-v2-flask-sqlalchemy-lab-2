from app import app, db
from server.models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    @classmethod
    def setup_class(cls):
        '''Setup method to create the database tables.'''
        with app.app_context():
            db.create_all()

    @classmethod
    def teardown_class(cls):
        '''Teardown method to drop the database tables.'''
        with app.app_context():
            db.drop_all()

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        with app.app_context():
            c = Customer(name='Test Customer')
            i = Item(name='Test Item', price=10.00)
            db.session.add_all([c, i])
            db.session.commit()
            
            r = Review(comment='great!', customer=c, item=i)  # Updated line
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns
            c = Customer(name='Test Customer')
            i = Item(name='Test Item', price=10.00)
            db.session.add_all([c, i])
            db.session.commit()
            
            r = Review(comment='great!', customer=c, item=i)  # Updated line
            db.session.add(r)
            db.session.commit()
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)  # Updated line
            db.session.add(r)
            db.session.commit()

            # check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
