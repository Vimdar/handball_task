TEST_DATA = {
    'first_country': {
        'country_name': "Bulgaria",
        'wins': 1,
        'opponents': ['Austria'],
    },
    'second_country': {
        'country_name': "Italy",
        'wins': 1,
        'opponents': ['Belgium'],
    },
    'third_country': {
        'country_name': "Bulgaria",
        'wins': 1,
        'opponents': ['Netherlands'],
    },
    'fourth_country': {
        'country_name': "Bulgaria",
        'wins': 2,
        'opponents': ['Austria', 'Netherlands'],
    },
    'fifth_country': {
        'country_name': "Netherlands",
        'wins': 0,
        'opponents': ['Bulgaria'],
    },
    'sixth_country': {
        'country_name': "Italy",
        'wins': 1,
        'opponents': ['Belgium', 'England'],
    },
    'seventh_country': {
        'country_name': "England",
        'wins': 1,
        'opponents': ['Italy'],
    },
}

TEST_SCORES = {
    'first': ['5:0', '0:0'],
    'second': ['1:0', '3:0'],
    'third': ['0:0', '1:1'],
    'fourth': ['2:2', '1:1'],
}

TEST_LINES = {
    'first': 'Denmark | Belgium | 0:0 | 1:1',
    'second': 'Malta | Bulgaria | 0:5 | 3:3'
}

TEST_RESULTS = {
    'first': (
        {'country_name': 'Denmark',
         'opponents': ['Belgium'],
         'wins': 1,
         },
        {'country_name': 'Belgium',
         'opponents': ['Denmark'],
         'wins': 0,
         }
    ),
    'second': (
        {'country_name': 'Malta',
         'opponents': ['Bulgaria'],
         'wins': 0,
         },
        {'country_name': 'Bulgaria',
         'opponents': ['Malta'],
         'wins': 1,
         },
    )

}

EXAMPLE_LISTING = {
    'first': [
        {
            "country_name": "Belgium",
            "wins": 1,
            "opponents": [
                "Denmark",
                "Austria"
            ]
        },
        {
            "country_name": "Bulgaria",
            "wins": 1,
            "opponents": [
                "Italy"
            ]
        },
        {
            "country_name": "Denmark",
            "wins": 1,
            "opponents": [
                "Belgium"
            ]
        },
        {
            "country_name": "Latvia",
            "wins": 1,
            "opponents": [
                "Monaco"
            ]
        },
        {
            "country_name": "Austria",
            "wins": 0,
            "opponents": [
                "Belgium"
            ]
        },
        {
            "country_name": "Italy",
            "wins": 0,
            "opponents": [
                "Bulgaria"
            ]
        },
        {
            "country_name": "Monaco",
            "wins": 0,
            "opponents": [
                "Latvia"
            ]
        }
    ],
    'second': [
        {
            "country_name": "Montenegro",
            "wins": 3,
            "opponents": [
                "Cyprus",
                "Bosnia",
                "South Africa"
            ]
        },
        {
            "country_name": "Bosnia",
            "wins": 0,
            "opponents": [
                "Montenegro"
            ]
        },
        {
            "country_name": "Cyprus",
            "wins": 0,
            "opponents": [
                "Montenegro"
            ]
        },
        {
            "country_name": "South Africa",
            "wins": 0,
            "opponents": [
                "Montenegro"
            ]
        }
    ],
    'third': [
        {
            "country_name": "Germany",
            "wins": 1,
            "opponents": [
                "Brazil"
            ]
        },
        {
            "country_name": "Brazil",
            "wins": 0,
            "opponents": [
                "Germany"
            ]
        }
    ],
}

TEST_POST_DATA = {
    'first': 'Denmark | Belgium | 0:0 | 1:1\nBelgium | Austria | 2:0 | 0:2\nLatvia | Monaco | 2:0 | 0:0\nBulgaria | Italy | 2:1 | 3:2\nstop',
    'second': 'Montenegro | Cyprus | 0:0 | 1:1\nMontenegro | Bosnia | 0:0 | 1:1\nMontenegro | South Africa | 0:0 | 1:1\nstop',
    'third': 'Brazil | Germany | 1:1 | 7:0\nstop',
}

TEST_POST_RESPONSE = [
    {
        "country_name": "Bulgaria",
        "wins": 1,
        "opponents": ["Netherlands"]
    },
    {
        "country_name": "Netherlands",
        "wins": 0,
        "opponents": ["Bulgaria"]
    }
]
