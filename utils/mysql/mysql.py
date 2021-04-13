# import MySQLdb
# from MySQLdb import cursors
# import json
# from datetime import datetime
# import YoutubeAPI
#
# import app_config as app_config
#
#
# def get_mysql():
#     return MySQLdb.connect(host=app_config.host, user=app_config.user, passwd=app_config.password, db=app_config.database, cursorclass=cursors.DictCursor, use_unicode=True, charset="utf8mb4")
#
#
# def get_cur():
#     return get_mysql().cursor()
#
#
# def video_exists(video_id):
#     data = execute_select("""SELECT COUNT(*) FROM videos WHERE video_id = %s""", (video_id,))
#     return data["COUNT(*)"] >= 1
#
#
# def channel_exists(channel_id):
#     data = execute_select("""SELECT COUNT(*) FROM channels WHERE channel_id = %s""", (channel_id,))
#     return data["COUNT(*)"] >= 1
#
#
# def get_channel_hm_from_id(channel_id):
#     return app_config.url_host + '/channels/' + channel_id
#
#
# def get_video_hm_from_id(video_id):
#     return app_config.url_host + '/videos/' + video_id
#
#
# def get_published_datetime(published):
#     temp = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
#     return temp.strftime('%Y-%m-%d %H:%M:%S')
#
#
# def create_channel(channel_id):
#     channel = YoutubeAPI.get_channel_by_id(channel_id)
#     data = execute_insert('channels',
#                           ['channel_id', 'channel_title', 'channel_description', 'channel_thumbnail_url', 'channel_uploads_playlist'],
#                           (channel['channelId'], channel['title'], channel['description'], channel['thumbnail'], channel['uploads']))
#     return json.dumps(data)
#
#
# def create_video(video):
#     if not video_exists(video['video_id']):
#         if not channel_exists(video['channelId']):
#             res = create_channel(video['channelId'])
#             print("Channel Created: " + str(res))
#         else:
#             pass
#             # print("Channel Exists, Skipping")
#
#         print("Inserting video " + video['video_id'])
#         data = execute_insert('videos',
#                               ['video_id', 'video_title', 'video_description', 'video_thumbnail_url', 'video_published_date',
#                                'video_views', 'video_likes', 'video_dislikes', 'video_comments', 'video_player', 'video_channel_hm', 'video_tags'],
#                               (video['video_id'], video['title'], video['description'], video['thumbnail_url'], get_published_datetime(video['published']),
#                                video['views'], video['likes'], video['dislikes'], video['comments'], video['player'], get_channel_hm_from_id(video['channelId']),
#                                json.dumps(video['video_tags'])))
#         return json.dumps(data)
#     else:
#         return "Video Exists, Skipping"
#
#
# def yt_json_to_mysql(video_data):
#     count = 0
#     max = len(video_data)
#     for k in video_data:
#         count += 1
#         print('{}/{} Completed'.format(count, max))
#         video = video_data[k]
#         channel_id = video['channelId']
#
#         tags = video['tags']
#
#         data = {
#             'title': video['title'],
#             'description': video['description'],
#             'video_id': video['videoId'],
#             'video_tags': tags,
#             'thumbnail_url': video['thumbnail'],
#             'published': video['published'],
#             'views': video['views'],
#             'likes': video['likes'],
#             'dislikes': video['dislikes'],
#             'comments': video['comments'],
#             'player': video['player'],
#             'channelId': channel_id,
#         }
#
#         try:
#             r = create_video(data)
#             print(str(r))
#         except:
#             pass
#
#
# def api_format_to_mysql(video_data):
#     count = 0
#     max = len(video_data)
#     for video in video_data:
#
#         data = {
#             'title': video['video_title'],
#             'description': video['video_description'],
#             'video_id': video['video_id'],
#             'video_tags': video['video_tags'],
#             'thumbnail_url': video['video_thumbnail_url'],
#             'published': video['video_published_date'],
#             'views': video['video_views'],
#             'likes': video['video_likes'],
#             'dislikes': video['video_dislikes'],
#             'comments': video['video_comments'],
#             'player': video['video_player'],
#             'channelId': video['video_channel_hm'][-24:],
#         }
#
#         try:
#             r = create_video(data)
#             print(str(r))
#         except:
#             pass
#
#
# # file = open('./new_filtered.json', 'r', encoding='utf-8')
# # videos = json.loads(file.read())
# # file.close()
# #
# # api_format_to_mysql(videos)
#
#
# file = open('../logs/videos-hololive eng.json', 'r', encoding='utf-8')
# videos = json.loads(file.read())
# file.close()
#
# yt_json_to_mysql(videos)
#
# # fields = ('username', 'subreddit', 'type', 'content', 'date')
# # values = ('test', 'Testing', 'Comment', 'This is a test', timestamp())
# #
# # print(insert_row('users', fields, values))
#
#
# # data = execute_select("SELECT * FROM subreddit_whitelist")
# #
# # for i in data:
# #     print(i['subreddit'])
