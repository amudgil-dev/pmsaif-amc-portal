from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField,DateField, IntegerField,EmailField,HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email,NumberRange,InputRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    


class AddTransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Add Transaction')
    


# Create a dummy form
class DummyForm(FlaskForm):
    pass

# create a Sign up Form class

class SignupForm(FlaskForm):
  fname = StringField("First Name", validators=[DataRequired(), Length(min=1, max=50)])
  lname = StringField("Last Name", validators=[DataRequired(), Length(min=1, max=50)])  
  email = EmailField("Email", validators=[DataRequired(), Email()])
#   password_hash = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=10), EqualTo('password_hash2', message='Passwords Must Match!')])
#   password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
  submit = SubmitField("Submit")

  # create a SignIn Form class
class SigninForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Email()])
  password_hash = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Submit")



class ResetRequestForm(FlaskForm):
  email = EmailField("Type your Registered Email below", validators=[DataRequired(), Email()])
  submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
  token = HiddenField("token")
  password_hash = PasswordField("New Password", validators=[DataRequired(), Length(min=5, max=10), EqualTo('password_hash2', message='Passwords Must Match!')])
  password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
  submit = SubmitField("Submit")


class PMSPerformanceForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    user_id = IntegerField('User ID')
    p_month = IntegerField('Performance Month')
    p_year = IntegerField('Performance Year')
    
    one_month = FloatField('One Month *')
    three_months = FloatField('Three Months', validators=[Optional()])
    six_months = FloatField('Six Months', validators=[Optional()])
    twelve_months = FloatField('Twelve Months', validators=[Optional()])
    two_year_cagr = FloatField('Two Year CAGR', validators=[Optional()])
    three_year_cagr = FloatField('Three Year CAGR', validators=[Optional()])
    five_year_cagr = FloatField('Five Year CAGR', validators=[Optional()])
    ten_year_cagr = FloatField('Ten Year CAGR', validators=[Optional()])
    cagr_si = FloatField('CAGR Since Inception *')
    si = FloatField('Benchmark SI *')
    submit = SubmitField("Sumit Performance")


class PMSPerformanceEditForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    user_id = IntegerField('User ID')
    p_month = IntegerField('Performance Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    p_year = IntegerField('Performance Year', validators=[DataRequired(), NumberRange(min=2023, max=2026)])
    
    one_month = FloatField('One Month *')
    three_months = FloatField('Three Months', validators=[Optional()])
    six_months = FloatField('Six Months', validators=[Optional()])
    twelve_months = FloatField('Twelve Months', validators=[Optional()])
    two_year_cagr = FloatField('Two Year CAGR', validators=[Optional()])
    three_year_cagr = FloatField('Three Year CAGR', validators=[Optional()])
    five_year_cagr = FloatField('Five Year CAGR', validators=[Optional()])
    ten_year_cagr = FloatField('Ten Year CAGR', validators=[Optional()])
    cagr_si = FloatField('CAGR Since Inception *')
    si = FloatField('Benchmark SI *')
        
    submit = SubmitField("Confirm Change")


class StockSearchForm(FlaskForm):
    stock_query = StringField('Stock Query', validators=[InputRequired()])



class PMSStocksForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    stock_id = IntegerField('Stock ID')
    pct_deployed = FloatField('% Deployed', validators=[DataRequired()])
    submit = SubmitField("Create")

class PMSSectorsForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    sector_id = IntegerField('Sector ID')
    pct_deployed = FloatField('% Deployed', validators=[DataRequired()])
    submit = SubmitField("Create")

class SectorSearchForm(FlaskForm):
    sector_query = StringField('Sector Query', validators=[InputRequired()])



class PMSMasterEditForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    amc_id = IntegerField('AMC ID')
    pms_name = StringField('PMS Name')
    index_id = IntegerField('Index ID')
    # aum = FloatField('AUM - Cr.', validators=[DataRequired()])
    aum = FloatField('AUM - Cr.', validators=[NumberRange(min=0, max=99999, message='In Cr.')])    
    stocks_min = IntegerField('Stocks Min', validators=[Optional() ,NumberRange(min=0)])
    stocks_max = IntegerField('Stocks Max', validators=[Optional() ,NumberRange(min=0)])
    
    portfolio_pe = FloatField('Portfolio PE', validators=[Optional() ])
    large_cap = FloatField('Large Cap Percent', validators=[Optional() ,NumberRange(min=0.0)]) 
    mid_cap = FloatField('Mid Cap Percent', validators=[Optional() ,NumberRange(min=0.0)])  
    small_cap = FloatField('Small Cap Percent', validators=[Optional() ,NumberRange(min=0.0)])
    cash = FloatField('Cash Percent', validators=[Optional() ,NumberRange(min=0.0)])
    
    created_at = DateField('Created At')
    submit = SubmitField("Change")


    
class IndexPerformanceForm1(FlaskForm):
    user_id = IntegerField('User ID')
    index_id = IntegerField('Index ID')
    p_month = IntegerField('Performance Month')
    p_year = IntegerField('Performance Year')
    
    one_month = FloatField('One Month *', validators=[NumberRange(min=0.0)])
    three_months = FloatField('Three Months', validators=[Optional(),NumberRange(min=0.0)])
    six_months = FloatField('Six Months', validators=[Optional(),NumberRange(min=0.0)])
    twelve_months = FloatField('Twelve Months', validators=[Optional(),NumberRange(min=0.0)])
    two_year_cagr = FloatField('Two Year CAGR', validators=[NumberRange(min=0.0)])
    three_year_cagr = FloatField('Three Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    five_year_cagr = FloatField('Five Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    ten_year_cagr = FloatField('Ten Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    # cagr_si = FloatField('CAGR Since Inception', validators=[NumberRange(min=0.0)])
    
    submit = SubmitField("Create")

class IndexPerformanceForm(FlaskForm):
    user_id = IntegerField('User ID')
    index_id = IntegerField('Index ID')
    p_month = IntegerField('Performance Month')
    p_year = IntegerField('Performance Year')
    
    one_month = FloatField('One Month *', validators=[NumberRange(min=0.0)])
    three_months = FloatField('Three Months', validators=[Optional(),NumberRange(min=0.0)])
    six_months = FloatField('Six Months', validators=[Optional(),NumberRange(min=0.0)])
    twelve_months = FloatField('Twelve Months', validators=[Optional(),NumberRange(min=0.0)])
    two_year_cagr = FloatField('Two Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    three_year_cagr = FloatField('Three Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    five_year_cagr = FloatField('Five Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    ten_year_cagr = FloatField('Ten Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    submit = SubmitField("Create")


class IndexPerformanceEditForm(FlaskForm):
    
    user_id = IntegerField('User ID')
    index_id = IntegerField('Index ID')
    p_month = IntegerField('Performance Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    p_year = IntegerField('Performance Year', validators=[DataRequired(), NumberRange(min=2023, max=2026)])
    
    one_month = FloatField('One Month', validators=[Optional(), NumberRange(min=0.0)])
    three_months = FloatField('Three Months', validators=[Optional(),NumberRange(min=0.0)])
    six_months = FloatField('Six Months', validators=[Optional(),NumberRange(min=0.0)])
    twelve_months = FloatField('Twelve Months', validators=[Optional(),NumberRange(min=0.0)])
    two_year_cagr = FloatField('Two Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    three_year_cagr = FloatField('Three Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    five_year_cagr = FloatField('Five Year CAGR', validators=[Optional(),NumberRange(min=0.0)])
    ten_year_cagr = FloatField('Ten Year CAGR', validators=[Optional(),NumberRange(min=0.0)])

    
    submit = SubmitField("Confirm Change")
    


class PMSNavForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    user_id = IntegerField('User ID')
    p_month = IntegerField('NAV Month')
    p_year = IntegerField('NAV Year')
    
    nav = FloatField('NAV *', validators=[NumberRange(min=0.0)])

    submit = SubmitField("Create")
    
class PMSNavEditForm(FlaskForm):
    pms_id = IntegerField('PMS ID')
    user_id = IntegerField('User ID')
    p_month = IntegerField('NAV Month')
    p_year = IntegerField('NAV Year')
    
    nav = FloatField('NAV *', validators=[NumberRange(min=0.0)])

    submit = SubmitField("Edit")
    

# Form for editing NAV entries
class NavForm(FlaskForm):
    nav = FloatField('NAV Value', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
    

##### Test Form here   ####


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    