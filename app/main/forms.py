from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf
from ..models import Message
from .. import db

class MessgeForm(FlaskForm):
    t = SelectField('Type', choices=[('light', 'Normal'), ('primary', 'Important'), ('success', 'Good'), ('danger', 'Danger'), ('warning', 'Warning')])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')