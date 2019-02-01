from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SubmitForm(FlaskForm):
    code = TextAreaField('Code')
    submit = SubmitField('Submit')