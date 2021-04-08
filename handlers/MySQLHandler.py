from app import mysql


def execute_select(query, values=('none',)):
    cur = mysql.connection.cursor()
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


def execute_insert(table, fields, values):
    cur = mysql.connection.cursor()
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

        query = """INSERT INTO {} {} VALUES {}""".format(table, fields_string, values_string)

        cur.execute(query, values)
        mysql.connection.commit()
        return_message = {'status': 'success', 'action': 'INSERT', 'data': {}}

        for i in range(0, len(fields)):
            return_message['data'][fields[i]] = values[i]

    except Exception as e:
        return_message = {'status': 'error', 'action': 'INSERT', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)}
    finally:
        cur.close()
        return return_message


def execute_delete(table, field, value):
    cur = mysql.connection.cursor()
    return_message = {}
    try:
        query = """DELETE FROM {} WHERE {} = %s""".format(table, field)
        cur.execute(query, (value,))
        mysql.connection.commit()

        return_message = {'status': 'success', 'action': 'DELETE'}
    except Exception as e:
        return_message = {'status': 'error', 'action': 'DELETE', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)}
    finally:
        cur.close()
        return return_message


def tag_exists(tag):
    data = execute_select("""SELECT COUNT(*) FROM tags WHERE tag = %s""", (tag,))
    return data["COUNT(*)"] >= 1


def video_exists(video_id):
    data = execute_select("""SELECT COUNT(*) FROM videos WHERE video_id = %s""", (video_id,))
    return data["COUNT(*)"] >= 1


def channel_exists(channel_id):
    data = execute_select("""SELECT COUNT(*) FROM channels WHERE channel_id = %s""", (channel_id,))
    return data["COUNT(*)"] >= 1


def get_channels():
    data = execute_select("""SELECT * FROM channels""")
    return data


def get_videos():
    data = execute_select("""SELECT * FROM videos""")
    return data


def get_tags():
    data = execute_select("""SELECT * FROM tags""")
    return data
