from otree.api import *
import random

doc = """
Continuous time bargaining game over P and Q b/w Seller and Buyer
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining_practice'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
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
    if player.round_number <= player.session.config['practice_num_rounds'] / 2:
        r = player.session.config["r_practice"]

    else:
        r = player.session.config["r_practice"]

    endowment = player.session.config['endowment']*r
    seller_endowment = player.session.config['seller_endowment']
    if player.role == 'Buyer':  # buyer
        player.gross_payoff = player.session.config['A'] * player.group.deal_price_q ** player.session.config['a']
        player.net_payoff = player.gross_payoff - player.group.deal_price + player.amount_borrowed + endowment - player.amount_borrowed * (1+r)
    else:
        player.gross_payoff = -player.session.config['B'] * player.group.deal_price_q ** player.session.config['b']
        player.net_payoff = player.gross_payoff + player.group.deal_price + seller_endowment



# PAGES:
class Instructions1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
            others_in_group=C.PLAYERS_PER_GROUP-1,
            endowment=player.session.config['endowment'],
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            statement=1,
            num_other_participants=player.session.num_participants-1
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
            others_in_group=C.PLAYERS_PER_GROUP-1,
            a=player.session.config['a'],
            A=player.session.config['A'],
            b=player.session.config['b'],
            B=player.session.config['B'],
            seller_endowment=player.session.config['seller_endowment'],
            half_num_round=round(player.session.config['num_rounds']/2,0),
            half_num_round_plus_one=player.session.config['num_rounds'] / 2 + 1,
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
            others_in_group=C.PLAYERS_PER_GROUP-1,
            endowment_1=player.session.config['endowment']*player.session.config['r_1'],
            endowment_2=player.session.config['endowment']*player.session.config['r_2'],
            r_percentage_1=player.session.config['r_1'] * 100,
            r_percentage_2=player.session.config['r_2'] * 100,
            r_percentage_practice=player.session.config['r_practice'] * 100,
            a=player.session.config['a'],
            A=player.session.config['A'],
            b=player.session.config['b'],
            B=player.session.config['B'],
            seller_endowment=player.session.config['seller_endowment'],
            half_num_round=round(player.session.config['num_rounds'] / 2, 0),
            half_num_round_plus_one=player.session.config['num_rounds'] / 2 + 1,

        )


class QuizIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
            others_in_group=C.PLAYERS_PER_GROUP-1,
        )


class Quiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']




class PracticeIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        r_percentage = player.session.config['r_practice'] * 100
        r = player.session.config["r_practice"]
        return dict(
            practice_num_rounds=player.session.config['practice_num_rounds'],
            r=r,
            r_percentage=r_percentage,

            message_practice=player.session.config['message_practice'],
            principal_plus_interest_example=10 * (1 + r)
        )


class WaitForOthers_0(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    title_text = "Please wait"
    body_text = "Waiting while other participants finish their quiz"



class BorrowPractice(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['practice_num_rounds'] and player.role == 'Buyer'

    form_model = 'player'
    form_fields = ['amount_borrowed']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['practice_num_rounds']/2:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment']*(player.session.config['r_practice'])
        else:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])

        return dict(other_role=player.get_others_in_group()[0].role,
                    chat_on=player.session.config['chat_on'],
                    a=player.session.config['a'],
                    A=player.session.config['A'],
                    b=player.session.config['b'],
                    B=player.session.config['B'],
                    endowment=endowment,
                    practice_num_rounds=player.session.config['practice_num_rounds'],
                    r=r,
                    r_percentage=r_percentage,
                    borrow_max=borrow_max,
                    message_practice=player.session.config['message_practice'],
                    principal_plus_interest_example = 10 * (1 + r)
                    )


class WaitForOthers_I(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['practice_num_rounds']

    title_text = "Please wait"
    body_text = "Waiting while your counterpart decides how much money to bring to the meeting"

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.role == 'Seller':
                p.amount_borrowed = p.get_others_in_group()[0].amount_borrowed



class WaitForOthers_00(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    title_text = "Please wait"
    body_text = "Waiting while other Buyers decide how much money to bring to the meeting"




class BargainPractice1(Page):
    timeout_seconds = 150
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
        #return player.round_number <= player.session.config['practice_num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['practice_num_rounds']/2:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
        else:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])

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
                    practice_num_rounds=player.session.config['practice_num_rounds'], )

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


class BargainPractice2(Page):
    timeout_seconds = 120
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2
        #return player.round_number <= player.session.config['practice_num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['practice_num_rounds']/2:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
        else:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])

        return dict(other_role=player.get_others_in_group()[0].role,
                    chat_on=player.session.config['chat_on'],
                    a=player.session.config['a'],
                    A=player.session.config['A'],
                    b=player.session.config['b'],
                    B=player.session.config['B'],
                    q_bar=pow(player.amount_borrowed / player.session.config['B'], 1 / player.session.config['b'])+0.01,
                   # q_bar=pow(player.session.config['endowment']/ player.session.config['B'], 1 / player.session.config['b']),
                  # q_bar=11,
                    endowment=endowment,
                    r=r,
                    r_percentage=r_percentage,
                    borrow_max=borrow_max,
                    practice_num_rounds=player.session.config['practice_num_rounds'], )

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




class ResultsPractice(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['practice_num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['practice_num_rounds']/2:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
        else:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
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
            principal_plus_interest=player.amount_borrowed*(1+r),
            money_left=player.amount_borrowed-player.group.deal_price
        )


class MyWaitPage(WaitPage):
    wait_for_all_groups = True
    template_name = 'live_bargaining_nash_kalai_practice/MyWaitPage.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['practice_num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= player.session.config['practice_num_rounds']/2:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
        else:
            r=player.session.config["r_practice"]
            r_percentage = player.session.config['r_practice'] * 100
            borrow_max = player.session.config['endowment']
            endowment = player.session.config['endowment'] * (player.session.config['r_practice'])
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
#    @staticmethod
#    def is_displayed(player: Player):
#        return player.round_number <= player.session.config['practice_num_rounds']

#    title_text = "Please wait"
#    body_text = "Waiting to be matched with a new counterpart"


page_sequence = [Instructions1,
                 Instructions2,
                 Instructions3,
                 Quiz,
                 WaitForOthers_0,
                 PracticeIntro,
                 BorrowPractice,
                 WaitForOthers_I,
                 WaitForOthers_00,
                 BargainPractice1,
                 BargainPractice2,
                 ResultsPractice,
                 MyWaitPage]
