from app import app, db
from server.models import Customer, Item, Review

class TestAssociationProxy:
    '''Customer in models.py'''

    @classmethod
    def setup_class(cls):
        '''Setup method to create the database tables.'''
        with app.app_context():
            db.create_all()

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items
