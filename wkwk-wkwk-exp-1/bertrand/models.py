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


doc = """
2 firms complete in a market by setting prices for homogenous goods.

See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    players_per_group = 2
    name_in_url = 'bertrand'
    num_rounds = 1

    instructions_template = 'bertrand/instructions.html'

    maximum_price = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    winning_price = models.CurrencyField()

    def set_payoffs(self):
        import random

        players = self.get_players()
        self.winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == self.winning_price]
        winner = random.choice(winners)

        for p in players:
            if p == winner:
                p.is_winner = True
                p.payoff = p.price
            else:
                p.is_winner = False
                p.payoff = c(0)


class Player(BasePlayer):
    price = models.CurrencyField(
        min=0,
        max=Constants.maximum_price,
        doc="""Price player offers to sell product for""",
        label="Please enter an amount from 0 to 100 as your price"
    )

    is_winner = models.BooleanField()
