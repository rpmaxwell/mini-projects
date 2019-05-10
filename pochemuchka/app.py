# app.py
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect, generate_csrf


app = Flask(__name__)
app.config.from_object(BaseConfig)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)
csrf.init_app(app)


from questions import question_list
from models import *

@app.route('/', methods=['GET', 'POST'])
def home():
    print(request.form)
    try:
        question_section = int(request.form['question_no'])
    except KeyError:
        question_section = 0
    print(question_section)
    validator = eval("EarningsQuestion{}".format(question_section))
    form = validator(request.form)
    if request.method == 'POST':
        return render_template('chart.html', form=form, questions=question_list['earnings'][question_section])
    return render_template('chart.html', form=form, questions=question_list['earnings'][question_section])


def get_new_salary(salary_amount):
    new_ranges = [[i[0], i[1]+salary_amount, i[2]+salary_amount] for i in ranges]
    new_averages = [[i[0], i[1]+salary_amount] for i in averages]
    return new_ranges, new_averages


if __name__ == '__main__':
    app.run()
