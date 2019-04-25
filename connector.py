import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, insert, create_engine

class DBConn(object):
    def __init__(self, environment=None, schema_name=None):
        if environ:
            cred_file_path = os.environ['CRED_FILE_LOCATION']
            cred_payload = json.loads(open(cred_file_path).read())[environ]
            url = 'postgresql://{user}:{password}@{host}/{db}'.format(**cred_payload)
        else:
            url = 'postgresql://{0}:{1}@{2}/{3}'.format(**kwargs.values())
        self.engine = create_engine(url)
        self.metadata = MetaData(schema=schema_name)
        self.metadata.bind = self.engine

    def execute(self, query, fmt='df', params=None):
        """Take a SQL query in string format and then executes in Presto."""
        params = params or {}
        proxy = self.engine.execute(sqlalchemy.text(query), params)
        try:
            results_obj = self._format_query(proxy, fmt)
            return results_obj
        except:
            return None

    @staticmethod
    def _format_query(proxy, fmt):
        '''
        returns the results of the proxy object in the specified format (dataframe, dict, list etc.)
        Pandas Dataframes are handled explictly while others are just applied using the eval
        function.
        TODO:
        add timezone and datatype considerations as in dconn.
        '''
        if fmt == 'df':
            columns = [str(k) for k in proxy.keys()]
            results_obj = pd.DataFrame(proxy.fetchall(), columns=columns)
        else:
            results_obj = list(map(eval(fmt), proxy))
        return results_obj

def SheetConn(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',\
         'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open(sheet_name)
    return wks


