from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField,DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    


class AddTransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Add Transaction')