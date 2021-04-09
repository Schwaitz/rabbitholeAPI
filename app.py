from flask import Flask, request, jsonify, render_template, json
from flask_mysqldb import MySQL
import YoutubeAPI
from datetime import datetime

from flask.views import MethodView

import app_config as app_config

app = Flask(__name__)
mysql = MySQL(app)

app.config['TESTING'] = False
app.config['SECRET_KEY'] = app_config.SECRET_KEY

app.config['MYSQL_HOST'] = app_config.host
app.config['MYSQL_USER'] = app_config.user
app.config['MYSQL_PASSWORD'] = app_config.password
app.config['MYSQL_DB'] = app_config.database
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.url_map.strict_slashes = False


def get_result(r):
    try:
        r = r.json()
        return str(r)
    except Exception as e:
        print(str({'status': 'error', 'action': 'get_result', 'exception': str(type(e).__name__), 'message': 'Error during the getting of a result', 'e': str(e)}))
        return str(r.text)


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


def get_channel_hm_from_id(channel_id):
    return app_config.url_host + '/channels/' + channel_id


def get_video_hm_from_id(video_id):
    return app_config.url_host + '/videos/' + video_id


def get_published_datetime(published):
    temp = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    return temp.strftime('%Y-%m-%d %H:%M:%S')


def make_construction(message):
    return jsonify({'status': 'construction', 'message': message})


def make_error(message):
    return jsonify({'status': 'error', 'message': message})


def make_fail(message):
    return jsonify({'status': 'fail', 'message': message})


def create_channel(channel_id):
    channel = YoutubeAPI.get_channel_by_id(channel_id)
    data = execute_insert('channels',
                          ['channel_id', 'channel_title', 'channel_description', 'channel_thumbnail_url', 'channel_uploads_playlist'],
                          (channel['channelId'], channel['title'], channel['description'], channel['thumbnail'], channel['uploads']))
    return jsonify(data)


def create_video(video_id):
    video = YoutubeAPI.get_video_by_id(video_id)

    if not channel_exists(video['channelId']):
        res = create_channel(video['channelId'])
        print("Channel Creation: " + str(res))

    data = execute_insert('videos',
                          ['video_id', 'video_title', 'video_description', 'video_thumbnail_url', 'video_published_date',
                           'video_views', 'video_likes', 'video_dislikes', 'video_comments', 'video_player', 'video_channel_hm', 'video_tags'],
                          (video['videoId'], video['title'], video['description'], video['thumbnail'], get_published_datetime(video['published']),
                           video['views'], video['likes'], video['dislikes'], video['comments'], video['player'], get_channel_hm_from_id(video['channelId']),
                           json.dumps(video['tags'])))
    return jsonify(data)


class ChannelAPI(MethodView):
    def get(self, channel_id):
        if channel_id is None:
            data = get_channels()
            print(str(len(data)) + ' channels fetched')
            return jsonify(data)
        else:
            if channel_exists(channel_id):
                data = execute_select("""SELECT * FROM channels WHERE channel_id = %s""", (channel_id,))
                return jsonify(data)
            else:
                return make_fail('channel does not exist')

    def post(self):
        if request.form['channel_id'] != '':
            channel_id = request.form['channel_id']

            if not channel_exists(channel_id):
                return create_channel(channel_id)
            else:
                return make_error("channel already exists")
        else:
            return make_error("missing fields")

    def delete(self, channel_id):
        if channel_id is not None:
            if channel_exists(channel_id):
                data = execute_delete('channels', 'channel_id', channel_id)
                return data
            else:
                return make_fail('channel does not exist')
        else:
            return make_fail("DELETE request must be made on channel object")

    def put(self, channel_id):
        if channel_exists(channel_id):
            if request.form['channel_title'] != '' and request.form['channel_description'] != '' and request.form['channel_thumbnail_url'] != '' and request.form['channel_uploads_playlist'] != '':
                cur = mysql.connection.cursor()
                return_message = {}
                try:
                    cur.execute("""UPDATE channels SET channel_title = %s, channel_description = %s, channel_thumbnail_url = %s, channel_uploads_playlist = %s WHERE channel_id = %s""",
                                (request.form['channel_title'], request.form['channel_description'], request.form['channel_thumbnail_url'], request.form['channel_uploads_playlist'], channel_id))
                    mysql.connection.commit()

                    return_message = jsonify({
                        'status': 'success', 'action': 'UPDATE',
                        'data': {'channel_title': request.form['channel_title'], 'channel_description': request.form["channel_description"],
                                 'channel_thumbnail_url': request.form["channel_thumbnail_url"], 'channel_uploads_playlist': request.form["channel_uploads_playlist"]}
                    })
                except Exception as e:
                    return_message = jsonify({'status': 'error', 'action': 'UPDATE', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)})
                finally:
                    cur.close()
                    return return_message
            else:
                return make_error("missing fields")

        else:
            return make_fail('channel does not exist')


