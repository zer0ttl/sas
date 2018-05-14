from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class SetForm(FlaskForm):
    to_account = StringField('To Account', validators=[DataRequired()])
    amount = IntegerField('Number of Points', validators=[DataRequired()])
    submit = SubmitField('Update Details')


class BurnForm(FlaskForm):
    from_account = StringField('From Account', validators=[DataRequired()])
    amount = IntegerField('Points to be Redeemed', validators=[DataRequired()])
    submit = SubmitField('Update Details')