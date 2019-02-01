from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .forms import SigninForm, SignupForm, SettingForm
from ..models import User
from .. import db
from . import auth

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember = True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            flash('Signed in successfully!')
            return redirect(next)
        flash('Invalid email or password!')
    return render_template('auth/signin.html', current_time = datetime.utcnow(), form = form)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    flash('Signed out successfully!')
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email = form.email.data.lower(), username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Signed up successfully!')
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('auth/signup.html', current_time = datetime.utcnow(), form = form)

@auth.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        print(form.username.data)
        current_user.username = form.username.data
        current_user.password = form.password.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Updated successfully!')
        return redirect(url_for('main.home'))
    form.username.data = current_user.username
    return render_template('auth/settings.html', current_time = datetime.utcnow(), form = form)