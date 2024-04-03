from os import environ


SESSION_CONFIGS = [
    {
        'name': 'bargain',
        'display_name': "Bargain",
        'app_sequence':['live_bargaining','targetNLE','svo','compute_payoffs'],
        'num_demo_participants':2,
        'treatment':'test',
        'order':1,
        'targetNLE_constante':3,
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
    )
]


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'zqsdexpceem2024'
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
DEBUG =False


DEMO_PAGE_INTRO_HTML = """ """
DEMO_PAGE_TITLE = ""


SECRET_KEY = '4387860144726'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = []

SESSION_FIELDS = []
