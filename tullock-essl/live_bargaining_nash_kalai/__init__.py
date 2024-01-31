from otree.api import *
import random

doc = """
Continuous time bargaining game over P and Q b/w Seller and Buyer
"""


# how to extract ExtraModel info at the end (time-stamped bidding behaviour)..... IMPORTANT!!!   - DONE!
#  make sure the history table is side by side  - check!  - DONE!

# IMPORTANT:
# add borrowing page .....DONE
# make sure payback for borrowing is included! DONE
# in round results add points for seller and buyer DONE
# a function that limits negative surpluses.....  NOT SURE I WANT TO ADD THIS ??????  DONE
# add sliders for choices w/ max and min DONE
# add 2 minute time limit for barganing  DONE
# add result if trading does not take place DONE
# include  function so player are only paid for X rounds . How many rounds, what is the exchange rate?... .DONE
# if r=0 the borrowing instructions should reflect it !!!!!!!!.... DONE
# what to do if the buyer borrows zero in the ?.... DONE
# message before sending an offer and maybe before accepting an offer???... DONE
# add practice round as separate app (LAST THING TO DO)..... DONE
# Instructions and questions (same as Radhika for questions, what about instructions?..... See what they did in JOhn's... DONE
# add exit questionaire + risk assestment as separate app??  Same as Radhikjas??...DONE
# Include a graph of u(q) minus c(q) ?????????? Maybe in the instructions ???? Maybe as a pop up when you hover over something ?.... DONE



# make sure it reloads data from ExtraModel when the page loads so it does not loose when error..DON't know how!

# NOT SO IMPORTANT:
# include max and min at bottom of sliders in the barganing page.. .DONE
# include Intro for practice round and paying rounds (a la Investors code)..... DONE
# add color to results (lke I did for Rahdika)..... DONE

# NOT SURE:
# in results screen include counterpart (on alternative is to creat a field for your counterparts aka player.other_pay)


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 28
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal_price = models.FloatField()  # price accepted in the group
    deal_price_q = models.FloatField()  # quantity accepted in the group
    is_finished = models.BooleanField(initial=False)  # for when someone accepts
    no_agreement = models.BooleanField(initial=False) # wheter an agreement was reached or not

class Player(BasePlayer):
    amount_borrowed = models.FloatField()  # how much the buyer borrows
    gross_payoff = models.FloatField()  # payoff earned from trade in the round (excluding the transfer, so b(q) or c(q)
    net_payoff = models.FloatField()  # payoff after transfers and interest repayment

    amount_proposed = models.FloatField()  # last price proposed by player
    amount_accepted = models.FloatField()  # accepted price player  (0 if other player accepts)

    amount_proposed_q = models.FloatField()  # last quantity proposed by player
    amount_accepted_q = models.FloatField()  # accepted quantity player  (0 if other player accepts )


class Bid(ExtraModel):  # things that get saved without creating a variable
    player = models.Link(Player)
    time_stamp = models.FloatField()
    amount = models.FloatField()
    amount_q = models.FloatField()


# FUNCTIONS:


def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)


def custom_export(players):  # to export the variables that get saved in JS
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'bids']
    for p in players:
        participant = p.participant
        session = p.session
        group = p.group
        bids = Bid.filter(player=p)
        yield [session.code, participant.code, p.round_number, p.id_in_group, group.id_in_subsession, bids]


def set_payoff(player: Player):  # determines payoffs after each round
    if player.round_number <= player.session.config['num_rounds'] / 2:
        r = player.session.config["r_1"]
    else:
        r = player.session.config["r_2"]

    endowment = player.session.config['endowment']*r
    seller_endowment = player.session.config['seller_endowment']

    if player.role == 'Buyer':  # buyer
        player.gross_payoff = player.session.config['A'] * player.group.deal_price_q ** player.session.config['a']
        player.net_payoff = player.gross_payoff - player.group.deal_price + player.amount_borrowed + endowment - player.amount_borrowed * (1+r)
    else:
        player.gross_payoff = -player.session.config['B'] * player.group.deal_price_q ** player.session.config['b']
        player.net_payoff = player.gross_payoff + player.group.deal_price + seller_endowment



