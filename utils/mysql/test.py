from utils.mysql.create import *
from utils.mysql.get import *
from utils.mysql.execute import execute_delete
from utils.mysql.connect import *



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

# print(create_talent('test'))

# print(create_talent('test'))
#
# print(create_alias('test', 'test'))

t = get_talent('watson')
if t:
    print("t: " + str(t))

# file = open('./talents.json', 'r', encoding='utf-8')
# talents = json.loads(file.read())
# file.close()
#
#
# for t in talents:
#     name = t['full_name']
#
#     print('Creating talent: ' + name)
#     print(create_talent(name))
#
#     print('\tCreating alias: ' + t['name'] + ' for ' + name)
#     print(create_alias(t['name'], name))
#
#     for a in t['aliases']:
#         print('\tCreating alias: ' + a + ' for ' + name)
#         print(create_alias(a, name))
#
#     print('\n')