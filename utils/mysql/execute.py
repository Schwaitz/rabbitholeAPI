import MySQLdb
from MySQLdb import cursors

import app_config as app_config


def execute_select(mysql, query, values=('none',), from_flask=True):
    conn = mysql.connection if from_flask else mysql
    cur = conn.cursor()

    return_message = {}
    try:
        if values[0] == 'none':
            cur.execute(query)
        else:
            cur.execute(query, values)

        return_message = list(cur.fetchall())
        if len(return_message) == 1:
            return_message = return_message[0]

    except Exception as e:
        return_message = {'status': 'error', 'data': {'action': 'SELECT', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)}}
    finally:
        cur.close()
        return return_message


def execute_insert(mysql, table, fields, values, from_flask=True):
    conn = mysql.connection if from_flask else mysql
    cur = conn.cursor()

    return_message = {}
    try:
        values_string = "("
        for v in values:
            values_string += "%s, "
        values_string = values_string[:-2]
        values_string += ")"

        fields_string = "("
        for f in fields:
            fields_string += f + ", "
        fields_string = fields_string[:-2]
        fields_string += ")"

        # print("""INSERT INTO {} {} VALUES {}""".format(table, fields_string, values_string))

        query = """INSERT INTO {} {} VALUES {}""".format(table, fields_string, values_string)

        cur.execute(query, values)
        conn.commit()
        return_message = {'status': 'success', 'action': 'INSERT', 'data': {}}

        for i in range(0, len(fields)):
            return_message['data'][fields[i]] = values[i]

    except Exception as e:
        return_message = {'status': 'error', 'action': 'INSERT', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)}
    finally:
        cur.close()
        return return_message


def execute_delete(mysql, table, field, value, from_flask=True):
    conn = mysql.connection if from_flask else mysql
    cur = conn.cursor()

    return_message = {}
    try:
        query = """DELETE FROM {} WHERE {} = %s""".format(table, field)
        cur.execute(query, (value,))
        conn.commit()

        return_message = {'status': 'success', 'action': 'DELETE'}
    except Exception as e:
        return_message = {'status': 'error', 'action': 'DELETE', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)}
    finally:
        cur.close()
        return return_message
