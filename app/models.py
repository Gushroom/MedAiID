from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db

user_question = db.Table('user_question',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    responses_posted = db.relationship('Response')
    questions = db.relationship('Question', secondary=user_question, backref='users')

    def __repr__(self):
        return f"User('{self.name}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    responses = db.relationship('Response')

    def __repr__(self):
        return f"Question('{self.content}')"

    

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f"Response('{self.content}')"
    


