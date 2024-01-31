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
import numpy as np


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'doubleauction'
    players_per_group = None
    num_rounds = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    history_trade_price = models.LongStringField(initial='')
    history_trade_amount = models.LongStringField(initial='')
    history_trade_bidder = models.LongStringField(initial='')
    history_trade_asker = models.LongStringField(initial='')
    history_all_bid_price = models.LongStringField(initial='')
    history_all_bid_amount = models.LongStringField(initial='')
    history_all_ask_price = models.LongStringField(initial='')
    history_all_ask_amount = models.LongStringField(initial='')
    history_all_bidder = models.LongStringField(initial='')
    history_all_asker = models.LongStringField(initial='')

    def allotment(self):
        for p in self.get_players():
            p.allot_role()
            if p.roll == '1-A-F':
                p.amount = 25 #X
                p.money = 1   #Y
            elif p.roll == '2-G-L':
                p.amount = 5  #X
                p.money = 29  #Y
            p.utility = p.utility_cal(p.roll,p.id_in_group)
            p.history_money += str(p.money) + ','
            p.history_amount += str(p.amount) + ','
            p.history_utility += str(p.utility) + ','

    def func_chosen_utility(self):
        for p in self.get_players():
            # p.chosen_round = np.random.randint(1, Constants.num_rounds)
            # print(p.chosen_round)
            p.chosen_utility = p.in_all_rounds()[p.chosen_round-1].utility



