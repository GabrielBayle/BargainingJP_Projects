from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'vuetest'
    players_per_group = None
    num_rounds = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bidder = models.IntegerField()
    highest_bid = models.CurrencyField(initial=0)

class Player(BasePlayer):
    def live_auction(self, bid):
        group = self.group
        my_id = self.id_in_group
        if bid > group.highest_bid:
            group.highest_bid = bid
            group.highest_bidder = my_id
            response = dict(id_in_group=my_id, bid=bid)
            return {0: response}
