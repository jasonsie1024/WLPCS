from flask import render_template, redirect, url_for
from datetime import datetime
from . import problem
from .forms import NewProblemField, ProblemField
from ..models import Problem
from .. import db

@problem.route('/problems', methods = ['GET', 'POST'])
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
    return render_template('problem/show.html', current_time = datetime.utcnow(), form = form, problem = problem)