class Player(BasePlayer):
    money = models.IntegerField(initial=0)
    amount = models.IntegerField(initial=0)
    utility = models.FloatField(initial=0)
    chosen_utility = models.FloatField()
    chosen_round = models.IntegerField(initial=np.random.randint(1, 5)) #鯖を立ち上げた時に決まる
    history_bid = models.LongStringField(initial='')
    history_ask = models.LongStringField(initial='')
    history_money = models.LongStringField(initial='')
    history_amount = models.LongStringField(initial='')
    history_utility = models.LongStringField(initial='')
    history_partner = models.LongStringField(initial='0,')
    roll = models.StringField()



    def allot_role(self):
        # for p in self.group.get_players():
        #     print(p.id_in_group % 2)
        if self.id_in_group <= 10:
            self.roll = '1-A-F'
        elif self.id_in_group > 10:
            self.roll = '2-G-L'

    def utility_cal(self, role, id): #excelのcel番号準拠
        E38 = 1/9.8                         #a1
        E39 = 10.5                          #b1
        E40 = 6.2                           #c1
        E41 = 7.5                           #d1
        E42 = 14.9                          #e1
        G38 = 1/9.1                         #a2
        G39 = 11.3                          #b2
        G40 = 7.35                          #c2
        G41 = 8                             #d2
        G42 = 17.45                         #e2
        G43 = 18.45                         #g2
        Q38 = 1000                          #Ue
        Q39 = 2000                          #Ueq2
        V38 = 1                             #u1e
        V39 = 0.549450549                   #u2e
        I40 = 1                             #n1
        K40 = 1                             #n2
        Y38 = 14.74183673                   #u1eq2
        Y39 = 15                            #u2eq2
        I38 = (Q39-Q38)/(Y38**I40-V38**I40) #m1
        I39 = Q38-I38*V38**I40              #k1
        K38 = (Q39-Q38)/(Y39**K40-V39**K40) #m2
        K39 = Q38-K38*V39**K40              #k2
        P40 = 1.384                         #t
        AA38= 9                             #eq1
        AA39= 8.812032967                   #eq1
        AB38= 21
        AB39= 21
        print(I38)
        print(I39)
        print(K38)
        print(K39)

        if role == '1-A-F':
            #a1 = 52.58
            #b1 = 669.96
            if self.group.get_player_by_id(id).amount >= 0 and self.group.get_player_by_id(id).amount <= E40:
                utility = (I38 * min(E38*self.group.get_player_by_id(id).amount, self.group.get_player_by_id(id).money)**I40 + I39) / P40
            elif self.group.get_player_by_id(id).amount > E40 and self.group.get_player_by_id(id).amount <= E41:
                utility = (I38 * min(E39*self.group.get_player_by_id(id).amount+(E38-E39)*E40, self.group.get_player_by_id(id).money)**I40 + I39) / P40
            elif self.group.get_player_by_id(id).amount > E41 and self.group.get_player_by_id(id).amount <= E42:
                utility = (I38 * min(E38*self.group.get_player_by_id(id).amount+(E38-E39)*(E40-E41), self.group.get_player_by_id(id).money)**I40 + I39) / P40
            else:
                utility = (I38 * min(E39*self.group.get_player_by_id(id).amount+(E38-E39)*(E40-E41+E42), self.group.get_player_by_id(id).money)**I40 + I39) / P40
            return round(utility)

        else: #2-G-L
            #a2 = 50
            #b2 = 695.07
            if self.group.get_player_by_id(id).amount >= 0 and self.group.get_player_by_id(id).amount <= G40:
                utility = (K38 * min(G38*self.group.get_player_by_id(id).amount, self.group.get_player_by_id(id).money)**K40 + K39) / P40
            elif self.group.get_player_by_id(id).amount > G40 and self.group.get_player_by_id(id).amount <= G41:
                utility = (K38 * min(G39*self.group.get_player_by_id(id).amount+(G38-G39)*G40, self.group.get_player_by_id(id).money)**K40 + K39) / P40
            elif self.group.get_player_by_id(id).amount > G41 and self.group.get_player_by_id(id).amount <= G42:
                utility = (K38 * min(G38*self.group.get_player_by_id(id).amount+(G38-G39)*(G40-G41), self.group.get_player_by_id(id).money)**K40 + K39) / P40
            elif self.group.get_player_by_id(id).amount >G42 and self.group.get_player_by_id(id).amount <= G43:
                utility = (K38 * min(G39*self.group.get_player_by_id(id).amount+(G38-G39)*(G40-G41+G42), self.group.get_player_by_id(id).money)**K40 + K39) / P40
            else:
                utility = (K38 * min(G39*self.group.get_player_by_id(id).amount+(G38-G39)*(G40-G41+G42-G43), self.group.get_player_by_id(id).money)**K40 + K39) / P40
            return round(utility)

        # if role == '1-A-F':
        #     #a1 = 52.58
        #     #b1 = 669.96
        #     if self.amount >= 0 and self.amount <= E40:
        #         utility = (I38 * min(E38*self.amount, self.money)**I40 + I39) / P40
        #     elif self.amount > E40 and self.amount <= E41:
        #         utility = (I38 * min(E39*self.amount+(E38-E39)*E40, self.money)**I40 + I39) / P40
        #     elif self.amount > E41 and self.amount <= E42:
        #         utility = (I38 * min(E38*self.amount+(E38-E39)*(E40-E41), self.money)**I40 + I39) / P40
        #     else:
        #         utility = (I38 * min(E39*self.amount+(E38-E39)*(E40-E41+E42), self.money)**I40 + I39) / P40
        #     return round(utility)
        #
        # else: #2-G-L
        #     #a2 = 50
        #     #b2 = 695.07
        #     if self.amount >= 0 and self.amount <= G40:
        #         utility = (K38 * min(G38*self.amount, self.money)**K40 + K39) / P40
        #     elif self.amount > G40 and self.amount <= G41:
        #         utility = (K38 * min(G39*self.amount+(G38-G39)*G40, self.money)**K40 + K39) / P40
        #     elif self.amount > G41 and self.amount <= G42:
        #         utility = (K38 * min(G38*self.amount+(G38-G39)*(G40-G41), self.money)**K40 + K39) / P40
        #     elif self.amount >G42 and self.amount <= G43:
        #         utility = (K38 * min(G39*self.amount+(G38-G39)*(G40-G41+G42), self.money)**K40 + K39) / P40
        #     else:
        #         utility = (K38 * min(G39*self.amount+(G38-G39)*(G40-G41+G42-G43), self.money)**K40 + K39) / P40
        #     return round(utility)

    def live_auction(self, data):
        group = self.group
        my_id = self.id_in_group
        type = data['type']
        print('kiteruyo')

        if type == 'bid':
            price = data['price']
            amount = data['amount']
            if self.amount < amount:
                response = dict(type= 'not_enough_X')
                return {my_id: response}
            else:
                self.history_bid += str(price) + ','
                group.history_all_bid_price += str(price) + ','
                group.history_all_bid_amount += str(amount) + ','
                group.history_all_bidder += str(my_id) +','
                response = dict(
                    type = 'bid',
                    id_in_group = my_id,
                    amount = amount,
                    price = price,
                    unit_of_price = format(price/amount,'.1f')
                )
                return {0: response}

        elif type == 'ask':
            price = data['price']
            amount = data['amount']
            if self.money < price:
                response = dict(type= 'not_enough_Y')
                return {my_id: response}
            else:
                self.history_ask += str(price) + ','
                group.history_all_ask_price += str(price) + ','
                group.history_all_ask_amount += str(amount) + ','
                group.history_all_asker += str(my_id) +','
                response = dict(
                    type = 'ask',
                    id_in_group = my_id,
                    amount = amount,
                    price = price,
                    unit_of_price = format(price/amount,'.1f')
                )
                return {0: response}

        elif type == 'bid_cancel':
            response = dict(
                type = 'bid_cancel',
                id_in_group = my_id
            )
            return {0: response}

        elif type == 'ask_cancel':
            response = dict(
                type = 'ask_cancel',
                id_in_group = my_id
            )
            return {0: response}

        elif type == 'bid_accept':
            bidder = data['bidder']
            price = data['price']
            amount = data['amount']
            print(bidder, price, amount)
            if self.money < price :
                response = dict(type= 'not_enough_Y')
                return {my_id: response}
            else:
                group.get_player_by_id(bidder).money += price
                group.get_player_by_id(my_id).money -= price
                group.get_player_by_id(bidder).amount -= amount
                group.get_player_by_id(my_id).amount += amount
                group.get_player_by_id(bidder).utility = self.utility_cal(group.get_player_by_id(bidder).roll,bidder)
                group.get_player_by_id(my_id).utility = self.utility_cal(group.get_player_by_id(my_id).roll,my_id)
                group.get_player_by_id(bidder).history_money += str(group.get_player_by_id(bidder).money) + ','
                group.get_player_by_id(my_id).history_money += str(group.get_player_by_id(my_id).money) + ','
                group.get_player_by_id(bidder).history_amount += str(group.get_player_by_id(bidder).amount) + ','
                group.get_player_by_id(my_id).history_amount += str(group.get_player_by_id(my_id).amount) + ','
                group.get_player_by_id(bidder).history_utility += str(group.get_player_by_id(bidder).utility) + ','
                group.get_player_by_id(my_id).history_utility += str(group.get_player_by_id(my_id).utility) + ','
                group.get_player_by_id(bidder).history_partner += str(my_id) + ','
                group.get_player_by_id(my_id).history_partner += str(bidder) + ','
                group.history_trade_bidder += str(bidder) + ','
                group.history_trade_asker += str(my_id) + ','
                group.history_trade_price += str(price) + ','
                group.history_trade_amount += str(amount) + ','
                response = dict(
                    type = 'bid_accept',
                    asker = my_id,
                    bidder = bidder,
                    amount = amount,
                    price = price,
                    unit_of_price = format(price/amount,'.1f'),
                    bidder_amount = group.get_player_by_id(bidder).amount,
                    bidder_money = group.get_player_by_id(bidder).money,
                    bidder_utility = group.get_player_by_id(bidder).utility,
                    asker_amount = group.get_player_by_id(my_id).amount,
                    asker_money = group.get_player_by_id(my_id).money,
                    asker_utility = group.get_player_by_id(my_id).utility
                )
                return {0: response}

        elif type == 'ask_accept':
            asker = data['asker']
            price = data['price']
            amount = data['amount']
            print(asker, price, amount)
            if self.amount < amount:
                response = dict(type= 'not_enough_X')
                return {my_id: response}
            else:
                group.get_player_by_id(my_id).money += price
                group.get_player_by_id(asker).money -= price
                group.get_player_by_id(my_id).amount -= amount
                group.get_player_by_id(asker).amount += amount
                group.get_player_by_id(my_id).utility = self.utility_cal(group.get_player_by_id(my_id).roll,my_id)
                group.get_player_by_id(asker).utility = self.utility_cal(group.get_player_by_id(asker).roll,asker)
                group.get_player_by_id(my_id).history_money += str(group.get_player_by_id(my_id).money) + ','
                group.get_player_by_id(asker).history_money += str(group.get_player_by_id(asker).money) + ','
                group.get_player_by_id(my_id).history_amount += str(group.get_player_by_id(my_id).amount) + ','
                group.get_player_by_id(asker).history_amount += str(group.get_player_by_id(asker).amount) + ','
                group.get_player_by_id(my_id).history_utility += str(group.get_player_by_id(my_id).utility) + ','
                group.get_player_by_id(asker).history_utility += str(group.get_player_by_id(asker).utility) + ','
                group.get_player_by_id(my_id).history_partner += str(asker) + ','
                group.get_player_by_id(asker).history_partner += str(my_id) + ','
                group.history_trade_bidder += str(my_id) + ','
                group.history_trade_asker += str(asker) + ','
                group.history_trade_price += str(price) + ','
                group.history_trade_amount += str(amount) + ','
                response = dict(
                    type = 'ask_accept',
                    bidder = my_id,
                    asker = asker,
                    amount = amount,
                    price = price,
                    unit_of_price = format(price/amount,'.1f'),
                    bidder_amount = group.get_player_by_id(my_id).amount,
                    bidder_money = group.get_player_by_id(my_id).money,
                    bidder_utility = group.get_player_by_id(my_id).utility,
                    asker_amount = group.get_player_by_id(asker).amount,
                    asker_money = group.get_player_by_id(asker).money,
                    asker_utility = group.get_player_by_id(asker).utility
                )
                return {0: response}
