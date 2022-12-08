from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db

user_question = db.Table('user_question',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
)

user_response = db.Table('user_response',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('response_id', db.Integer, db.ForeignKey('response.id'), primary_key=True)
)

question_response = db.Table('question_response',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
    db.Column('response_id', db.Integer, db.ForeignKey('response.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(100))
    responses_posted = db.relationship('Response')
    questions = db.relationship('Question', secondary=user_question, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"{self.name}"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    responses = db.relationship('Response')

    def __repr__(self):
        return f"{self.id}: {self.content}"

    

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(1000))
    diag_conf = db.Column(db.Integer)
    tests = db.Column(db.String(1000))
    test_conf = db.Column(db.Integer)
    interventions = db.Column(db.String(1000))
    inter_conf = db.Column(db.Integer)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f"Response to question {self.question_id}: Diagnosis: {self.diagnosis}, Tests: {self.tests}, Interventions: {self.interventions}, Confidence: {self.conf_level})"
    


