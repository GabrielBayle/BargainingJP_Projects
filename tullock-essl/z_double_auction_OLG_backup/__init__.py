from otree.api import *
import time
import random

doc = "Double auction market in an OLG framework"

# TO DO:
# IMPORTANT:
#   - DONE - restrict money offers, so they can't be mote than money holdings: use pop up window (see bargaining)
#   - Done: - include price prediction for those who are not playing  w/ results page (use page from Investors game)
#   - DONE: - round payoff function: for those not playing and for sellers (aka OLD)
#   - Done: - Add dividend payment for Buyers only in  last round
#   - Done: Add round_payoff for short horizon and long horizon treatment
#   - DONE: select 1 seller (aka OLD) rounds and 1 prediction rounds for OLG treatment
#   - DONE: select 1 of the 3 short for random payments
#   - DONE : replace 5,6 and 10,11 with settings variable for short horizon treatment
#   - DONE : Information Acquisition page w/separate endowment payoff (add this info to sequence page )
#   - DONE:  add FINAL  results screen
#   - DONE:- check Final Results screen

#   - add intro screen for every new sequence in the non-olg treatment

# NOT SO IMPORTANT:

#   - add instructions
#   - add practice rounds
#   - show non-olg players past average_price (an option would be to create a var as I do with the random payment)


class C(BaseConstants):
    NAME_IN_URL = 'double_auction_OLG'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15
    ORIGINAL_ASSETS_PER_SELLER = 4


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=False)

    if subsession.session.config['OLG'] is True:  # for OLG treatment
        players = subsession.get_players()

        for p in players:
            p.is_buyer = p.id_in_group > p.session.config['num_sellers']
            p.is_playing = p.id_in_group <= p.session.config['num_sellers']+p.session.config['num_buyers']

            p.is_informed = False

            if p.is_playing:
                if p.is_buyer:
                    p.num_items = 0
                    # p.break_even_point = random.randint(C.VALUATION_MIN, C.VALUATION_MAX)
                    p.break_even_point = 0
                    p.current_offer = 0
                    p.money = p.session.config['money']

                else:
                    p.num_items = p.session.config['assets_per_seller']
                    # p.break_even_point = random.randint(
                    #  C.PRODUCTION_COSTS_MIN, C.PRODUCTION_COSTS_MAX
                    # )
                    p.break_even_point = 0
                    # p.current_offer = C.VALUATION_MAX + 1
                    p.current_offer = 999  # try with NA later
                    p.money = 0
            else:
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.money = 0

            if p.session.config['info_acquisition'] is False:
                p.is_informed = True

    if subsession.session.config['OLG'] is False:     # For the non-OLG: with 2 option, short term and long term  asset
        if subsession.session.config['short_horizon'] is True:
            players = subsession.get_players()
            for p in players:
                p.is_buyer = True
                p.num_items = p.session.config['assets_per_seller']
                p.break_even_point = 0
                p.current_offer = 0
                p.money = p.session.config['initial_money']
                p.is_playing = True
                p.is_informed = False

                if p.session.config['info_acquisition'] is False:
                    p.is_informed = True

        if subsession.session.config['short_horizon'] is False:
            players = subsession.get_players()
            for p in players:
                p.is_buyer = True
                p.num_items = p.session.config['assets_per_seller']
                p.break_even_point = 0
                p.current_offer = 0
                p.money = p.session.config['initial_money']
                p.is_playing = True
                p.is_informed = False

                if p.session.config['info_acquisition'] is False:
                    p.is_informed = True


class Group(BaseGroup):
    # original fields
    start_timestamp = models.IntegerField()

    # my fields
    signal = models.FloatField()  # information about dividends
    average_price = models.FloatField()  # average round price


class Player(BasePlayer):
    # original fields
    is_buyer = models.BooleanField()    # works in conjunction with
    current_offer = models.CurrencyField(blank=True)
    break_even_point = models.CurrencyField()   # won't need this
    num_items = models.IntegerField()   # assets during each round

    # my fields
    money = models.CurrencyField()
    # assets = models.FloatField()        # would be the same  as num_items
    round_payoff = models.FloatField()    # for recording payments to be selected at random
    is_playing = models.BooleanField()    # this is whether they are trading or just waiting and predicting
    prediction = models.FloatField()      # predicted price
    is_informed = models.BooleanField()   # whether they see the divided (or a clue) or not

    # for the quiz
    Q1 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

    Q2 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

    Q3 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

    Q4 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

    Q5 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

    Q6 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )
    Q7 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )
    Q8 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )
    Q9 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )
    Q10 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Disagree strongly'], [2, 'Disagree'], [3, 'Neither agree or disagree'], [4, 'Agree'],
                 [5, 'Agree strongly']],
    )

