from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class NewProblemField(FlaskForm):
    title = StringField('Title', [DataRequired()])
    abbr = StringField('Abbr.', [DataRequired()])
    submit = SubmitField('Create')

    def validate_submit(self, field):
        if current_user.id != 1:
            raise ValidationError('Forbidden!')

class ProblemField(FlaskForm):
    title = StringField('Title', [DataRequired()])
    abbr = StringField('Abbr', [DataRequired()])
    content = TextAreaField('Content')
    submit = SubmitField('Update')