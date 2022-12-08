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
    return render_template('home.html', user = current_user)

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
    return render_template('profile.html', user = current_user)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_question():
    if current_user.role != 'medical professor':
        flash('You are not authorized to upload questions')
        return render_template('home.html', user = current_user)
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        new_question = Question(title=title, content=question)
        db.session.add(new_question)
        db.session.commit() 
    return render_template('upload.html')


@main.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    all_questions = Question.query.all()
    questions_answered = current_user.questions
    print(f"questions answered: {questions_answered}")
    unanswered_questions = []
    for question in all_questions:
        print(f"question: {question}")
        if question not in questions_answered:
            unanswered_questions.append(question)
    if not unanswered_questions:
        flash('No questions available')
        return render_template("home.html", user = current_user)
    return render_template('questions.html', questions = unanswered_questions)


@main.route('/question/<int:qid>', methods=['GET', 'POST'])
@login_required
def question(qid):
    selected_question = Question.query.filter_by(id=qid).first()
    if request.method == 'POST':
        # print(f"selected question: {selected_question}")
        diagnosis = request.form['Diagnosis']
        diag_conf = request.form['Diag_conf']
        tests = request.form['Tests']
        test_conf = request.form['Test_conf']
        interventions = request.form['Intervention']
        inter_conf = request.form['Interv_conf']
        if not diagnosis:
            flash("Please enter a diagnosis")
            return render_template('question.html', question = selected_question)
        if not tests:
            flash("Please enter a test")
            return render_template('question.html', question = selected_question)
        if not interventions:
            flash("Please enter an intervention")
            return render_template('question.html', question = selected_question)
        question_id = selected_question.id
        # print(f"question id: {question_id}")
        answerer_id = current_user.id
        new_response = Response(diagnosis=diagnosis, diag_conf=diag_conf, 
        tests=tests, test_conf=test_conf, interventions=interventions, inter_conf=inter_conf, 
        question_id=question_id, user_id=answerer_id)
        db.session.add(new_response)
        current_user.responses_posted.append(new_response)
        current_user.questions.append(selected_question)
        selected_question.responses.append(new_response)
        db.session.commit()
        print(f"question answered: {current_user.questions}")
        # add response to the current user
        flash(f"Response submitted to question {question_id}")
        return render_template('home.html', user = current_user)
    return render_template('questions.html', question = selected_question)


@main.route('/responses', methods=['GET', 'POST'])
@login_required
def responses():
    if current_user.role == 'medical professor':
        responses = Response.query.all()
        return(render_template('responses.html', responses = responses))
    responses = current_user.responses_posted
    return(render_template('responses.html', responses = responses, user = current_user))

@main.route('/responses/<int:uid>/<int:qid>', methods=['GET', 'POST'])
@login_required
def response(uid, qid):
    response = Response.query.filter_by(user_id=uid, question_id=qid).first()
    user = User.query.filter_by(id=uid).first()
    question = Question.query.filter_by(id=qid).first()
    return(render_template('responses.html', response = response, user = user, question = question))


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