# USED WHEN PAYING ONly ONE ROUND AT RANDOM
    if player.round_number == player.session.config['num_rounds']:
        player.participant.vars['paying_round'] = random.sample(range(1, player.session.config['num_rounds'] + 1), 1)
        for x in player.participant.vars['paying_round']:
            if player.in_round(x).net_payoff > 0:
                player.payoff = player.in_round(x).net_payoff/player.session.config['us_exchange_rate']
                player.participant.vars['aux_payoff'] = player.in_round(x).net_payoff
                print('paying round is', player.participant.vars['paying_round'], '=',
                      player.participant.vars['aux_payoff'])
            else:
                player.payoff = 0
                player.participant.vars['aux_payoff'] = player.in_round(x).net_payoff
# PAGES:

class PayingIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 or player.round_number == (player.session.config['num_rounds']/2+1)

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['num_rounds']/2:
            r=player.session.config["r_1"]
            r_percentage = player.session.config['r_1'] * 100
            borrow_max = player.session.config['endowment'] / (1 + player.session.config["r_1"])
        else:
            r=player.session.config["r_2"]
            r_percentage = player.session.config['r_2'] * 100
            borrow_max = player.session.config['endowment'] / (1 + player.session.config["r_2"])


        return dict(other_role=player.get_others_in_group()[0].role,
                    chat_on=player.session.config['chat_on'],
                    a=player.session.config['a'],
                    A=player.session.config['A'],
                    b=player.session.config['b'],
                    B=player.session.config['B'],
                    endowment=player.session.config['endowment'],
                    num_rounds=player.session.config['num_rounds'],
                    r=r,
                    r_percentage=r_percentage,
                    borrow_max= borrow_max,
                    message=player.session.config['message'],
                    half_num_round=player.session.config['num_rounds']/2,
                    half_num_round_plus_one=player.session.config['num_rounds']/2+1,
                    principal_plus_interest_example = 10 * (1 + r)
                    )
#class WaitForOthers_I(WaitPage):
#    @staticmethod
#    def is_displayed(player: Player):
#        return player.round_number <= player.session.config['num_rounds']

#    title_text = "Please wait"
#    body_text = "Waiting to be matched with a new counterpart"