class Transaction(ExtraModel):
    group = models.Link(Group)
    buyer = models.Link(Player)
    seller = models.Link(Player)
    price = models.CurrencyField()
    seconds = models.IntegerField(doc="Timestamp (seconds since beginning of trading)")

# FUNCTIONS


def find_match(buyers, sellers):
    for buyer in buyers:
        for seller in sellers:
            if seller.num_items > 0 and seller.current_offer <= buyer.current_offer:
                # return as soon as we find a match (the rest of the loop will be skipped)
                return [buyer, seller]


def live_method(player: Player, data):
    group = player.group
    players = group.get_players()
    buyers = [p for p in players if p.is_buyer and p.is_playing]
    sellers = [p for p in players if not p.is_buyer and p.is_playing]

    news = None
    if data:
        print('Valid message received', data)
        if player.session.config['OLG'] is False:
            aux = int(data['role'])
            player.is_buyer = aux
            players = group.get_players()
            buyers = [p for p in players if p.is_buyer and p.is_playing]
            sellers = [p for p in players if not p.is_buyer and p.is_playing]

        offer = int(data['offer'])
        player.current_offer = offer
        if player.is_buyer:
            match = find_match(buyers=[player], sellers=sellers)
        else:
            match = find_match(buyers=buyers, sellers=[player])
        if match:
            [buyer, seller] = match
            price = buyer.current_offer
            Transaction.create(
                group=group,
                buyer=buyer,
                seller=seller,
                price=price,
                seconds=int(time.time() - group.start_timestamp),
            )
            buyer.num_items += 1
            seller.num_items -= 1
            buyer.money += -price
            seller.money += price
            buyer.current_offer = 0
            # seller.current_offer = C.VALUATION_MAX + 1
            seller.current_offer = 999
            news = dict(buyer=buyer.id_in_group, seller=seller.id_in_group, price=price)

    bids = sorted([p.current_offer for p in buyers if p.current_offer > 0], reverse=True)
    # asks = sorted([p.current_offer for p in sellers if p.current_offer <= C.VALUATION_MAX])
    asks = sorted([p.current_offer for p in sellers if p.current_offer <= 998])
    highcharts_series = [[tx.seconds, tx.price] for tx in Transaction.filter(group=group)]

    return {
        p.id_in_group: dict(
            num_items=p.num_items,
            current_offer=p.current_offer,
            payoff=p.money,                 # check this
            bids=bids,
            asks=asks,
            highcharts_series=highcharts_series,
            news=news,
        )
        for p in players
    }


def custom_export(players):  # to export the variables that get saved in JS
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'id_in_subsession', 'bids']
    for p in players:
        participant = p.participant
        session = p.session
        group = p.group
        bids = Transaction.filter(group=group)
        yield [session.code, participant.code, p.round_number, p.id_in_group, group.id_in_subsession, bids]


# get payoff put off the live function
# def payoff(player: Player):
#   pass

# determines payoffs after each round in the OLG setup
def round_payoff_olg(group: Group):
    players = group.get_players()
    for p in players:
        if p.is_playing is True:    # players  payoff
            if p.is_buyer is True:  # buyers (aka young) w/2 options: normal and final round
                if p.round_number < p.session.config['num_rounds']:                             # normal rounds
                    p.round_payoff = 0
                else:
                    p.round_payoff = p.session.config['dividend']*p.num_items + float(p.money)  # last round
            else:                   # seller (aka old)
                p.round_payoff = float(p.money)
        else:                       # non-players prediction payoff
            p.round_payoff = p.session.config['prediction_endowment']-p.session.config['scale_prediction'] * \
                             (p.prediction - p.group.average_price)**2

