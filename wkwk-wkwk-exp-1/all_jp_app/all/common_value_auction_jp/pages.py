from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def before_next_page(self):
        self.player.item_value_estimate = self.group.generate_value_estimate()


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'


class Results(Page):
    def vars_for_template(self):
        return dict(is_greedy=self.group.item_value - self.player.bid_amount < 0)


page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
