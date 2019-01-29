from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import MessgeForm
from ..models import Message
from .. import db

@main.route('/bulletin', methods = ['GET', 'POST'])
def bulletin():
    form = MessgeForm()
    if form.validate_on_submit():
        message = Message(t = form.t.data, content = form.content.data, create_time = datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        flash({
            't': form.t.data,
            'message': form.content.data,
            'create_time': datetime.utcnow()
        })
        return redirect(url_for('main.bulletin'))
    messages = Message.query.order_by(Message.create_time.desc()).all()
    print(messages)
    return render_template('bulletin.html', current_time = datetime.utcnow(), form = form, messages = messages)

@main.route('/ranking')
def ranking():
    return render_template('ranking.html', current_time = datetime.utcnow())