class Borrow(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds'] and player.role == 'Buyer'

    form_model = 'player'
    form_fields = ['amount_borrowed']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['num_rounds']/2:
            r=player.session.config["r_1"]
            r_percentage = player.session.config['r_1'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_1'])
        else:
            r=player.session.config["r_2"]
            r_percentage = player.session.config['r_2'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_2'])


        return dict(other_role=player.get_others_in_group()[0].role,
                    chat_on=player.session.config['chat_on'],
                    a=player.session.config['a'],
                    A=player.session.config['A'],
                    b=player.session.config['b'],
                    B=player.session.config['B'],
                    endowment=endowment,
                    num_rounds=player.session.config['num_rounds'],
                    r=r,
                    r_percentage=r_percentage,
                    borrow_max= borrow_max,
                    message=player.session.config['message'],
                    half_num_round=player.session.config['num_rounds']/2,
                    half_num_round_plus_one=player.session.config['num_rounds']/2+1,
                    principal_plus_interest_example = 10 * (1 + r)
                    )


class WaitForOthers_I(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    title_text = "Please wait"
    body_text = "Waiting while your counterparts decides how much money to bring to the meeting"

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.role == 'Seller':
                p.amount_borrowed = p.get_others_in_group()[0].amount_borrowed


class Bargain(Page):
    timeout_seconds = 120
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['num_rounds']/2:
            r=player.session.config["r_1"]
            r_percentage = player.session.config['r_1'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_1'])
        else:
            r=player.session.config["r_2"]
            r_percentage = player.session.config['r_2'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_2'])

        return dict(other_role=player.get_others_in_group()[0].role,
                    chat_on=player.session.config['chat_on'],
                    a=player.session.config['a'],
                    A=player.session.config['A'],
                    b=player.session.config['b'],
                    B=player.session.config['B'],
                    q_bar=pow(player.amount_borrowed / player.session.config['B'], 1 / player.session.config['b'])+0.01,
                  #  q_bar=pow(player.session.config['endowment'] / player.session.config['B'], 1 / player.session.config['b']),
                  # q_bar=11,
                    endowment=endowment,
                    r=r,
                    r_percentage=r_percentage,
                    borrow_max=borrow_max,
                    num_rounds=player.session.config['num_rounds'], )

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    # Receives what is sent from the page from liveSend() in JS  and sends back to Recv(data) in JS  automatically
    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        [other] = player.get_others_in_group()
        count = []
        count2 = []

        if 'amount' in data:
            try:
                amount = float(data['amount'])
                amount_q = float(data['amount_q'])
                time_stamp = data['time_stamp']
                print('Valid message received', data)
                count = len(Bid.filter(player=player)) + 1
                count2 = len(Bid.filter(player=other)) + 1
                print('number of proposals made by player:', count)
            except Exception:
                print('Invalid message received', data)
                count = 0
                count2 = 0
                return

            if data['type'] == 'accept':
                #      if amount == other.amount_proposed:    not necessary  when using multiplke bids
                player.amount_accepted = amount
                group.deal_price = amount

                player.amount_accepted_q = amount_q
                group.deal_price_q = amount_q

                group.is_finished = True
                return {0: dict(finished=True)}

            Bid_aux = []
            for t in Bid.filter(player=player):
                Bid_aux.append([t.time_stamp])

            if data['type'] == 'propose':
                player.amount_proposed = amount
                player.amount_proposed_q = amount_q
                Bid.create(player=player, amount=amount, amount_q=amount_q, time_stamp=time_stamp)

            proposals = []
            proposals.append([player.id_in_group, player.amount_proposed,
                              player.amount_proposed_q])
            return {0: dict(proposals=proposals,
                            #        Bid_aux=Bid_aux,
                            count=count,
                            count2=count2)
                    }

    #    Bid_aux=[]
    #    for t in Bid.filter(player=player):
    #        Bid_aux.append([t.time_stamp])

    #    proposals = []
    #    for p in [player, other]:
    #        amount_proposed = p.field_maybe_none('amount_proposed')
    #        if amount_proposed is not None:
    #            proposals.append([p.id_in_group, amount_proposed])
    #    return {0: dict(proposals=proposals,
    #                    Bid_aux=Bid_aux,
    #                    count=count)
    #            }

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if timeout_happened:
            player.group.deal_price_q = 0
            player.group.deal_price = 0
            player.group.no_agreement = True
        set_payoff(player)

#   @staticmethod
#   def is_displayed(player: Player):
#       """Skip this page if a deal has already been made"""
#       group = player.group
#       deal_price = group.field_maybe_none('deal_price')
#       return deal_price is None


class Results(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['num_rounds']/2:
            r=player.session.config["r_1"]
            r_percentage = player.session.config['r_1'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * ( player.session.config['r_1'])
        else:
            r=player.session.config["r_2"]
            r_percentage = player.session.config['r_2'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_2'])

        return dict(
            bids=Bid.filter(player=player),
            # bid_2=Bid.filter(player=player)[0]
            player_in_all_rounds=reversed(player.in_all_rounds()),
            a=player.session.config['a'],
            A=player.session.config['A'],
            b=player.session.config['b'],
            B=player.session.config['B'],
            endowment=endowment,
            seller_endowment=player.session.config['seller_endowment'],
            r=r,
            r_percentage=r_percentage,
            borrow_max=borrow_max,
            num_rounds=player.session.config['num_rounds'],
            gross_payoff=-player.gross_payoff,
            principal_plus_interest=player.amount_borrowed*(1+r),
            money_left=player.amount_borrowed-player.group.deal_price
        )


class MyWaitPage(WaitPage):
    wait_for_all_groups = True
    template_name = 'live_bargaining_nash_kalai/MyWaitPage.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['num_rounds'] / 2:
            r = player.session.config["r_1"]
            r_percentage = player.session.config['r_1'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_1'])
        else:
            r = player.session.config["r_2"]
            r_percentage = player.session.config['r_2'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_2'])
        return dict(
            bids=Bid.filter(player=player),
            # bid_2=Bid.filter(player=player)[0]
            player_in_all_rounds=reversed(player.in_all_rounds()),
            a=player.session.config['a'],
            A=player.session.config['A'],
            b=player.session.config['b'],
            B=player.session.config['B'],
            endowment=endowment,
            seller_endowment=player.session.config['seller_endowment'],
            r=r,
            r_percentage=r_percentage,
            borrow_max=borrow_max,
            practice_num_rounds=player.session.config['practice_num_rounds'],
            gross_payoff=-player.gross_payoff,
            principal_plus_interest=player.amount_borrowed * (1 + r),
            money_left=player.amount_borrowed - player.group.deal_price,
            body_text="Waiting to be matched with a new counterpart",
            title_text="Please wait"
        )


#class WaitForOthers_II(WaitPage):
 #   @staticmethod
  #  def is_displayed(player: Player):
   #     return player.round_number <= player.session.config['num_rounds']

   # title_text = "Please wait"
   # body_text = "Waiting to be matched with a new counterpart"


page_sequence = [PayingIntro, Borrow, WaitForOthers_I, Bargain, Results,
                 MyWaitPage]