# USED WHEN PAYING ONly ONE ROUND AT RANDOM
        if p.round_number == p.session.config['num_rounds']:
            players_all = p.in_all_rounds()

            #  as a seller aka (old):
            sellers = [x for x in players_all if not x.is_buyer and x.is_playing and x.round_number != 1]
            p.participant.vars['paying_round_seller'] = random.sample([p.round_number for p in sellers], 1)
            for y in p.participant.vars['paying_round_seller']:
                z = float(y)
                print('seller round', z)
                print(p.in_round(z).round_payoff, p.in_round(z).is_buyer, p.in_round(z).is_playing)

                if p.in_round(z).is_informed and p.session.config['info_acquisition'] is True:
                    p.payoff = p.in_round(z).round_payoff/p.session.config['us_exchange_rate'] - \
                               p.session.config['info_cost']
                else:
                    p.payoff = p.in_round(z).round_payoff / p.session.config['us_exchange_rate']

                p.participant.vars['aux_payoff_seller'] = p.payoff
                print('paying round is', p.participant.vars['paying_round_seller'], '=',
                      p.participant.vars['aux_payoff_seller'])

            # as a predictor :
            predictor = [x for x in players_all if not x.is_playing]
            p.participant.vars['paying_round_predictor'] = random.sample([p.round_number for p in predictor], 1)
            for y in p.participant.vars['paying_round_predictor']:
                z = float(y)
                print('predictor round', z)
                print(p.in_round(z).round_payoff, p.in_round(z).is_buyer, p.in_round(z).is_playing)

                if p.in_round(z).is_informed and p.session.config['info_acquisition'] is True:
                    p.payoff += p.in_round(z).round_payoff / p.session.config['us_exchange_rate'] - \
                               p.session.config['info_cost']

                else:
                    p.payoff += p.in_round(z).round_payoff / p.session.config['us_exchange_rate']

                p.participant.vars['aux_payoff_predictor'] = p.payoff
                print('paying round is', p.participant.vars['paying_round_predictor'], '=',
                      p.participant.vars['aux_payoff_predictor'])


# determines payoffs in the final sequence round in the non-OLG setup
def round_payoff(group: Group):
    players = group.get_players()
    if group.round_number == group.session.config['dividend_1_period']:
        dividend = group.session.config['dividend_1']
    if group.round_number == group.session.config['dividend_2_period']:
        dividend = group.session.config['dividend_2']
    if group.round_number == group.session.config['dividend_3_period'] and\
            group.session.config['short_horizon'] is True:
        dividend = group.session.config['dividend_3']
    if group.round_number == group.session.config['num_rounds'] and group.session.config['short_horizon'] is False:
        dividend = group.session.config['dividend']
    for p in players:
        p.round_payoff = dividend * p.num_items + float(p.money)

        if p.round_number == p.session.config['num_rounds']:

            # USED when there's only one large sequence
            if group.round_number == p.session.config['num_rounds'] and group.session.config['short_horizon'] is False:
                p.payoff = p.round_payoff

            # USED WHEN PAYING ONly ONE of the 3 Sequences AT RANDOM
            if group.round_number == p.session.config['num_rounds'] and group.session.config['short_horizon'] is True:
                p.participant.vars['paying_round'] = random.sample([5, 10, 15], 1)
                for y in p.participant.vars['paying_round']:
                    z = float(y)
                    print('predictor round', z)

                    if p.in_round(z).is_informed and p.session.config['info_acquisition'] is True:
                        p.payoff += p.in_round(z).round_payoff / p.session.config['us_exchange_rate'] - \
                               p.session.config['info_cost']
                    else:
                        p.payoff += p.in_round(z).round_payoff / p.session.config['us_exchange_rate']

                    p.participant.vars['aux_payoff'] = p.in_round(z).payoff
                    print('paying round is', p.participant.vars['paying_round'], '=',
                          p.participant.vars['aux_payoff'])


# include this at the beginning of each round (except the first one)
def round_change_olg(group: Group):
    players = group.get_players()

    total_unsold = sum(player.in_round(player.round_number - 1).num_items for player in players if
                       player.in_round(player.round_number - 1).is_buyer is False)

    print('unsold items in previous round = ', total_unsold)

    # Transforms buyers (aka young) into  sellers (aka old), and sellers (old) into non-playing.
    count = 1
    for p in players:
        # among those who played the last round
        if p.in_round(p.round_number - 1).is_playing is True:

            # seller to non-players
            if p.in_round(p.round_number - 1).is_buyer is False:
                p.is_playing = False
                p.is_buyer = True
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.money = 0
                p.is_informed = p.in_round(p.round_number - 1).is_informed

            # buyer to seller
            else:
                p.is_buyer = False
                p.is_playing = True
                p.num_items = p.in_round(p.round_number - 1).num_items
                p.break_even_point = 0
                p.current_offer = 999
                p.money = p.in_round(p.round_number - 1).money
                p.is_informed = p.in_round(p.round_number - 1).is_informed

        # among those who did not play
        else:
            # non-player to buyer
            if count <= p.session.config['num_buyers']:
                p.is_playing = True
                p.is_buyer = True
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.money = p.session.config['money']
                p.is_informed = p.in_round(p.round_number - 1).is_informed
                print('new buyers', count)
                count += 1
            # non-player who stays out
            else:
                p.is_playing = False
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.is_buyer = True
                p.money = 0
                p.is_informed = p.in_round(p.round_number - 1).is_informed

        if p.session.config['info_acquisition'] is False:
            p.is_informed = True

    # assigns unsold units to those buyers that will become sellers
    # (this assigns in order but order changes every round)
    counter = 1
    while counter <= total_unsold:
        for p in players:
            if counter <= total_unsold:
                if p.is_playing is True and p.is_buyer is False:
                    print('assigning unsold assets', counter)
                    counter += 1
                    p.num_items += 1


