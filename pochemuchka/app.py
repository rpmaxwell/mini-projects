# app.py
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect, generate_csrf
import connector



app = Flask(__name__)
app.config.from_object(BaseConfig)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)
csrf.init_app(app)

conn = connector.DBConn('gameplan_db', 'pochemuchka')

from questions import question_list
from models import *


@app.route('/', methods=['GET', 'POST'])
def home():
    print(request.form)
    if 'question_no' in request.form.keys():
        question_section = int(eval(request.form['question_no']))
        record_response(request.form)
    else:
        question_section = 0
    print(request)
    validator = eval("EarningsQuestion{}".format(question_section))
    form = validator(request.form)
    if request.method == 'POST':
        return render_template('chart.html', form=form, questions=question_list['earnings'][question_section])
    return render_template('chart.html', form=form, questions=question_list['earnings'][question_section])


def get_new_salary(salary_amount):
    new_ranges = [[i[0], i[1]+salary_amount, i[2]+salary_amount] for i in ranges]
    new_averages = [[i[0], i[1]+salary_amount] for i in averages]
    return new_ranges, new_averages


def record_response(response):
    row = response.to_dict()
    q = """
    INSERT INTO
                pochemuchka.responses
    (question_id, subject_id, user_id, response, response_dt)
    VALUES (
        :question_id
        ,:subject_id
        ,:user_id
        ,:response
        ,CURRENT_TIMESTAMP
    )
    """
    conn.execute(q, params=row)
    return 'OK'



if __name__ == '__main__':
    app.run()
