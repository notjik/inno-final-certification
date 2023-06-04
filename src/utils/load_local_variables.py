import os
import inspect

from dotenv import load_dotenv


def view_nones():
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars
            if var_val is None and not var_name.startswith('__') and not var_name.endswith('__')]


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BANK_TOKEN = os.getenv('BANK_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')
DB_PATH = os.getenv('DB_PATH')
LOG_MESSAGE_PATH = os.getenv('LOG_MESSAGE_PATH')
LOG_DB_PATH = os.getenv('LOG_DB_PATH')
LOG_STATUS_PATH = os.getenv('LOG_STATUS_PATH')
nones = view_nones()
if nones:
    exit('Create local variables: {}'.format(', '.join(nones)))
