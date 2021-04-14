from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from utils.mysql.create import *
from utils.api.match import *

from flask.views import MethodView

import app_config as app_config

app = Flask(__name__)
mysql = MySQL(app)
CORS(app, resources={r'/*': {'origins': '*'}})

debug = True

app.config['TESTING'] = debug
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


class ChannelAPI(MethodView):
    def get(self, channel_id):
        if channel_id is None:
            data = get_channels(mysql)
            print(str(len(data)) + ' channels fetched')
            return jsonify(data)
        else:
            if channel_exists(mysql, channel_id):
                data = execute_select(mysql, """SELECT * FROM channels WHERE channel_id = %s""", (channel_id,))
                return jsonify(data)
            else:
                return make_fail('channel does not exist')

    def post(self):
        if request.form['channel_id'] != '':
            channel_id = request.form['channel_id']
            return create_channel(mysql, channel_id)
        else:
            return make_error("missing fields")

    def delete(self, channel_id):
        if channel_id is not None:
            if channel_exists(mysql, channel_id):
                data = execute_delete(mysql, 'channels', 'channel_id', channel_id)
                return data
            else:
                return make_fail('channel does not exist')
        else:
            return make_fail("DELETE request must be made on channel object")

    def put(self, channel_id):
        if channel_exists(mysql, channel_id):
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
            talent_field = ''

            if request.args.get('talent') is not None:
                talent_field = str(request.args['talent']).lower()
            elif request.form.get('talent') is not None != '':
                talent_field = str(request.form['talent']).lower()

            # No talent data
            if talent_field == '':
                data = get_videos(mysql)
                print(str(len(data)) + ' videos fetched')
                return jsonify(data)

            # Yes talent data
            else:
                talent = get_talent(mysql, talent_field)
                data = get_videos(mysql)

                matched_videos = []
                for v in data:
                    if talent:
                        if talent_match(talent['name'], talent['aliases'], v):
                            # if talent_field in v['video_title'].lower() or any(alias in v['video_title'].lower() for alias in talent_field):
                            matched_videos.append(v)
                    else:
                        return make_error('invalid talent value')

                print(str(len(matched_videos)) + ' videos fetched')

                return jsonify(matched_videos)

        else:
            if video_exists(mysql, video_id):
                data = execute_select(mysql, """SELECT * FROM videos WHERE video_id = %s""", (video_id,))
                return jsonify(data)
            else:
                return make_fail('video does not exist')

    def post(self):
        if request.form['video_id'] != '':
            video_id = request.form['video_id']
            return create_video(mysql, video_id)
        else:
            return make_error("missing fields")

    def delete(self, video_id):
        if video_id is not None:
            if video_exists(mysql, video_id):
                data = execute_delete(mysql, 'videos', 'video_id', video_id)
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


class TalentAPI(MethodView):
    def get(self, talent):
        if talent is None:
            aliases = get_aliases(mysql)

            data = {}
            for a in aliases:
                data[a['talent_name']] = data.get(a['talent_name'], [])
                data[a['talent_name']].append(a['alias'])

            return jsonify(data)

        else:
            talent_data = get_talent(mysql, talent)
            if talent_data:
                return jsonify(talent_data)
            else:
                return make_fail('talent does not exist')

    def post(self):
        if request.form['talent'] != '':
            talent = request.form['talent']
            data = create_talent(mysql, talent)

            return jsonify(data)
        else:
            return make_error("missing fields")

    def delete(self, talent):
        if talent is not None:
            if talent_exists(mysql, talent):
                data = execute_delete(mysql, 'talents', 'name', talent)
                return data
            else:
                return make_fail('talent does not exist')
        else:
            return make_fail("DELETE request must be made on talent object")

    def put(self, talent):
        if talent is not None:
            return make_construction('talent PUT requests currently under construction')
        else:
            return make_fail("PUT request must be made on talent object")


def register_api(view, endpoint, url, pk='id', pk_type='string'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(ChannelAPI, 'channel_api', '/channels/', pk='channel_id')
register_api(VideoAPI, 'video_api', '/videos/', pk='video_id')
register_api(TalentAPI, 'talent_api', '/talents/', pk='talent')


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
    app.run(host='127.0.0.1', port=8000, debug=debug)
