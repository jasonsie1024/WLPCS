from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from . import problem
from .forms import NewProblemField, ProblemField, TestDataField
from ..models import Problem, TestData
from .. import db

@problem.route('/problems', methods = ['GET', 'POST'])
@login_required
def problems():
    form = NewProblemField()
    if form.validate_on_submit():
        problem = Problem(abbr = form.abbr.data, title = form.title.data)
        db.session.add(problem)
        db.session.commit()
        return redirect(url_for('problem.show', pid = problem.id))
    problems = Problem.query.order_by(Problem.id).all()
    return render_template('problem/problems.html', current_time = datetime.utcnow(), form = form, problems = problems)

@problem.route('/problems/<pid>', methods = ['GET', 'POST'])
@login_required
def show(pid):
    form = ProblemField()
    problem = Problem.query.get_or_404(pid)
    if form.validate_on_submit():
        problem.abbr = form.abbr.data
        problem.title = form.title.data
        problem.content = form.content.data
        db.session.add(problem)
        db.session.commit()
        return redirect(url_for('problem.show', pid = pid))
    form.abbr.data = problem.abbr
    form.title.data = problem.title
    form.content.data = problem.content
    testdata = TestData.query.filter_by(pid = pid).all()
    return render_template('problem/show.html', current_time = datetime.utcnow(), form = form, problem = problem, testdata = testdata)

@problem.route('/problems/<pid>/new_testdata')
@login_required
def new_testdata(pid):
    testdata = TestData(pid = pid)
    db.session.add(testdata)
    db.session.commit()
    return redirect(url_for('problem.testdata', tid = testdata.id))

@problem.route('/problems/testdata/<tid>', methods = ['GET', 'POST'])
@login_required
def testdata(tid):
    form = TestDataField()
    testdata = TestData.query.get_or_404(tid)
    if form.validate_on_submit():
        testdata.score = form.score.data
        testdata.input = form.inputs.data
        testdata.answer = form.answers.data
        testdata.time_limit = form.time_limit.data
        testdata.memory_limit = form.memory_limit.data
        db.session.add(testdata)
        db.session.commit()

        problem = Problem.query.get_or_404(testdata.pid)
        testdatas = TestData.query.filter_by(pid = testdata.pid).all()
        problem.total_score = 0
        for data in testdatas:
            problem.total_score += data.score
        db.session.add(problem)
        db.session.commit()

        return redirect(url_for('problem.show', pid = testdata.pid))

    form.score.data = testdata.score
    form.inputs.data = testdata.input
    form.answers.data = testdata.answer
    form.time_limit.data = testdata.time_limit
    form.memory_limit.data = testdata.memory_limit
    return render_template('problem/testdata.html', current_time = datetime.utcnow(), form = form)