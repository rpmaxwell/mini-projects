from wtforms import Form, BooleanField, DateField, StringField, SelectField, PasswordField, IntegerField, validators
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class EarningsPage1(Form):
	gender = SelectField('gender', choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other'), ('n', 'I\'d prefer not to say')], render_kw={"class": "col-md-6"})
	martial_status = SelectField('marital', choices=[('s', 'Single'), ('m', 'Married'), ('d', 'Divorced')], render_kw={"class": "col-md-6"})
	birthday = IntegerField('Birth Day', [validators.NumberRange(min=1, max=31)], render_kw={"placeholder": "DD", "class": "col-md-4"})
	birthmonth = IntegerField('Birth Month', [validators.NumberRange(min=1, max=12)], render_kw={"placeholder": "MM", "class": "col-md-4"})
	birthyear = IntegerField('Birth Year', [validators.NumberRange(min=1940, max=2000)], render_kw={"placeholder": "YYYY", "class": "col-md-4"})


class EarningsPage2(Form):
	income_source = SelectField('Income Source', choices=[('s', 'Salary'), ('sg', 'Side Gig'), ('i', 'Investment'), ('o', 'Other')])
	current_salary = IntegerField('Annual Salary', [validators.NumberRange(min=0, max=5000000)])


	