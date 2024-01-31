from os import environ


SESSION_CONFIGS = [
    {
        'name': 'bargain',
        'display_name': "Bargain",
        'app_sequence':['live_bargaining'],
        'num_demo_participants':2,
        'treatment':'test',
        'order':1,
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=500, doc="")

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

ROOMS = [
    dict(
        name='Waseda_experiment_Bargaining_2024',
        display_name='Waseda_experiment_Bargaining_2024',
        #participant_label_file='econ101.txt',
    )
]


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'klapp1275'
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
DEBUG =False # to get rid of debug!


DEMO_PAGE_INTRO_HTML = """ """
DEMO_PAGE_TITLE = ""


SECRET_KEY = '4387860144726'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = [
    'booking_time',
    'cards',
    'order',
    'reaction_times',
    'read_mind_in_eyes_score',
    'responses',
    'stimuli',
    'svo_angle',
    'svo_category',
]

SESSION_FIELDS = [
     'finished_p1_list', 'iowa_costs', 'wisconsin', 'intergenerational_history'
    ]
