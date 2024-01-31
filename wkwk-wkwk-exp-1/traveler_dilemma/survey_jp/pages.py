from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3','question4' ,'question5']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['breakout', 'question6', 'question7', 'question8','question9' ,'question10']


page_sequence = [Demographics, CognitiveReflectionTest]

