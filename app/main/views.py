from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from markdown import markdown
from . import main
from .forms import MessgeForm, SettingForm
from ..models import Message, Setting
from .. import db

@main.route('/', methods = ['GET', 'POST'])
def home():
    form = SettingForm()
    if form.validate_on_submit():
        about = Setting.get_or_create(setting = 'about')
        about.value = form.about.data
        db.session.commit()

        schedule = Setting.get_or_create(setting = 'schedule')
        schedule.value = form.schedule.data
        db.session.commit()

        return redirect(url_for('main.home'))

    about = form.about.data = Setting.get_or_create(setting = 'about').value
    schedule = form.schedule.data = Setting.get_or_create(setting = 'schedule').value
    about = markdown(about, output_format = 'html')
    schedule = markdown(schedule, output_format = 'html')

    return render_template('home.html', current_time = datetime.utcnow(), form = form, about = about, schedule = schedule)

@main.route('/bulletin', methods = ['GET', 'POST'])
def bulletin():
    form = MessgeForm()
    if form.validate_on_submit():
        message = Message(t = form.t.data, content = form.content.data, create_time = datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.bulletin'))
    messages = Message.query.order_by(Message.create_time.desc()).all()
    return render_template('bulletin.html', current_time = datetime.utcnow(), form = form, messages = messages)

@main.route('/ranking')
def ranking():
    return render_template('ranking.html', current_time = datetime.utcnow())