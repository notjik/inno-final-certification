import sys
import logging

from utils.load_local_variables import LOG_MESSAGE_PATH, LOG_DB_PATH, LOG_STATUS_PATH

logger_message = logging.getLogger('messages')
logger_message.setLevel(logging.INFO)
formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                       "%(user)s[%(user_id)d] send %(content_type)s\ndetailed: %(message)s\n",
                                       datefmt="%Y-%m-%d %H:%M:%S")
_handler_logfile = logging.FileHandler(LOG_MESSAGE_PATH, mode='a', encoding='utf8')
_handler_logfile.setFormatter(formatter_messages)
_handler_console = logging.StreamHandler(sys.stdout)
_handler_console.setFormatter(formatter_messages)
logger_message.addHandler(_handler_logfile)
logger_message.addHandler(_handler_console)

logger_database_engine = logging.getLogger('sqlalchemy.engine')
logger_database_engine.setLevel(logging.DEBUG)
formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                       "[%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
_handler_logfile = logging.FileHandler(LOG_DB_PATH, mode='a', encoding='utf8')
_handler_logfile.setFormatter(formatter_messages)
logger_database_engine.addHandler(_handler_logfile)

logger_database_pool = logging.getLogger('sqlalchemy.pool')
logger_database_pool.setLevel(logging.DEBUG)
formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                       "[%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
_handler_logfile = logging.FileHandler(LOG_DB_PATH, mode='a', encoding='utf8')
_handler_logfile.setFormatter(formatter_messages)
logger_database_pool.addHandler(_handler_logfile)

logger_status = logging.getLogger('status')
logger_status.setLevel(logging.INFO)
formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                       "The %(bot)s[%(bot_id)d] %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
_handler_logfile = logging.FileHandler(LOG_STATUS_PATH, mode='a', encoding='utf8')
_handler_logfile.setFormatter(formatter_messages)
_handler_console = logging.StreamHandler(sys.stdout)
_handler_console.setFormatter(formatter_messages)
logger_status.addHandler(_handler_logfile)
logger_status.addHandler(_handler_console)

