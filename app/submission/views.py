from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime
from hashlib import md5
from .forms import SubmitForm
from . import submission
from .. import db
from ..models import Submission, User, Problem, TestData

@submission.route('/submissions')
def list():
    page = request.args.get('page', 1, type=int)
    pagination = Submission.query.order_by(Submission.id.desc()).paginate(page, per_page = current_app.config['ITEMS_PER_PAGE'], error_out=True)
    submissions = pagination.items
    problems = Problem
    user = User
    return render_template('submissions/list.html', current_time = datetime.utcnow(), submissions = submissions, pagination = pagination, user = user, problems = problems)

@submission.route('/<uid>/submissions')
def list_by_user(uid):
    page = request.args.get('page', 1, type=int)
    pagination = Submission.query.order_by(Submission.id.desc()).filter_by(uid = uid).paginate(page, per_page = current_app.config['ITEMS_PER_PAGE'], error_out = True)
    submissions = pagination.items
    problems = Problem
    user = User.query.get_or_404(uid)
    return render_template('submissions/list_by_user.html', current_time = datetime.utcnow(), submissions = submissions, pagination = pagination, user = user, problems = problems)

@submission.route('/submissions/<sid>')
def result(sid):
    submission = Submission.query.get_or_404(sid)
    problem = Problem.query.get(submission.pid)
    testdata = TestData.query.filter_by(pid = submission.pid)
    user = User.query.get(submission.uid)

    return render_template('submissions/result.html', current_time = datetime.utcnow(), submission = submission, user = user, problem = problem, testdata = testdata)

@submission.route('/problems/<pid>/submit', methods = ['GET', 'POST'])
@login_required
def submit(pid):
    form = SubmitForm()
    if form.validate_on_submit():
        submission = Submission(pid = pid, uid = current_user.id, code = form.code.data, create_time = datetime.utcnow(), verdict = 'Pending')
        db.session.add(submission)
        db.session.commit()
        
        return redirect(url_for('submission.result', sid = submission.id))
    problem = Problem.query.get_or_404(pid)
    return render_template('submissions/submit.html', current_time = datetime.utcnow(), form = form, pid = pid, problem = problem)