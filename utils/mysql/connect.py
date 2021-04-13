import MySQLdb
from MySQLdb import cursors

import app_config as app_config


def get_mysql():
    return MySQLdb.connect(host=app_config.host, user=app_config.user, passwd=app_config.password, db=app_config.database, cursorclass=cursors.DictCursor, use_unicode=True, charset="utf8mb4")


def get_cur():
    return get_mysql().cursor()

