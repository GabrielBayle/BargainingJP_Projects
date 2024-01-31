from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class first_waitPage(WaitPage):
    after_all_players_arrive= 'allotment'

class Instruction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Plantime(Page):
    timeout_seconds=300
    def is_displayed(self):
        return self.subsession.round_number == 1

class waitPage(WaitPage):
    pass

class Game(Page):
    timeout_seconds = 360
    live_method = 'live_auction'

class Result(Page):
    timeout_seconds = 90
    def js_vars(self):
        amount = []
        money  = []
        utility = []
        partner = []
        diff_amount = [0]
        diff_money = [0]
        unit_of_price = []
        history_amount_list = self.player.history_amount.split(',')
        print(self.player.history_money)
        history_money_list  = self.player.history_money.split(',')
        history_utility_list= self.player.history_utility.split(',')
        history_partner_list= self.player.history_partner.split(',')
        history_amount_list.pop(-1)
        history_money_list.pop(-1)
        history_utility_list.pop(-1)
        history_partner_list.pop(-1)
        for i in history_amount_list:
            amount.append(int(i))
        for i in history_money_list:
            money.append(int(i))
        for i in history_utility_list:
            utility.append(float(i))
        for i in history_partner_list:
            partner.append(int(i))
        for i in range(len(amount)-1):
            diff_amount.append(amount[i+1]-amount[i])
        for i in range(len(money)-1):
            diff_money.append(money[i+1]-money[i])
        for i in range(len(diff_amount)):
            if diff_amount[i] == 0:
                unit_of_price.append(0)
            else:
                unit_of_price.append(format(abs(diff_money[i]/diff_amount[i]),'.2f'))

        print(unit_of_price)

        return dict(
            traded_numbers = [i for i in range(len(amount))],
            diff_amounts   = diff_amount,
            diff_moneys    = diff_money,
            unit_of_prices = unit_of_price,
            partners       = partner,
            amounts        = amount,
            moneys        = money,
            utilitys      = utility,
        )

class Endwait(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
    after_all_players_arrive= 'func_chosen_utility'

class End(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def js_vars(self):
        lank_list = {}
        for p in self.group.get_players():
            lank_list[p.id_in_group] = p.in_all_rounds()[p.chosen_round-1].utility
            print(lank_list)
        return dict(lank_list=lank_list)




page_sequence = [first_waitPage, Instruction,Plantime, waitPage ,Game, Result,Endwait, End]
