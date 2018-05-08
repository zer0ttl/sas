from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class SetForm(FlaskForm):
    instructor_name = StringField('Instructor Name', validators=[DataRequired()])
    instructor_age = IntegerField('Instructor Age', validators=[DataRequired()])
    submit = SubmitField('Update Details')