import requests
import json
from datetime import datetime
import app_config as app_config
import re


def get_talent_data():
    data = requests.get('http://api.rabbithole.moe/talents').json()
    return data


holo_related_keywords = ['hololive', 'holo live', 'holoen', 'holo en', 'holoid', 'holo id', 'holostars', 'holo stars', 'hololiveclips', 'hololiveclip']

keywords = [
    {
        "category": "hololive",
        "list": holo_related_keywords,
        "worth": {
            "title": 5,
            "description": 2,
            "tags": 3
        }
    },
    {
        "category": "vtuber",
        "list": ['vtuber', 'v tuber'],
        "worth": {
            "title": 1,
            "description": 1,
            "tags": 1
        }
    },
    {
        "category": "pairings",
        "list": ['okakoro', 'mioshuba', 'noefure'],
        "worth": {
            "title": 5,
            "description": 5,
            "tags": 5
        }
    }
]

translation_keywords = ['engsub', 'eng sub', 'english sub', 'sub eng', 'holoengsubs']
translation_worth = {
    "title": 10,
    "description": 6,
    "tags": 8
}

# Blacklist if also doesn't have a talent match
no_name_blacklist = ['nijisanji']

tag_keywords = []

count = 0

score_deletion_threshold = 8.0

name_worth = {
    "title": 10,
    "description": 5,
    "tags": 5
}

name_count_exponent = {
    "title": 0.1,
    "description": 0.4,
    "tags": 0.3
}

official_channels_blacklist = ['UCJFZiqLMntJufDCHc6bQixg', 'UCfrWoRGlawPQDQxxeIDRP0Q', 'UCotXwY6s8pWmuWd_snKYjhg', 'UCWsfcksUUpoEvhia0_ut0bA', 'UCp6993wxpyDPHUpavwDFqgg',
                               'UCDqI2jOz0weumE8s7paEk6g', 'UC0TXe_LYZ4scaW2XMyi5_kw', 'UC5CwaMl1eIgY8h02uZw7u8A', 'UC-hM6YJuNYVAmUWxeIr9FeA', 'UC1CfXB_kRs3C-zaeTG3oGyg',
                               'UCD8HOxPs4Xvsm8H0ZxXGiBw', 'UCdn5BQ06XqgXoAxIhbqw5Rg', 'UCFTLzh12_nrtzqBPsTCqenA', 'UCQ0UDLQCjY0rmuxCDE38FGg', 'UCHj_mh57PVMXhAUDphUQDFA',
                               'UCLbtM3JZfRTg8v2KGag-RMw', 'UC1opHUrw8rvnsadT-iGp7Cg', 'UC1suqwovbL1kzsoaZgFZLKg', 'UC7fk0CB07ly8oSl0aqKkqFg', 'UCvzGlP9oQwU--Y0r9id_jnA',
                               'UCXTpFs_3PqI41qX2d9tL2Rw', 'UCp3tgHXw_HI0QMk1K8qh3gQ', 'UChAnqc_AY5_I3Px5dig3X1Q', 'UCp-5t9SrOQwXMU7iIjQfARg', 'UCvaTdHTWBGv3MKj3KVqJVCw',
                               'UC1DCedRgGHBdm81E1llLhOQ', 'UCCzUftO8KOVkV4wQG1vkUvg', 'UCdyqAaZDKHXg4Ahi7VENThQ', 'UCl_gCybOJRIgOXw6Qb4qJzQ', 'UCvInZx9h3jC2JzsIzoOebWg',
                               'UC1uv2Oq6kNxgATlCiez59hw', 'UCa9Y57gfeY0Zro_noHRVrnw', 'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCS9uQI-jC3DE0L4IpXyvr6w', 'UCZlDXzGoo7d44bwdNObFacg',
                               'UCAWSyEs_Io8MtpY3m-zqILA', 'UCFKOVgVbGmX65RxO3EtH3iw', 'UCK9V2B22uJYu3N7eR_BT9QA', 'UCUKD-uaobj9jiqB-VXt71mA', 'UCHsx4Hqa-1ORjQTh9TYDhww',
                               'UCL_qhgtOy0dy1Agp8vkySQg', 'UCMwGHR0BTZuLsmjY_NT5Pwg', 'UCoSrY_IQQVpmIRZ9Xf-y93g', 'UCyl1z3jo3XHR1riLFKG5UAg', 'UCAoy6rzhSf4ydcYjJw3WoVg',
                               'UCOyYb1c43VlX9rc_lT6NKQw', 'UCP0BspO_AMEe3aQqqpo89Dg', 'UC727SQYUvx5pDDGQpTICNWg', 'UChgTyjG-pdNvxxhdsXfHQ5Q', 'UCYz_5n-uDuChHtLo7My1HnQ',
                               'UC6t3-_N8A6ME1JShZHHqOMw', 'UC9mf_ZVpouoILRY9NUIaK-w', 'UCKeAhJvy8zgXWbh9duVjIaQ', 'UCZgOv3YDEs-ZnZWDYVwJdmA', 'UCANDOlYTJT7N5jlRC3zfzVA',
                               'UCGNI4MENvnsymYjKiZwv9eg', 'UCNVEsYbiZjH5QLmGeSgTSzg', 'UChSvpZYRPh0FvG4SJGSga3g', 'UCwL7dgTxKo8Y4RFIKWaf8gA', 'UCEzsociuFqVwgZuMaZqaCsg',
                               'UCgNVXGlZIFK96XdEY20sVjg', 'UCgZuwn-O7Szh9cAgHqJ6vjw', 'UCsehvfwaWF6nWuFnXI0AqZQ']

