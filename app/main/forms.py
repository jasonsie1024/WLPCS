from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_login import current_user
from ..models import Message
from .. import db

class MessgeForm(FlaskForm):
    t = SelectField('Type', choices=[('light', 'Light'), ('primary', 'Primary'), ('success', 'Success'), ('warning', 'Warning'), ('danger', 'Danger')])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_submit(self, field):
        if not current_user.is_authenticated or current_user.id != 1:
            raise ValidationError('Only administrator can send message!')

