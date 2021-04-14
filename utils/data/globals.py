official_channels_blacklist = ['UCJFZiqLMntJufDCHc6bQixg', 'UCfrWoRGlawPQDQxxeIDRP0Q', 'UCotXwY6s8pWmuWd_snKYjhg', 'UCWsfcksUUpoEvhia0_ut0bA', 'UCp6993wxpyDPHUpavwDFqgg', ' UCDqI2jOz0weumE8s7paEk6g',
                               'UC0TXe_LYZ4scaW2XMyi5_kw', 'UC5CwaMl1eIgY8h02uZw7u8A', 'UC-hM6YJuNYVAmUWxeIr9FeA', 'UC1CfXB_kRs3C-zaeTG3oGyg', ' UCD8HOxPs4Xvsm8H0ZxXGiBw', 'UCdn5BQ06XqgXoAxIhbqw5Rg',
                               'UCFTLzh12_nrtzqBPsTCqenA', 'UCQ0UDLQCjY0rmuxCDE38FGg', 'UCHj_mh57PVMXhAUDphUQDFA', ' UCLbtM3JZfRTg8v2KGag-RMw', 'UC1opHUrw8rvnsadT-iGp7Cg', 'UC1suqwovbL1kzsoaZgFZLKg',
                               'UC7fk0CB07ly8oSl0aqKkqFg', 'UCvzGlP9oQwU--Y0r9id_jnA', ' UCXTpFs_3PqI41qX2d9tL2Rw', 'UCp3tgHXw_HI0QMk1K8qh3gQ', 'UChAnqc_AY5_I3Px5dig3X1Q', 'UCp-5t9SrOQwXMU7iIjQfARg',
                               'UCvaTdHTWBGv3MKj3KVqJVCw', ' UC1DCedRgGHBdm81E1llLhOQ', 'UCCzUftO8KOVkV4wQG1vkUvg', 'UCdyqAaZDKHXg4Ahi7VENThQ', 'UCl_gCybOJRIgOXw6Qb4qJzQ', 'UCvInZx9h3jC2JzsIzoOebWg',
                               ' UC1uv2Oq6kNxgATlCiez59hw', 'UCa9Y57gfeY0Zro_noHRVrnw', 'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCS9uQI-jC3DE0L4IpXyvr6w', 'UCZlDXzGoo7d44bwdNObFacg', ' UCAWSyEs_Io8MtpY3m-zqILA',
                               'UCFKOVgVbGmX65RxO3EtH3iw', 'UCK9V2B22uJYu3N7eR_BT9QA', 'UCUKD-uaobj9jiqB-VXt71mA', 'UCHsx4Hqa-1ORjQTh9TYDhww', ' UCL_qhgtOy0dy1Agp8vkySQg', 'UCMwGHR0BTZuLsmjY_NT5Pwg',
                               'UCoSrY_IQQVpmIRZ9Xf-y93g', 'UCyl1z3jo3XHR1riLFKG5UAg', 'UCAoy6rzhSf4ydcYjJw3WoVg', ' UCOyYb1c43VlX9rc_lT6NKQw', 'UCP0BspO_AMEe3aQqqpo89Dg', 'UC727SQYUvx5pDDGQpTICNWg',
                               'UChgTyjG-pdNvxxhdsXfHQ5Q', 'UCYz_5n-uDuChHtLo7My1HnQ', ' UC6t3-_N8A6ME1JShZHHqOMw', 'UC9mf_ZVpouoILRY9NUIaK-w', 'UCKeAhJvy8zgXWbh9duVjIaQ', 'UCZgOv3YDEs-ZnZWDYVwJdmA',
                               'UCANDOlYTJT7N5jlRC3zfzVA', ' UCGNI4MENvnsymYjKiZwv9eg', 'UCNVEsYbiZjH5QLmGeSgTSzg', 'UChSvpZYRPh0FvG4SJGSga3g', 'UCwL7dgTxKo8Y4RFIKWaf8gA', 'UCEzsociuFqVwgZuMaZqaCsg',
                               ' UCgNVXGlZIFK96XdEY20sVjg', 'UCgZuwn-O7Szh9cAgHqJ6vjw', 'UCsehvfwaWF6nWuFnXI0AqZQ']

manual_channel_blacklist = ['UCMcBvfofbiimdj3uGqoFlww', 'UCi7GJNg51C3jgmYTUwqoUXA', 'UCNWIN_bb9gB3KWEaeHpP8nA', 'UCVi2lI40LetxLBKn-rtWC3A', 'UCeijqgCP9z3zLJ-uwQzvFtQ', 'UC-JSeFfovhNsEhftt1WHMvg',
                            'UChc76D7x_mbLNoaCHJAOOyQ']

manual_video_blacklist = ['xtqO80ir0yI', 'lSCZ5r6HntI']


retired_keywords = ['yakushiji', 'suzaku', 'tsukishita', 'kaoru', 'kagami', 'kira', 'hitomi', 'chris', 'mano', 'aloe']

# Blacklist if also doesn't have a talent match
no_name_blacklist = ['nijisanji']

holo_related_keywords = ['hololive', 'holo live',
                         'holoen', 'holo en', 'hololiveen',
                         'holoid', 'holo id', 'hololiveid',
                         'holostars', 'holo stars',
                         'hololiveclips', 'hololiveclip']

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
        "list": ['okakoro', 'mioshuba', 'noefure', 'shishilamy'],
        "worth": {
            "title": 5,
            "description": 5,
            "tags": 5
        }
    }
]

translation_keywords = ['engsub','eng sub', 'english sub', 'sub eng', 'holoengsubs']
translation_worth = {
    "title": 10,
    "description": 6,
    "tags": 8
}

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
