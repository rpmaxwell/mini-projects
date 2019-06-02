import json
import os


environment = 'gameplan_app'

class BaseConfig(object):
    cred_file_path = os.environ['CRED_FILE_LOCATION']
    cred_payload = json.loads(open(cred_file_path).read())[environment]

    SECRET_KEY = cred_payload['SECRET_KEY']
    DEBUG = cred_payload['DEBUG']
    WTF_CSRF_SECRET_KEY = cred_payload['WTF_CSRF_SECRET_KEY']
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    #     cred_payload['DB_USER'], cred_payload['DB_PASS'], cred_payload['DB_SERVICE'], cred_payload['DB_PORT'], cred_payload['DB_NAME']
    # )