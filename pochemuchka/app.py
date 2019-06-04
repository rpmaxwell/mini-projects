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

from models import *
import pandas as pd


def get_questions(page_id):
    q = """   
    SELECT
            q.question_id
            ,q.page_id
            ,q.prompt
    FROM
            pochemuchka.question q
    WHERE
            q.page_id = :page_id
    """
    questions = conn.execute(q, params={'page_id': page_id}, fmt='dict')
    return questions

def get_current_page(user_id):
    q = """
    SELECT
            COALESCE(MAX(q.page_id), 1) page_id
    FROM 
            pochemuchka.user u
    LEFT JOIN
            pochemuchka.response r
        ON r.user_id = u.user_id  
    LEFT JOIN
            pochemuchka.prompt p 
        ON p.prompt_id = r.prompt_id
    LEFT JOIN
            pochemuchka.question q 
        ON q.question_id = p.prompt_id
    WHERE
            u.user_id=1
    """
    current_page = conn.execute(q, params={'user_id': user_id}, fmt='dict')
    return current_page[0]['page_id']


def get_prompts(page_id):
    q = """
    SELECT
        q.question_id
        ,p.prompt_id
        ,p.response_type
        ,p.validation
        ,p.placeholder
        ,p.prompt_name
        
    FROM
            pochemuchka.question q
    JOIN
            pochemuchka.prompt p
        ON q.question_id=p.question_id
    WHERE
            q.page_id=:page_id
    """
    prompts = conn.execute(q, params={'page_id': page_id}, fmt='dict')
    return prompts


@app.route('/', methods=['GET', 'POST'])
def home():
    user_id = 1
    if request.method == 'POST':
        record_response(request.form)
    current_page = get_current_page(user_id)
    questions = get_questions(current_page)
    prompts = get_prompts(current_page)
    validator = eval('EarningsPage{}'.format(current_page))
    form = validator(request.form)
    return render_template('chart.html', form=form, questions=questions, prompts=prompts, user_id=user_id)


def get_new_salary(salary_amount):
    new_ranges = [[i[0], i[1]+salary_amount, i[2]+salary_amount] for i in ranges]
    new_averages = [[i[0], i[1]+salary_amount] for i in averages]
    return new_ranges, new_averages



def record_response(response):
    response_row = response.to_dict()
    print(response_row)
    prompts = get_prompts(response_row['page_id'])
    db_ready = []
    for k in response_row.keys():
        if k in [rec['prompt_name'] for rec in prompts]:
            db_rec = {}
            rec = [i for i in prompts if i['prompt_name']==k][0]
            db_rec['prompt_id'] = rec['prompt_id']
            db_rec['response'] = response_row[k]
            db_rec['user_id'] = response_row['user_id']
            db_ready.append(db_rec)

    q = """
    INSERT INTO
                pochemuchka.response
    (prompt_id, user_id, response, response_dt)
    VALUES (
        :prompt_id
        ,:user_id
        ,:response
        ,CURRENT_TIMESTAMP
    )
    """
    conn.execute(q, params=db_ready)
    return 'OK'


if __name__ == '__main__':
    app.run()
