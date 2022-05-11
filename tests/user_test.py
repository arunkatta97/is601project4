import logging

from app import db
from app.db.models import User, Song, Transaction
from faker import Faker
from sqlalchemy.sql import functions


def test_adding_user(application):
    # log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        # showing how to add a record
        # create a record
        user = User('keith@webizly.com', 'testtest')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        db.session.commit()
        # assert that we now have a new user
        assert user.email == 'keith@webizly.com'
        assert db.session.query(User).count() == 1

def test_checin_user(application):
            # log = logging.getLogger("myApp")
    with application.app_context():
        # finding one user record by email
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email='keith@webizly.com').first()
        # log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'

def test_transaction_add(application):
    with application.app_context():
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        user.transactions = [Transaction(4000,"CREDIT"), Transaction(-2000,"DEBIT")]
        db.session.commit()
        assert db.session.query(Transaction).count() == 2

def test_accessing_transaction(application):
    with application.app_context():
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        user.transactions = [Transaction(4000, "CREDIT"), Transaction(-2000, "DEBIT")]
        transaction1 = Transaction.query.filter_by(amount=4000).first()
        db.session.commit()
        assert transaction1.amount == 4000
        assert transaction1.type == "CREDIT"

def test_changing_transaction_mount(application):
    with application.app_context():
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        user.transactions = [Transaction(4000, "CREDIT"), Transaction(-2000, "DEBIT")]
        transaction1 = Transaction.query.filter_by(amount=4000).first()
        db.session.commit()
        transaction1.amount = 5000
        assert transaction1.amount == 5000

def test_balance(application):
    with application.app_context():
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        user.transactions = [Transaction(4000, "CREDIT"), Transaction(-2000, "DEBIT")]
        transaction1 = Transaction.query.filter_by(amount=4000).first()
        db.session.commit()
        balance =  db.session.query(functions.sum(Transaction.amount)).scalar()
        assert balance == 2000

def test_balance_after_changing_transaction_amount(application):
            with application.app_context():
                user = User('keith@webizly.com', 'testtest')
                db.session.add(user)
                db.session.commit()
                user.transactions = [Transaction(4000, "CREDIT"), Transaction(-2000, "DEBIT")]
                transaction1 = Transaction.query.filter_by(amount=4000).first()
                db.session.commit()
                transaction1.amount = 5000
                assert transaction1.amount == 5000
                balance = db.session.query(functions.sum(Transaction.amount)).scalar()
                assert balance == 3000






        #
        # # changing the title of the song
        # song1.title = "SuperSongTitle"
        # # saving the new title of the song
        # db.session.commit()
        # song2 = Song.query.filter_by(title='SuperSongTitle').first()
        # assert song2.title == "SuperSongTitle"
        # # checking cascade delete
        # db.session.delete(user)
        # assert db.session.query(User).count() == 0
        # assert db.session.query(Song).count() == 0
