
from otree.api import *
import random

author = 'Francisco Klapp'
doc = """
This app implements the questionnaire and ethical survey for the  common value auction experiment , where sellers can 
send a costly signal. Sellers are exposed to an ethical statement treatment
"""


class Constants(BaseConstants):
    name_in_url = 'InvQuestionnaire'
    players_per_group = None  # For testing and actual experiment
    num_rounds = 1  # For testing and actual experiment
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Variables used by individual players
    # Questionnaire variables

    age = models.IntegerField(min=16, max=99)
    sex = models.StringField(
        widget=widgets.RadioSelectHorizontal,
        choices=['Male', 'Female', 'Non-Binary'],
    )
    # major = models.StringField()

    major = models.IntegerField(
        choices=[
            [1, "Arts"],
            [2, "Biological Science"],
            [3, "Business"],
            [4, "Education"],
            [5, "Engineering"],
            [6, "Humanities"],
            [7, "Information & Computer Sciences"],
            [8, "Interdisciplinary Studies"],
            [9, "Nursing Sciences"],
            [10, "Pharmaceutical Sciences"],
            [11, "Physical Sciences"],
            [12, "Public Health"],
            [13, "Social Ecology"],
            [14, "Social Sciences"],
            [15, "other STEM"],
            [17, "other non-STEM"],
            [17, "Undeclared"],
        ],
        label="Field of Study"
    )


    GPA = models.FloatField(min=0, max=4)
    race = models.StringField(
        choices=['Asian or Pacific Islander', 'Black or African American', 'Hispanic or Latino',
                 'Native American or Alaskan Native', 'White or Caucasian', 'Multiracial or Biracial',
                 'A race/ethnicity not listed here']
    )
    #risk = models.IntegerField(
    #    widget=widgets.RadioSelectHorizontal,
    #    choices=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
   # )

    risk1 = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="1.   In general, how willing are you to take risks?",
        choices=[
        [0, " 0 "],
        [1, " 1 "],
        [2, " 2"],
        [3, " 3"],
        [4, " 4"],
        [5, " 5"],
        [6, " 6"],
        [7, " 7"]

    ]
    )

    risk2 = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="2.   How willing are you to give up something that is beneficial for you today in order to benefit more from that in the future?",
        choices=[
            [0, " 0 "],
            [1, " 1 "],
            [2, " 2"],
            [3, " 3"],
            [4, " 4"],
            [5, " 5"],
            [6, " 6"],
            [7, " 7"]

        ]
    )

    competitive = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        
        choices=[
            [0, " 0 "],
            [1, " 1 "],
            [2, " 2"],
            [3, " 3"],
            [4, " 4"],
            [5, " 5"],
            [6, " 6"],
            [7, " 7"]
         
        ]
    )

 #   propensity1 = models.IntegerField(
#        widget=widgets.RadioSelectHorizontal,
  #      choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
   #              [5, 'Agree strongly']],
   # )

    #propensity2 = models.IntegerField(
     #   widget=widgets.RadioSelectHorizontal,
     #   choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
      #           [5, 'Agree strongly']],
    #)

   # propensity3 = models.IntegerField(
   #    widget=widgets.RadioSelectHorizontal,
   #     choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
   #             [5, 'Agree strongly']],
   # )

   # propensity4 = models.IntegerField(
   #     widget=widgets.RadioSelectHorizontal,
   #     choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
   #              [5, 'Agree strongly']],
   # )

  #  propensity5 = models.IntegerField(
  #      widget=widgets.RadioSelectHorizontal,
  #      choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
  #               [5, 'Agree strongly']],
  #  )

  #  propensity6 = models.IntegerField(
  #      widget=widgets.RadioSelectHorizontal,
  #      choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
  #               [5, 'Agree strongly']],
  #  )

   # propensity7 = models.IntegerField(
   #     widget=widgets.RadioSelectHorizontal,
   #     choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
  #               [5, 'Agree strongly']],
 #   )
#
 #   propensity8 = models.IntegerField(
 #       widget=widgets.RadioSelectHorizontal,
 #       choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
 #                [5, 'Agree strongly']],
 #   )

    open_question = models.LongStringField(
        blank=True
    )

    math_classes = models.IntegerField(min=0, max=99)

    stats_classes = models.IntegerField(min=0, max=99)

    econ_classes = models.IntegerField(min=0, max=99)

    CRT1 = models.IntegerField(
        label="11.   If John can drink one barrel of water in 6 days, and Mary can drink one barrel of water in 12 days, how many days would it take them to drink one barrel of water together?", min=0, max=99
    )

    CRT2 = models.IntegerField(
        label="12.   Jerry received both the 15th highest and the 15th lowest mark in the class. How many students are in the class? ", min=0, max=99
    )

    CRT3 = models.IntegerField(
        label="13.   A man buys a pig for $60, sells it for $70, buys it back for $80, and sells it finally for $90. How much ($) has he made?  ", min=0, max=99
    )

    CRT4 = models.IntegerField(
        label="14.   Simon decided to invest $8,000 in the stock market one day early in 2008. Six months after he invested, on July 17, the stocks he had purchased were down 50%. Fortunately for Simon, from July 17 to October 17, the stocks he had purchased went up 75%. At this point, Simon has:  ",
        widget=widgets.RadioSelect,
        choices=[
            [1, "broke even in the stock market"],
            [2, "is ahead of where he began"],
            [3, "has lost money "]
    ]
    )





# PAGES


class Questionnaire1(Page):

    form_model = 'player'
    form_fields = ['age', 'sex', 'major', 'race', 'GPA', 'risk1', 'risk2', 'competitive', 'math_classes', 'stats_classes', 'econ_classes']


class Questionnaire2(Page):

    form_model = 'player'
   # form_fields = ['propensity1', 'propensity2', 'propensity3', 'propensity4', 'propensity5', 'propensity6',
    #               'propensity7', 'propensity8']
    form_fields = ['CRT1', 'CRT2', 'CRT3', 'CRT4']


class Questionnaire3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['open_question'] == 'yes'
    form_model = 'player'
    form_fields = ['open_question']


class FinalResults(Page):
    # timeout_seconds = 25

  #  @staticmethod
  #  def is_displayed(player: Player):
  #      return player.round_number <= player.session.config['num_rounds'] and \
  #             ((player.round_number == player.session.config['num_rounds'] and player.is_playing) or
  #              (player.is_out is True and player.in_round(player.round_number-1).is_playing is True))


    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            payoff_plus_participation_fee=player.participant.payoff_plus_participation_fee(),
            total_earnings=float(player.participant.payoff*player.session.config['us_exchange_rate']),
            show_up_fee=float(player.session.config['participation_fee']),
            total_earnings_US=float(player.participant.payoff),
            total_payoff_US=float(player.participant.payoff_plus_participation_fee()),
           
            us_exchange_rate=player.session.config['us_exchange_rate'],
            num_rounds=player.session.config['num_supergames'],
            pressure=player.session.config['pressure']
        )



page_sequence = [Questionnaire1,
                 Questionnaire2,
                 Questionnaire3,
                 FinalResults]
