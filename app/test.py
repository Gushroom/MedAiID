from flask import Blueprint, jsonify, make_response, render_template
from . import db
from .models import User, Question, Response

test = Blueprint('test', __name__)

users = []
questions = []
responses = []

@test.route('/testinit')
def init():
    db.create_all()
    return "Initialized the database."

@test.route('/testadduser/<name>')
def adduser(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return "Added user " + name


@test.route('/testaddquestion/<content>')
def addquestion(content):
    question = Question(content=content)
    db.session.add(question)
    db.session.commit()
    return "Added question " + content

@test.route('/testaddresponse/<user>/<question>/<content>')
def addresponse(user, question, content):
    response = Response(content=content, user_id=user, question_id=question)
    db.session.add(response)
    db.session.commit()
    return "Added response " + content


@test.route('/testgetquestions')
def getquestions():
    questions = Question.query.all()
    return jsonify([question.content for question in questions])

@test.route('/testgetresponses/<question>')
def getresponses(question):
    responses = Response.query.filter_by(question_id=question).all()
    return jsonify([(response.content,response.user) for response in responses])