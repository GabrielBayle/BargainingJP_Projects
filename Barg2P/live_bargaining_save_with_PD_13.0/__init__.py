from otree.api import *
from datetime import datetime


doc = """
For oTree beginners, it would be simpler to implement this as a discrete-time game 
by using multiple rounds, e.g. 10 rounds, where in each round both players can make a new proposal,
or accept the value from the previous round.

However, the discrete-time version has more limitations
(fixed communication structure, limited number of iterations).

Also, the continuous-time version works smoother & faster, 
and is less resource-intensive since it all takes place in 1 page.
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining_nash_kalai'

    #### BARGAINING

    # Players roles
    PLAYER1_ROLE = 'Player 1'
    PLAYER2_ROLE = 'Player 2'

    # Parameters
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    CONVERSION_RATE = 1
    PIE_SIZE = 1000
    BARGAINING_TIME = 300
    DISAGREEMENT_PAYOFF_P1 = 100
    DISAGREEMENT_PAYOFF_P2 = 400

    # Treatments
    BG = "bargain"
    PD = "prisoner"
    UG = "ultimatum"
    SH = "staghunt"

    #### PRISONER DILEMMA

    betray_payoff_PD = 700
    betrayed_payoff_PD = 0
    mutual_cooperation_payoff_PD = PIE_SIZE // 2
    mutual_betrayal_payoff_PD_p1 = DISAGREEMENT_PAYOFF_P1
    mutual_betrayal_payoff_PD_p2 = DISAGREEMENT_PAYOFF_P2


class Subsession(BaseSubsession):
    conversion_rate = models.FloatField()
    treatment = models.StringField()

    def creating_session(self):
        for group in self.get_groups():
            players = group.get_players()
            players[0].role = C.PLAYER1_ROLE
            players[1].role = C.PLAYER2_ROLE


class Group(BaseGroup):
    share_price = models.CurrencyField()
    is_finished = models.BooleanField(initial=False)


class Player(BasePlayer):
    has_read_instructions = models.BooleanField(initial=False)

    # PRISONER DILEMMA

    PD_decision = models.BooleanField(
        choices=[
            [False, 'Defect'],
            [True, 'Cooperate'],
        ]
    )

    # BARGAINING

    amount_proposed_player1 = models.IntegerField()
    amount_proposed_player2 = models.IntegerField()
    amount_accepted_player1 = models.IntegerField()
    amount_accepted_player2 = models.IntegerField()
    offers_made_player1 = models.LongStringField(initial="")
    offers_made_player2 = models.LongStringField(initial="")
    accepted_shares = models.LongStringField(initial="")
    timeout_occurred = models.BooleanField(initial=False)
    player1_share = models.IntegerField()
    player2_share = models.IntegerField()
    bargain_start_time = models.StringField()
    bargain_end_time = models.StringField()
    stopped_by_player_id = models.IntegerField(initial=0)

    def set_accepted_shares(self, player1_share, player2_share):
        self.accepted_shares = str([player1_share, player2_share])
        self.player1_share = player1_share
        self.player2_share = player2_share

    def add_offer_player1(self, offer):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        offer_with_time = {'offer': offer, 'time': current_time}
        offers = self.get_offers_player1()
        offers.append(offer_with_time)
        self.offers_made_player1 = str(offers)

    def get_offers_player1(self):
        if self.offers_made_player1:
            return eval(self.offers_made_player1)
        else:
            return []

    def add_offer_player2(self, offer):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        offer_with_time = {'offer': offer, 'time': current_time}
        offers = self.get_offers_player2()
        offers.append(offer_with_time)
        self.offers_made_player2 = str(offers)

    def get_offers_player2(self):
        if self.offers_made_player2:
            return eval(self.offers_made_player2)
        else:
            return []


class Bargain2(Page):

    def get(self):
        # Record the current time when the page is accessed
        self.player.bargain_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super().get()

    timeout_seconds = C.BARGAINING_TIME

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        print("Received data:", data)
        group = player.group
        [other] = player.get_others_in_group()

        if 'amount_player1' in data and 'amount_player2' in data:
            try:
                amount_player1 = int(data['amount_player1'])
                amount_player2 = int(data['amount_player2'])
            except ValueError:
                print('Invalid message received', data)
                return

            if data['type'] == 'accept':
                if amount_player1 == other.amount_proposed_player1 and amount_player2 == other.amount_proposed_player2:
                    player.amount_accepted_player1 = amount_player1
                    player.amount_accepted_player2 = amount_player2
                    group.share_price = amount_player1 + amount_player2
                    group.is_finished = True
                    player.set_accepted_shares(amount_player1, amount_player2)
                    other.set_accepted_shares(amount_player1, amount_player2)
                    print(f"Sending finished=True for player {player.id_in_group}")
                    return {0: dict(finished=True)}

            if data['type'] == 'propose':
                player.amount_proposed_player1 = amount_player1
                player.amount_proposed_player2 = amount_player2
                player.add_offer_player1(amount_player1)
                player.add_offer_player2(amount_player2)

            if data['type'] == 'stop_bargaining':
                default_share_player1 = C.DISAGREEMENT_PAYOFF_P1
                default_share_player2 = C.DISAGREEMENT_PAYOFF_P2

                player.amount_accepted_player1 = default_share_player1
                player.amount_accepted_player2 = default_share_player2
                player.set_accepted_shares(default_share_player1, default_share_player2)

                other.amount_accepted_player1 = default_share_player1
                other.amount_accepted_player2 = default_share_player2
                other.set_accepted_shares(default_share_player1, default_share_player2)

                player.stopped_by_player_id = player.id_in_group
                other.stopped_by_player_id = player.id_in_group

                group.share_price = default_share_player1 + default_share_player2
                group.is_finished = True

                print(f"Sending finished=True for player {player.id_in_group}")
                return {0: dict(finished=True)}

        proposals = []
        for p in [player, other]:
            amount_proposed_player1 = p.field_maybe_none('amount_proposed_player1')
            amount_proposed_player2 = p.field_maybe_none('amount_proposed_player2')
            if amount_proposed_player1 is not None and amount_proposed_player2 is not None:
                proposals.append([p.id_in_group, amount_proposed_player1, amount_proposed_player2])

        return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    @staticmethod
    def is_displayed(player: Player):
        """Skip this page if a deal has already been made"""
        group = player.group
        share_price = group.field_maybe_none('share_price')
        return share_price is None

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            group = player.group
            # If timeout occurred, set the timeout_occurred field to True
            player.timeout_occurred = True

            # Assign default shares if the timer runs out
            default_share_player1 = C.DISAGREEMENT_PAYOFF_P1  # Example value
            default_share_player2 = C.DISAGREEMENT_PAYOFF_P2
            player.amount_accepted_player1 = default_share_player1
            player.amount_accepted_player2 = default_share_player2
            player.set_accepted_shares(default_share_player1, default_share_player2)
            group.share_price = default_share_player1 + default_share_player2
        else:
            # If timeout did not occur, ensure timeout_occurred is False
            player.timeout_occurred = False
        player.bargain_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")




class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Parse the accepted_shares string
        if player.accepted_shares:
            accepted_shares = eval(player.accepted_shares)
            player1_share, player2_share = accepted_shares[0], accepted_shares[1]
        else:
            # Default values in case accepted_shares is empty
            player1_share, player2_share = 0, 0

        return {
            'player1_share': player1_share,
            'player2_share': player2_share,
            'timeout_occurred': player.timeout_occurred
        }

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    def before_next_page(player, timeout_happened):
        player.has_read_instructions = True

class InstructionsWaitMonitor(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.session.config.get("instructions_relues", True)

class WaitForGroup(WaitPage):
    pass

class NextAppWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS



##########################################
###### ALTERNATIVE GAMES #################

###### PRISONER DILEMMA

class PDDecisionPage(Page):
    form_model = 'player'
    form_fields = ['PD_decision']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'player_id': player.id_in_group,
            'coop_coop_payoff': C.mutual_cooperation_payoff_PD,
            'defect_coop_payoff_p1': C.betray_payoff_PD,
            'defect_coop_payoff_p2': C.betrayed_payoff_PD,
            'coop_defect_payoff_p1': C.betrayed_payoff_PD,
            'coop_defect_payoff_p2': C.betray_payoff_PD,
            'defect_defect_payoff_p1': C.mutual_betrayal_payoff_PD_p1,
            'defect_defect_payoff_p2': C.mutual_betrayal_payoff_PD_p2,
        }

class PDWaitForGroup(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        PDWaitForGroup.set_payoffs_pd(group)

    @staticmethod
    def set_payoffs_pd(group: Group):
        player1 = group.get_player_by_id(1)
        player2 = group.get_player_by_id(2)

        if player1.PD_decision and player2.PD_decision:
            player1.payoff = C.mutual_cooperation_payoff_PD
            player2.payoff = C.mutual_cooperation_payoff_PD
        elif player1.PD_decision and not player2.PD_decision:
            player1.payoff = C.betrayed_payoff_PD
            player2.payoff = C.betray_payoff_PD
        elif not player1.PD_decision and player2.PD_decision:
            player1.payoff = C.betray_payoff_PD
            player2.payoff = C.betrayed_payoff_PD
        else:
            player1.payoff = C.mutual_betrayal_payoff_PD_p1
            player2.payoff = C.mutual_betrayal_payoff_PD_p2

class PDResultsPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return {
            'other_payoff': other_player.payoff,
            'other_decision_display': "Cooperate" if other_player.PD_decision else "Defect",
            'player_decision_display': "Cooperate" if player.PD_decision else "Defect",
        }


page_sequence = [Introduction, Instructions, InstructionsWaitMonitor,
                 Bargain2, Results, WaitForGroup,
                 PDDecisionPage, PDWaitForGroup, PDResultsPage, WaitForGroup,
                 NextAppWaitForAll]