class VideoAPI(MethodView):
    def get(self, video_id):
        if video_id is None:
            data = get_videos()
            print(str(len(data)) + ' videos fetched')
            return jsonify(data)
        else:
            if video_exists(video_id):
                data = execute_select("""SELECT * FROM videos WHERE video_id = %s""", (video_id,))
                return jsonify(data)
            else:
                return make_fail('video already exists')

    def post(self):
        if request.form['video_id'] != '':
            video_id = request.form['video_id']
            if not video_exists(video_id):
                return create_video(video_id)
            else:
                return make_error("video already exists")
        else:
            return make_error("missing fields")

    def delete(self, video_id):
        if video_id is not None:
            if video_exists(video_id):
                data = execute_delete('videos', 'video_id', video_id)
                return data
            else:
                return make_fail('video does not exist')
        else:
            return make_fail("DELETE request must be made on video object")

    def put(self, video_id):
        if video_id is not None:
            return make_construction('video PUT requests currently under construction')
        else:
            return make_fail("PUT request must be made on video object")
        # if video_exists(video_id):
        #     if request.form['video_title'] != '' and request.form['channel_description'] != '' and request.form['channel_thumbnail_url'] != '' and request.form['channel_uploads_playlist'] != '':
        #         cur = mysql.connection.cursor()
        #         return_message = {}
        #         try:
        #             cur.execute("""UPDATE channels SET channel_title = %s, channel_description = %s, channel_thumbnail_url = %s, channel_uploads_playlist = %s WHERE channel_id = %s""",
        #                         (request.form['channel_title'], request.form['channel_description'], request.form['channel_thumbnail_url'], request.form['channel_uploads_playlist'], channel_id))
        #             mysql.connection.commit()
        #
        #             return_message = jsonify({
        #                 'status': 'success', 'action': 'UPDATE',
        #                 'data': {'channel_title': request.form['channel_title'], 'channel_description': request.form["channel_description"],
        #                          'channel_thumbnail_url': request.form["channel_thumbnail_url"], 'channel_uploads_playlist': request.form["channel_uploads_playlist"]}
        #             })
        #         except Exception as e:
        #             return_message = jsonify({'status': 'error', 'action': 'UPDATE', 'exception': str(type(e).__name__), 'message': 'Error during execution of query', 'e': str(e)})
        #         finally:
        #             cur.close()
        #             return return_message
        #     else:
        #         return make_error("missing fields")

        # else:
        # return make_fail('channel does not exist')


def register_api(view, endpoint, url, pk='id', pk_type='string'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(ChannelAPI, 'channel_api', '/channels/', pk='channel_id')
register_api(VideoAPI, 'video_api', '/videos/', pk='video_id')


def timestamp():
    return str(datetime.today().strftime("%m/%d/%Y %H:%M:%S %p"))


@app.route('/')
def index():
    endpoints = [
        {'methods': 'GET, POST', 'link': '/channels', 'desc': 'data for all channels'},
        {'methods': 'GET, PUT, DELETE', 'link': '/channels/id', 'desc': 'data for a single channel'},

        {'methods': 'GET, POST', 'link': '/videos', 'desc': 'data for all videos'},
        {'methods': 'GET, PUT, DELETE', 'link': '/videos/id', 'desc': 'data for a single video'},
    ]

    methods = []
    links = []
    descs = []

    for e in endpoints:
        methods.append(e['methods'])
        links.append(e['link'])
        descs.append(e['desc'])

    return render_template('index.html', count=len(endpoints), methods=methods, links=links, descs=descs)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
