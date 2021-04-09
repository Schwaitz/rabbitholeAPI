import requests
import app_config as app_config

api_key = app_config.YOUTUBE_API_KEY

base_url = 'https://youtube.googleapis.com/youtube/v3/'
channels_url = base_url + 'channels'
playlist_url = base_url + 'playlistItems'
search_url = base_url + 'search'
videos_url = base_url + 'videos'

ht = '%23'
pipe = '%7C'

verbose = True


def get_video_url(id):
    return 'https://www.youtube.com/watch?v=' + id


def get_channel_url(id):
    return 'https://www.youtube.com/channel/' + id


def get_channel_by_id(id):
    channel = {}

    data = {
        'part': 'snippet,contentDetails',
        'id': id,
        'key': api_key,
        'fields': 'items(id,contentDetails/relatedPlaylists/uploads,snippet(title,description,publishedAt,thumbnails/high/url))'
    }

    r = requests.get(channels_url, params=data).json()

    item = r['items'][0]
    snippet = item.get('snippet', 'N/A')
    details = item.get('contentDetails', 'N/A')

    if snippet != 'N/A':
        channel['title'] = snippet.get('title', 'N/A')
        channel['description'] = snippet.get('description', 'N/A')
        channel['channelId'] = item.get('id', 'N/A')
        channel['channelUrl'] = 'https://www.youtube.com/channel/' + channel['channelId']
        channel['thumbnail'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

    if details != 'N/A':
        channel['uploads'] = details.get('relatedPlaylists', 'N/A').get('uploads', 'N/A')

    return channel


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
            'key': api_key,
            'fields': 'nextPageToken,items(id,snippet(title,description,channelId,channelTitle,publishedAt,resourceId/videoId,thumbnails/high/url))'
        }

        if next_page_token != '':
            data['pageToken'] = next_page_token

        r = requests.get(playlist_url, params=data).json()

        for item in r['items']:
            video = {}

            snippet = item.get('snippet', 'N/A')

            if snippet != 'N/A':
                video['title'] = snippet.get('title', 'N/A')
                video['description'] = snippet.get('description', 'N/A')
                video['videoId'] = snippet.get('resourceId', 'N/A').get('videoId', 'N/A')
                video['videoUrl'] = 'https://www.youtube.com/watch?v=' + video['videoId']

                video['playlistItemId'] = item.get('id', 'N/A')
                video['published'] = snippet.get('publishedAt', 'N/A')
                video['thumbnail'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

                video['channelTitle'] = snippet.get('channelTitle', 'N/A')
                video['channelId'] = snippet.get('channelId', 'N/A')
                video['channelUrl'] = 'https://www.youtube.com/channel/' + video['channelId']

                uploads.append(video)

        next_page_token = r.get('nextPageToken', 'N/A')

        if next_page_token == 'N/A':
            print("No more pages")
            break

    return uploads


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
            'key': api_key,
            'order': sort_by,
            'fields': 'nextPageToken,items(id/videoId,snippet(title,description,channelId,channelTitle,publishedAt,thumbnails/high/url))'
        }

        if next_page_token != '':
            data['pageToken'] = next_page_token

        r = requests.get(search_url, params=data).json()

        for item in r['items']:
            video = {}
            snippet = item.get('snippet', 'N/A')

            if snippet != 'N/A':
                video['title'] = snippet.get('title', 'N/A')
                video['description'] = snippet.get('description', 'N/A')
                video['videoId'] = item.get('id', 'N/A').get('videoId', 'N/A')
                video['videoUrl'] = 'https://www.youtube.com/watch?v=' + video['videoId']

                video['published'] = snippet.get('publishedAt', 'N/A')
                video['thumbnail'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

                video['channelTitle'] = snippet.get('channelTitle', 'N/A')
                video['channelId'] = snippet.get('channelId', 'N/A')
                video['channelUrl'] = 'https://www.youtube.com/channel/' + video['channelId']

                videos.append(video)

        next_page_token = r.get('nextPageToken', 'N/A')

        if next_page_token == 'N/A':
            print("No more pages")
            break
        else:
            file = open('next.txt', 'w', encoding='utf-8')
            file.write(next_page_token + '\n')
            file.close()
    return videos



def get_video_by_id(vodep_id):
    video = {}

    data = {
        'part': 'snippet,statistics,player',
        'id': vodep_id,
        'key': api_key,
        'fields': 'items(id,snippet(title,description,channelId,channelTitle,publishedAt,thumbnails/high/url,tags,defaultAudioLanguage),statistics(viewCount,likeCount,dislikeCount,commentCount),player/embedHtml)'
    }

    r = requests.get(videos_url, params=data).json()

    print(str(r))
    items = r['items'][0]
    snippet = items.get('snippet', 'N/A')
    statistics = items.get('statistics', 'N/A')
    player = items.get('player', 'N/A')

    if snippet != 'N/A':
        video['title'] = snippet.get('title', 'N/A')
        video['description'] = snippet.get('description', 'N/A')
        video['videoId'] = items.get('id', 'N/A')
        video['videoUrl'] = 'https://www.youtube.com/watch?v=' + video['videoId']
        video['tags'] = snippet.get('tags', [])

        video['published'] = snippet.get('publishedAt', 'N/A')
        video['thumbnail'] = snippet.get('thumbnails', 'N/A').get('high', 'N/A').get('url', 'N/A')

        video['audioLanguage'] = snippet.get('defaultAudioLanguage', 'N/A')

        video['channelTitle'] = snippet.get('channelTitle', 'N/A')
        video['channelId'] = snippet.get('channelId', 'N/A')
        video['channelUrl'] = 'https://www.youtube.com/channel/' + video['channelId']

    if statistics != 'N/A':
        video['views'] = statistics.get('viewCount', 'N/A')
        video['likes'] = statistics.get('likeCount', 'N/A')
        video['dislikes'] = statistics.get('dislikeCount', 'N/A')
        video['comments'] = statistics.get('commentCount', 'N/A')

    if player != 'N/A':
        video['player'] = player.get('embedHtml', 'N/A')

    return video
