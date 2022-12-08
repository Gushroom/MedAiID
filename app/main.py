from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Question, Response
from werkzeug.security import generate_password_hash, check_password_hash
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('about.html')

@main.route('/home')
@login_required
def home():
    return render_template('home.html', name = current_user.name)

@main.route('/profile/password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pass = request.form['old_password']
        new_pass = request.form['new_password']
        new_pass_repeat = request.form['repeat_password']
        if not check_password_hash(current_user.password, old_pass):
            flash('Passwords do not match')
            return render_template('changepass.html')
        if new_pass != new_pass_repeat:
            flash('Passwords do not match')
            return render_template('changepass.html')
        new_pass_hash = generate_password_hash(new_pass, method='sha256')
        current_user.password = new_pass_hash
        db.session.commit()
        return render_template('home.html')
    return render_template('changepass.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', name = current_user.name, email = current_user.email)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
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
    questions = Question.query.all()
    if not questions:
        message = "No questions available"
        return render_template('question.html', questions = questions, message = message)
    selected_index = random.choice(range(len(questions)))
    selected_question = questions[selected_index]
    selected_question_object = Question.query.filter_by(id=selected_question.id).first()
    if request.method == 'GET':
        return render_template('question.html', question = selected_question)
    if request.method == 'POST':
        diagnosis = request.form['Diagnosis']
        tests = request.form['Tests']
        intervetions = request.form['Intervetion']
        question_id = selected_question.id
        answerer_id = current_user.id
        confidece = request.form['confidence']
        print(f"Diagnosis: {diagnosis}, Tests: {tests}, Interventions: {intervetions}, Question ID: {question_id}, Answerer ID: {answerer_id}")
        new_response = Response(diagnosis=diagnosis, tests=tests, interventions=intervetions, conf_level=confidece, question_id=question_id, user_id=answerer_id)
        # curr_user = User.query.filter_by(id=answerer_id).first()
        # curr_user.responses_posted.append(new_response)
        db.session.add(new_response)
        current_user.responses_posted.append(new_response)
        current_user.questions.append(selected_question)
        selected_question_object.responses.append(new_response)
        db.session.commit()
        # add response to the current user

    return(render_template('question.html', question = selected_question))


# @main.route('/question/<int:question_id>', methods=['GET', 'POST'])
# @login_required
# def question(question_id):
#     question = Question.query.filter_by(id=question_id).first()
#     return render_template('question.html', question=question)

# @main.route('/view/question', methods=['GET', 'POST'])
# def view():
#     if request.method == 'POST':
#         response = request.form.get('response')
#         question_id = request.form.get('question_id')
#         new_response = Response(response=response, question_id=question_id)
#         db.session.add(new_response)
#         db.session.commit()
#     return render_template('question.html')

# @main.route('/question', methods=['POST'])
# @login_required
# def question():
#     question = request.form.get('question')
#     new_question = Question(question=question, user_id=current_user.id)
#     db.session.add(new_question)
#     db.session.commit() 
#     return render_template('question.html')