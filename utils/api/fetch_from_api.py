import requests
import app_config as app_config
import json

base_url = 'https://youtube.googleapis.com/youtube/v3/'
channels_url = base_url + 'channels'
playlist_url = base_url + 'playlistItems'
search_url = base_url + 'search'
videos_url = base_url + 'videos'

ht = '%23'
pipe = '%7C'

verbose = True


def make_response(status, message):
    response_data = {
        'status': status,
        'message': message
    }
    return json.dumps(response_data)


def make_success(message):
    return make_response('success', message)


def make_fail(message):
    return make_response('fail', message)


def make_error(message):
    return make_response('error', message)


def get_video_url(id):
    return 'https://www.youtube.com/watch?v=' + id


def get_channel_url(id):
    return 'https://www.youtube.com/channel/' + id


def get_channel_by_id(id):
    channel = {}

    data = {
        'part': 'snippet,contentDetails',
        'id': id,
        'key': app_config.YOUTUBE_API_KEY,
        'fields': 'items(id,contentDetails/relatedPlaylists/uploads,snippet(title,description,publishedAt,thumbnails/high/url))'
    }

    r = requests.get(channels_url, params=data).json()

    try:
        item = r['items'][0]
        snippet = item.get('snippet', 'N/A')
        details = item.get('contentDetails', 'N/A')

        if snippet != 'N/A':
            channel['channel_title'] = snippet.get('title', 'N/A')
            channel['channel_description'] = snippet.get('description', 'N/A')
            channel['channel_id'] = item.get('id', 'N/A')
            channel['channel_url'] = 'https://www.youtube.com/channel/' + channel['channel_id']
            channel['channel_thumbnail_url'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

        if details != 'N/A':
            channel['channel_uploads_playlist'] = details.get('relatedPlaylists', 'N/A').get('uploads', 'N/A')

        return channel
    except:
        make_error("Failed to get channel from Youtube API")


def get_uploads_by_id(id, pages=1, max_count=5):
    uploads = []
    next_page_token = ''
    for x in range(0, pages):
        if verbose:
            print('Page {} of {}'.format(str(x), str(pages)))

        data = {
            'part': 'snippet',
            'playlistId': id,
            'maxResults': max_count,
            'key': app_config.YOUTUBE_API_KEY,
            'fields': 'nextPageToken,items(id,snippet(title,description,channelId,channelTitle,publishedAt,resourceId/videoId,thumbnails/high/url))'
        }

        if next_page_token != '':
            data['pageToken'] = next_page_token

        r = requests.get(playlist_url, params=data).json()

        try:
            for item in r['items']:
                video = {}

                snippet = item.get('snippet', 'N/A')

                if snippet != 'N/A':
                    video['video_title'] = snippet.get('title', 'N/A')
                    video['video_description'] = snippet.get('description', 'N/A')
                    video['video_id'] = snippet.get('resourceId', 'N/A').get('videoId', 'N/A')
                    video['video_url'] = 'https://www.youtube.com/watch?v=' + video['video_id']

                    video['playlistItemId'] = item.get('id', 'N/A')
                    video['published_data'] = snippet.get('publishedAt', 'N/A')
                    video['thumbnail'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

                    video['channel_title'] = snippet.get('channelTitle', 'N/A')
                    video['channel_id'] = snippet.get('channelId', 'N/A')
                    video['channel_url'] = 'https://www.youtube.com/channel/' + video['channel_id']

                    uploads.append(video)

            next_page_token = r.get('nextPageToken', 'N/A')

            if next_page_token == 'N/A':
                print("No more pages")
                break
        except:
            return ['Youtube API Error']

    return uploads


def get_video_by_id(video_id):
    video = {}

    data = {
        'part': 'snippet,statistics,player',
        'id': video_id,
        'key': app_config.YOUTUBE_API_KEY,
        'fields': 'items(id,snippet(title,description,channelId,channelTitle,publishedAt,thumbnails/high/url,tags),statistics(viewCount,likeCount,dislikeCount,commentCount),player/embedHtml)'
    }

    r = requests.get(videos_url, params=data).json()

    try:
        items = r['items'][0]
        snippet = items.get('snippet', 'N/A')
        statistics = items.get('statistics', 'N/A')
        player = items.get('player', 'N/A')

        if snippet != 'N/A':
            video['video_title'] = snippet.get('title', 'N/A')
            video['video_description'] = snippet.get('description', 'N/A')
            video['video_id'] = items.get('id', 'N/A')
            video['video_url'] = 'https://www.youtube.com/watch?v=' + video['video_id']
            video['video_tags'] = snippet.get('tags', [])

            video['video_published_date'] = snippet.get('publishedAt', 'N/A')
            video['video_thumbnail_url'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

            video['channel_title'] = snippet.get('channelTitle', 'N/A')
            video['channel_id'] = snippet.get('channelId', 'N/A')
            video['channel_url'] = 'https://www.youtube.com/channel/' + video['channel_id']

        if statistics != 'N/A':
            video['video_views'] = statistics.get('viewCount', 'N/A')
            video['video_likes'] = statistics.get('likeCount', 'N/A')
            video['video_dislikes'] = statistics.get('dislikeCount', 'N/A')
            video['video_comments'] = statistics.get('commentCount', 'N/A')

        return video
    except:
        return make_error('Failed to get video from Youtube API')


def search_videos(query, pages=1, max_count=50, start_token='', sort_by='relevance'):
    videos = []
    next_page_token = start_token
    for x in range(0, pages):
        if verbose:
            print('Page {} of {}'.format(str(x), str(pages)))

        data = {
            'part': 'snippet',
            'id': id,
            'q': query,
            'maxResults': max_count,
            'safeSearch': 'none',
            'type': 'video',
            'key': app_config.YOUTUBE_API_KEY,
            'order': sort_by,
            'fields': 'nextPageToken,items(id/videoId,snippet(title,description,channelId,channelTitle,publishedAt,thumbnails/high/url))'
        }

        if next_page_token != '':
            data['pageToken'] = next_page_token

        r = requests.get(search_url, params=data).json()

        try:
            for item in r['items']:
                video = {}
                snippet = item.get('snippet', 'N/A')

                if snippet != 'N/A':
                    video['video_title'] = snippet.get('title', 'N/A')
                    video['video_description'] = snippet.get('description', 'N/A')
                    video['video_id'] = item.get('id', 'N/A').get('videoId', 'N/A')
                    video['video_url'] = 'https://www.youtube.com/watch?v=' + video['video_id']

                    video['video_published_date'] = snippet.get('publishedAt', 'N/A')
                    video['video_thumbnail_url'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

                    video['channel_title'] = snippet.get('channelTitle', 'N/A')
                    video['channel_id'] = snippet.get('channelId', 'N/A')
                    video['channel_url'] = 'https://www.youtube.com/channel/' + video['channel_id']

                    videos.append(video)

            next_page_token = r.get('nextPageToken', 'N/A')

            if next_page_token == 'N/A':
                print("No more pages")
                break
            else:
                file = open('./next.txt', 'w', encoding='utf-8')
                file.write(next_page_token + '\n')
                file.close()

        except:
            print("Youtube API Error")
            break

    return videos
