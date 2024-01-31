from os import environ

SESSION_CONFIGS = [
    # dict(
    #    name='public_goods',
    #    display_name="Public Goods",
    #    num_demo_participants=3,
    #    app_sequence=['public_goods', 'payment_info']
    # ),
    # dict(
    #     name='vuetest',
    #     display_name='vuetest',
    #     num_demo_participants=2,
    #     app_sequence=['vuetest']
    # ),
    dict(
        name = 'doubleauction',
        display_name='ダブルオークション (Double Action)',
        num_demo_participants = 3,
        app_sequence=['doubleauction']
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
REAL_WORLD_CURRENCY_DECIMAL_PLACES=0
USE_POINTS = False

ROOMS = [
    dict(
    name='doubleauction',
    display_name='ダブルオークション (Double Action)',
    participant_label_file='_rooms/double_auction.txt',
    use_secure_urls=False
    ),
]

DEBUG = True

AUTH_LEVEL='DEMO'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'economics2020'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '$6_2#@aaykvqw#9mz8k_7$t7wn!k05tq2r)lmb(e8ly=ku)i!v'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