def round_change(group: Group):
    players = group.get_players()
    for p in players:
        p.is_playing = True
        p.num_items = p.in_round(p.round_number - 1).num_items
        p.break_even_point = 0
        p.current_offer = 0
        p.is_buyer = True
        p.money = p.in_round(p.round_number - 1).money
        p.is_informed = p.in_round(p.round_number - 1).is_informed

        if p.session.config['info_acquisition'] is False:
            p.is_informed = True


def average_price(group: Group):
    players = group.get_players()

    total_sold = sum(player.num_items for player in players if player.is_buyer is True)
    total_paid = sum(player.money for player in players if player.is_buyer is False)

    print('sold items in current round = ', total_sold)
    print('total payments  in current round = ', total_paid)

    if total_sold > 0:
        group.average_price = float(total_paid/total_sold)
    else:
        group.average_price = 0

    print('average price is', group.average_price)


# PAGES

class Instructions1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
            num_sequences=player.session.config['num_sequences'],
            num_practice_sequences=player.session.config['num_practice_sequences'],
            # others_in_group=,
            #signal_cost_scale=player.session.config['signal_cost_scale'],
            endowment=player.session.config['money'],
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            #statement=player.session.config['statement'],
        )


class Instructions2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
          #  others_in_group=Constants.players_per_group-1,
           # signal_cost_scale=player.session.config['signal_cost_scale'],
            endowment=player.session.config['money'],
          #  theta_hat_prize=player.session.config['theta_hat_prize'],
           # seller_bonus=player.session.config['seller_bonus'],
            # statement=player.session.config['statement'],
        )


class Instructions3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
         #   others_in_group=Constants.players_per_group-1,
         #   signal_cost_scale=player.session.config['signal_cost_scale'],
            endowment=player.session.config['money'],
            #theta_hat_prize=player.session.config['theta_hat_prize'],
            #seller_bonus=player.session.config['seller_bonus'],
            #statement=player.session.config['statement'],
        )

class Instructions4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
         #   others_in_group=Constants.players_per_group-1,
         #   signal_cost_scale=player.session.config['signal_cost_scale'],
            endowment=player.session.config['money'],
            #theta_hat_prize=player.session.config['theta_hat_prize'],
            #seller_bonus=player.session.config['seller_bonus'],
            #statement=player.session.config['statement'],
        )


#class QuizIntro(Page):
#    @staticmethod
#    def is_displayed(player: Player):
#        return player.round_number == 1

#    @staticmethod
#    def vars_for_template(player: Player):
#        return dict(
#            num_rounds=player.session.config['num_rounds'],
#            practice_num_rounds=player.session.config['practice_num_rounds'],
#            others_in_group=Constants.players_per_group-1,
#        )


class Quiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']


class Quiz_II(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['Q7', 'Q8', 'Q9', 'Q10']



class PracticeIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
            others_in_group=2,
        )







class PayingIntro(Page):
    timeout_seconds = 20

    @staticmethod
    def is_displayed(player: Player):
        return (player.session.config['OLG'] is False and
                (player.session.config['short_horizon'] is True and
                (player.round_number == 1 or player.round_number == player.session.config['dividend_1_period'] or
                 player.round_number == player.session.config['dividend_2_period'])
                or (player.session.config['short_horizon'] is False and player.round_number == 1))) or\
               (player.session.config['OLG'] is True and player.round_number == 1)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            short_horizon=player.session.config['short_horizon'],
            OLG=player.session.config['OLG']
        )