manual_channel_blacklist = ['UCMcBvfofbiimdj3uGqoFlww', 'UCi7GJNg51C3jgmYTUwqoUXA', 'UCNWIN_bb9gB3KWEaeHpP8nA', 'UCVi2lI40LetxLBKn-rtWC3A', 'UCeijqgCP9z3zLJ-uwQzvFtQ', 'UC-JSeFfovhNsEhftt1WHMvg', 'UChc76D7x_mbLNoaCHJAOOyQ']

manual_video_blacklist = ['xtqO80ir0yI']

talent_data = get_talent_data()


def score_videos(videos, search_tags=True):
    def calc_name_score(category):
        amount = name_worth[category] * (1 - (name_counts[category] * name_count_exponent[category]))

        if amount < 0:
            return 0
        else:
            return amount

    def keyword_exists(v, words, check_title=True, check_description=True, check_tags=True):

        tags_string = ''
        if search_tags:
            tags = list(v['video_tags'])
            tags_lower = list(map(lambda x: x.lower(), tags))
            tags_string = ' '.join(tags_lower)

        if check_title:
            if any(re.search(rf"\b{t}\b", v['video_title'].lower()) for t in words):
                return True

        if check_description:
            if any(re.search(rf"\b{t}\b", v['video_description'].lower()) for t in words):
                return True

        if search_tags:
            if check_tags:
                if any(re.search(rf"\b{t}\b", tags_string) for t in words):
                    return True

        return False

    name_title_matches = 0
    name_description_matches = 0
    name_tag_matches = 0

    to_remove = []
    to_remove_json = []

    scores = {}

    for vid in videos:
        v = vid

        if not search_tags:
            v = videos[vid]

        holo_related_exists = keyword_exists(v, holo_related_keywords)
        score = 0.0

        channel_id = ''
        if 'channel_id' in v.keys():
            channel_id = v['channel_id']
        else:
            channel_id = v['video_channel_hm'][-24:]

        found_names = {}

        name_counts = {
            "title": 0,
            "description": 0,
            "tags": 0
        }

        matches = {
            "hololive": False,
            "vtuber": False,
            "translation": False
        }

        tags_string = ''

        if search_tags:
            tags = list(v['video_tags'])
            tags_lower = list(map(lambda x: x.lower(), tags))
            tags_string = ' '.join(tags_lower)

        for talent_name, aliases in talent_data.items():
            filtered_aliases = list(filter(lambda x: (len(x) > 3), aliases))
            short_aliases = list(set(aliases) - set(filtered_aliases))

            if re.search(rf"\b{talent_name}\b", v['video_title'].lower()) or any(re.search(rf"\b{alias}\b", v['video_title'].lower()) for alias in filtered_aliases):
                category = 'title'
                score += calc_name_score(category)
                name_counts[category] += 1
                name_title_matches += 1
                found_names[talent_name] = True

            else:
                if len(short_aliases) > 0:
                    for a in short_aliases:
                        if re.search(rf"\b{a}\b", v['video_title'].lower()) and holo_related_exists:
                            category = 'title'
                            score += calc_name_score(category)
                            name_counts[category] += 1
                            name_title_matches += 1
                            found_names[talent_name] = True

                            # print("!!!Title Short Alias {} granted on {}".format(a, v['video_title']))

            if re.search(rf"\b{talent_name}\b", v['video_description'].lower()) or any(re.search(rf"\b{alias}\b", v['video_description'].lower()) for alias in filtered_aliases):
                category = 'description'
                score += calc_name_score(category)
                name_counts[category] += 1
                name_description_matches += 1
                found_names[talent_name] = True

            else:
                if len(short_aliases) > 0:
                    for a in short_aliases:
                        if re.search(rf"\b{a}\b", v['video_description'].lower()) and holo_related_exists:
                            category = 'description'
                            score += calc_name_score(category)
                            name_counts[category] += 1
                            name_title_matches += 1
                            found_names[talent_name] = True

                            # print("!!!Description Short Alias {} granted on {}".format(a, v['video_title']))

            if search_tags:
                if re.search(rf"\b{talent_name}\b", tags_string) or any(re.search(rf"\b{alias}\b", tags_string) for alias in filtered_aliases):
                    category = 'tags'
                    score += calc_name_score(category)
                    name_counts[category] += 1
                    name_tag_matches += 1
                    found_names[talent_name] = True

                else:
                    if len(short_aliases) > 0:
                        for a in short_aliases:
                            if re.search(rf"\b{a}\b", tags_string) and holo_related_exists:
                                category = 'tags'
                                score += calc_name_score(category)
                                name_counts[category] += 1
                                name_title_matches += 1
                                found_names[talent_name] = True


        name_count_sum = name_counts['title'] + name_counts['description']

        if search_tags:
            name_count_sum += name_counts['tags']

        if name_count_sum > 1:
            for k in keywords:
                if any(t in v['video_title'].lower() for t in k['list']):
                    score += k['worth']['title']
                    matches[k['category']] = True

                if any(t in v['video_description'].lower() for t in k['list']):
                    score += k['worth']['description']
                    matches[k['category']] = True

                if search_tags:
                    if any(t in tags_string for t in k['list']):
                        score += k['worth']['tags']
                        matches[k['category']] = True

        if name_count_sum > 1 or holo_related_exists:
            if any(t in v['video_title'].lower() for t in translation_keywords):
                score += translation_worth['title']

                if holo_related_exists:
                    score += 5.0

            if any(t in v['video_description'].lower() for t in translation_keywords):
                score += translation_worth['description']

            if search_tags:
                if any(t in tags_string for t in translation_keywords):
                    score += translation_worth['tags']

        # Disqualifiers

        if name_count_sum == 0 and keyword_exists(v, no_name_blacklist):
            score = -1.0

        if channel_id in official_channels_blacklist or channel_id in manual_channel_blacklist:
            score = -1.0

        if v['video_id'] in manual_video_blacklist:
            score = -1.0

        # Videos about actual festivals
        if len(found_names) == 1 and 'Natsuiro Matsuri' in found_names.keys():
            if not keyword_exists(v, ['natsuiro', 'matsuri\'s'] + holo_related_keywords):
                score = -1.0

            elif not holo_related_exists and keyword_exists(v, ['Ume Matsuri', 'haikyuu']):
                score = -1.0

        if not holo_related_exists and keyword_exists(v, ['della luna', 'del luna']):
            score = -1.0

        if keyword_exists(v, ['live wallpaper'], check_description=False):
            score = -1.0

        # Subaru Outback
        if len(found_names) == 1 and 'Oozora Subaru' in found_names.keys():
            if keyword_exists(v, ['subaru outback']):
                score = -1.0

        scores[v['video_id']] = score

    return scores


def filter_videos_by_score(videos, threshold=10.0):
    scores = score_videos(videos)
    filtered = []

    for k, v in videos.items():
        if scores[k] >= threshold:
            videos[k]['score'] = scores[k]
            filtered.append(videos[k])
        else:
            print('Filtered Out (2): {}\t{}'.format(v['video_id'], v['video_title']))

    return filtered
