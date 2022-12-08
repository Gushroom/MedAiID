from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Question, Response
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)

@main.route('/question', methods=['POST'])
@login_required
def question():
    question = request.form.get('question')
    new_question = Question(question=question, user_id=current_user.id)
    db.session.add(new_question)
    db.session.commit() 
    return render_template('question.html')

@main.route('/view/question', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        response = request.form.get('response')
        question_id = request.form.get('question_id')
        new_response = Response(response=response, question_id=question_id)
        db.session.add(new_response)
        db.session.commit()
    return render_template('question.html')

@main.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload_question():
    if request.method == 'POST':
        question = request.form['question']
        new_question = Question(content=question)
        db.session.add(new_question)
        db.session.commit() 
    return render_template('upload.html')


@main.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    if request.method == 'GET':
        questions = Question.query.all()
        selected_question = random.choice(questions)
        return render_template('question.html', question = selected_question)
    # if request.method == 'POST':
    #     response = request.form.get('response')
    #     question_id = request.form.get('question_id')
    #     new_response = Response(response=response, question_id=question_id)
    #     db.session.add(new_response)
    #     db.session.commit()


# @main.route('/question/<int:question_id>', methods=['GET', 'POST'])
# @login_required
# def question(question_id):
#     question = Question.query.filter_by(id=question_id).first()
#     return render_template('question.html', question=question)

