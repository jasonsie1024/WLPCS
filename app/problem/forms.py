from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, SubmitField, TextAreaField, IntegerField
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
    scoring_script = TextAreaField('Scoring Script')
    submit = SubmitField('Update')

    def validate_submit(self, field):
        if current_user.id != 1:
            raise ValidationError('Forbidden!')

class TestDataField(FlaskForm):
    inputs = TextAreaField('Inputs')
    answers = TextAreaField('Outputs')
    time_limit = IntegerField('Time Limit (ms)')
    memory_limit = IntegerField('Memory Limit (KiB)')
    score = IntegerField('Score')
    submit = SubmitField('Save')

    def validate_submit(self, field):
        if current_user.id != 1:
            raise ValidationError('Forbidden!')