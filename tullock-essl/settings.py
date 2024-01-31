from os import environ


SESSION_CONFIGS = [
    {
        'name': 'bargain',
        'display_name': "Bargain",
        'app_sequence':['live_bargaining'],
        'num_demo_participants':2
    },

     {
        'name': 'tullock_3',
        'display_name': "Test version: 3-player Tullock Contest, 1 total supergames - only to show decision page",
        'app_sequence':['tullock_supergames_indefinite', 'Tullock_questionnaire'],

        # to select treatments
         'pressure': True,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':3,
         'num_supergames': 1,               # to choose the number of supergames outside the constants
         'num_active_participants': 3,    # players participating in contest in each round
         'buffer_size':2,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters

        'supergames':[20,2,12,7,6,24,17,3,3,3,3],

 },

 {
        'name': 'tullock_7a',
        'display_name': "Test version: 3-player Tullock Contest, 5 total supergames- full features - pressure",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': True,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':7,
         'num_supergames': 5,               # to choose the number of supergames outside the constants
         'num_active_participants': 3,    # players participating in contest in each round
         'buffer_size':2,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },

  {
        'name': 'tullock_7b',
        'display_name': "Test version: 4-player Tullock Contest, 5 total supergames- full features - pressure",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': True,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':7,
         'num_supergames': 5,               # to choose the number of supergames outside the constants
         'num_active_participants': 4,    # players participating in contest in each round
         'buffer_size':2,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },



  {
        'name': 'tullock_7a_random',
        'display_name': "Test version: 3-player Tullock Contest, 5 total supergames- full features - random",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': False,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':7,
         'num_supergames': 5,               # to choose the number of supergames outside the constants
         'num_active_participants': 3,    # players participating in contest in each round
         'buffer_size':2,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },

  {
        'name': 'tullock_7b_random',
        'display_name': "Test version: 4-player Tullock Contest, 5 total supergames- full features - random",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': False,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':7,
         'num_supergames': 5,               # to choose the number of supergames outside the constants
         'num_active_participants': 4,    # players participating in contest in each round
         'buffer_size':2,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },

  {
        'name': 'tullock_14',
        'display_name': "--> Full version: 4-player Tullock Contest, 11 total supergames- full features - pressure",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': True,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':14,
         'num_supergames': 11,               # to choose the number of supergames outside the constants
         'num_active_participants': 4,    # players participating in contest in each round
         'buffer_size':4,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },

 {
        'name': 'tullock_14_random',
        'display_name': "--> Full version: 4-player Tullock Contest, 11 total supergames- full features - random",
        'app_sequence':['tullock_supergames_indefinite','Tullock_questionnaire'],

        # to select treatments
         'pressure': False,                 # pressure treatment (instead of random selection)

        # General Parameters
         'num_demo_participants':14,
         'num_supergames': 11,               # to choose the number of supergames outside the constants
         'num_active_participants': 4,    # players participating in contest in each round
         'buffer_size':4,                 # players reading instructions waiting to enter

         'stop_prob':1/10,            #probability of stopping  round in the sequence
         'us_exchange_rate': 20,           #exchange rate for points
         'duration':180,                     #expected game duration (in minutes)
         'open_question':'yes',           # open question at the end

         # parameters for Tullock contest
         'endowment':100,     # for every contest round
         'r':1,              # function power parameter
         'V':100,              # winner's prize
         'tlimit': 0.5,           #  minutes for soft timer

                # replacement parameters
        'supergames':[2,2,12,7,6,24,17,3,3,3,3],

 },
 
 
 
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=10.00, doc="")

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

ROOMS = [
    dict(
        name='ESSL_experiment_2022',
        display_name='ESSL_experiment_2022',
        participant_label_file='econ101.txt',
    )
]


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'L$'
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