class WaitToStart(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.round_number >= 2 and group.session.config['OLG'] is True:
            round_change_olg(group)

        if group.round_number >= 2 and group.session.config['OLG'] is False:
            if group.session.config['short_horizon'] is True:
                if group.round_number == (group.session.config['dividend_1_period']+1) or \
                        group.round_number == (group.session.config['dividend_2_period']+1):
                    pass
                else:
                    round_change(group)
            elif group.session.config['short_horizon'] is False:
                round_change(group)

        group.start_timestamp = int(time.time())


class TradingOLG(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_playing is True and player.round_number <= player.session.config['num_rounds'] and \
               player.session.config['OLG'] is True

    form_model = 'player'
    form_fields = ['is_informed']

    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(id_in_group=player.id_in_group,
                    is_buyer=player.is_buyer,
                    )

    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return (group.start_timestamp + player.session.config['minutes'] * 60) - time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            dividend=player.session.config['dividend'],
            info_cost=player.session.config['info_cost'])


class Trading(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_playing is True and player.round_number <= player.session.config['num_rounds'] and \
               player.session.config['OLG'] is False

    form_model = 'player'
    form_fields = ['is_informed']

    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(id_in_group=player.id_in_group,
                    is_buyer=player.is_buyer,
                    )

    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return (group.start_timestamp + player.session.config['minutes'] * 60) - time.time()

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['dividend_3_period'] and \
                player.session.config['short_horizon'] is True:
            dividend = player.session.config['dividend_3']
        if player.round_number <= player.session.config['dividend_2_period'] and \
                player.session.config['short_horizon'] is True:
            dividend = player.session.config['dividend_2']
        if player.round_number <= player.session.config['dividend_1_period'] and \
                player.session.config['short_horizon'] is True:
            dividend = player.session.config['dividend_1']

        if player.round_number <= player.session.config['num_rounds'] and \
                player.session.config['short_horizon'] is False:
            dividend = player.session.config['dividend']
        return dict(
            num_rounds=player.session.config['num_rounds'],
            dividend=dividend,
            info_cost=player.session.config['info_cost'])


class Prediction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_playing is False and player.round_number <= player.session.config['num_rounds'] and \
               player.session.config['OLG'] is True

    form_model = 'player'
    form_fields = ['prediction']

    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return (group.start_timestamp + player.session.config['minutes'] * 60) - time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            scale_prediction=player.session.config['scale_prediction'],
            prediction_endowment=player.session.config['prediction_endowment'],
            prediction_min=player.session.config['prediction_min'],
            prediction_max=player.session.config['prediction_max'],
                    )



class ResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.session.config['OLG'] is True:
            average_price(group)
            round_payoff_olg(group)

        if group.session.config['OLG'] is False:
            if group.session.config['short_horizon'] is True and \
                    (group.round_number == group.session.config['dividend_1_period'] or
                     group.round_number == group.session.config['dividend_2_period'] or
                     group.round_number == group.session.config['dividend_3_period']):
                round_payoff(group)
            if group.session.config['short_horizon'] is False and\
                    group.round_number == group.session.config['num_rounds']:
                round_payoff(group)


class ResultsOlg(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds'] and \
               player.session.config['OLG'] is True

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            dividend=player.session.config['dividend'],
            )


class Results(Page):
    timeout_seconds = 20
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds'] and \
               player.session.config['OLG'] is False

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            )


class SequenceResults(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['OLG'] is False and \
               (player.session.config['short_horizon'] is True and
                (player.round_number == player.session.config['dividend_1_period'] or
                player.round_number == player.session.config['dividend_2_period'] or
                player.round_number == player.session.config['dividend_3_period'])
                or (player.session.config['short_horizon'] is False and
                    player.round_number == player.session.config['num_rounds']))

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == player.session.config['dividend_1_period']:
            dividend = player.session.config['dividend_1']
        if player.round_number == player.session.config['dividend_2_period']:
            dividend = player.session.config['dividend_2']
        if player.round_number == player.session.config['dividend_3_period'] and\
                player.session.config['short_horizon'] is True:
            dividend = player.session.config['dividend_3']
        if player.round_number == player.session.config['num_rounds'] and \
                player.session.config['short_horizon'] is False:
            dividend = player.session.config['dividend']

        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            dividend=dividend,
            )


class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.session.config['num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            payoff_plus_participation_fee=player.participant.payoff_plus_participation_fee(),
            total_earnings=player.participant.vars['aux_payoff'],
            show_up_fee=float(player.session.config['participation_fee']),
            total_earnings_US=float(player.participant.payoff),
            total_payoff_US=float(player.participant.payoff_plus_participation_fee()),
            paying_round=player.participant.vars['paying_round'][0],
            us_exchange_rate=player.session.config['us_exchange_rate'],
            OLG=player.session.config['OLG'],
            info_acquisition=player.session.config['info_acquisition'],
            info_cost=player.session.config['info_cost']

        )


page_sequence = [ Instructions1,
                 Instructions2,
                 Instructions3,
                 Instructions4,
                 Quiz,
                 Quiz_II,
                 PracticeIntro,  
                 PayingIntro,
                 WaitToStart,
                 Trading,
                 TradingOLG,
                 Prediction,
                 ResultsWaitPage,
                 ResultsOlg,
                 Results,
                 SequenceResults,
                 FinalResults]
