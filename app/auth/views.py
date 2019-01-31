from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .forms import SigninForm, SignupForm
from ..models import User
from .. import db
from . import auth

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember = True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            flash({'t': 'success', 'message': 'Signed in successfully!', 'create_time': datetime.utcnow()})
            return redirect(next)
        flash({'t': 'danger', 'message': 'Invalid email or password!', 'create_time': datetime.utcnow()})
    return render_template('auth/signin.html', current_time = datetime.utcnow(), form = form)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    flash({'t': 'success', 'message': 'Signed out successfully!', 'create_time': datetime.utcnow()})
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email = form.email.data.lower(), username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash({'t': 'success', 'message': 'Signed up successfully!', 'create_time': datetime.utcnow()})
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('auth/signup.html', current_time = datetime.utcnow(), form = form)