from otree.api import *
from datetime import datetime
import random


doc = """
If you want to run X rounds of the same treatment enter either "bargain", "prisoner, "staghunt" or "ultimatum". If you
want to run one session including all games, enter "test".

Fill the following fields: "", "".

The number of players have to be multiple of 2. If you want to ensure perfect stranger matching, you need at least 10
players.
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'

    #### BARGAINING

    # Players roles
    PLAYER1_ROLE = 'Player 1'
    PLAYER2_ROLE = 'Player 2'

    # Parameters
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
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
    TEST = "test"

    #### PRISONER DILEMMA

    betray_payoff_PD = 700
    betrayed_payoff_PD = 0
    mutual_cooperation_payoff_PD = PIE_SIZE // 2
    mutual_betrayal_payoff_PD_p1 = DISAGREEMENT_PAYOFF_P1
    mutual_betrayal_payoff_PD_p2 = DISAGREEMENT_PAYOFF_P2

    #### STAG HUNT
    stag_hare_payoff = 0
    hare_stag_payoff_p1 = DISAGREEMENT_PAYOFF_P1
    hare_stag_payoff_p2 = DISAGREEMENT_PAYOFF_P2
    both_stag_payoff = PIE_SIZE // 2
    both_hare_payoff_p1 = DISAGREEMENT_PAYOFF_P1
    both_hare_payoff_p2 = DISAGREEMENT_PAYOFF_P2

    #### STAG HUNT
    reject_payoff_p1 = DISAGREEMENT_PAYOFF_P1
    reject_payoff_p2 = DISAGREEMENT_PAYOFF_P2


class Subsession(BaseSubsession):
    conversion_rate = models.FloatField()
    treatment = models.StringField()

    def creating_session(self):
        selected_treatment = self.session.config.get('treatment', 'default_treatment')


        for group in self.get_groups():
            players = group.get_players()
            players[0].role = C.PLAYER1_ROLE
            players[1].role = C.PLAYER2_ROLE

            group.treatment = selected_treatment
            for player in players:
                player.treatment = selected_treatment


class Group(BaseGroup):
    share_price = models.CurrencyField()
    is_finished = models.BooleanField(initial=False)
    is_stopped = models.BooleanField(initial=False)


class Player(BasePlayer):
    has_read_instructions = models.BooleanField(initial=False)
    paid_round = models.IntegerField()
    main_task_payoff = models.IntegerField()
    converted_payoff = models.IntegerField()
    total_payoff = models.CurrencyField()

    # PRISONER DILEMMA

    PD_decision = models.BooleanField(
        choices=[
            [False, 'Defect'],
            [True, 'Cooperate'],
        ]
    )

    # STAG HUNT

    SH_decision = models.BooleanField(
        choices=[
            [False, 'Hare'],
            [True, 'Stag'],
        ]
    )

    # ULTIMATUM

    UG_proposer_decision = models.IntegerField()
    UG_responder_decision = models.BooleanField(
        choices=[
            [False, 'Reject'],
            [True, 'Accept'],
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
                group.is_stopped = True

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

class BLWaitForGroup(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        BLWaitForGroup.set_payoffs_bargain(group)

    @staticmethod
    def set_payoffs_bargain(group: Group):
        player1, player2 = group.get_players()

        # If an agreement is reached
        if group.is_finished:
            player1.payoff = int(player1.amount_accepted_player1)
            player2.payoff = int(player1.amount_accepted_player2)
        else:
            # If no agreement is reached, use disagreement payoffs
            player1.payoff = C.DISAGREEMENT_PAYOFF_P1
            player2.payoff = C.DISAGREEMENT_PAYOFF_P2

        # Update accepted shares and ensure they are integers
        player1.player1_share = int(player1.payoff)
        player1.player2_share = int(player2.payoff)
        player2.player1_share = int(player1.payoff)
        player2.player2_share = int(player2.payoff)

        # Update accepted shares string representation
        player1.set_accepted_shares(player1.player1_share, player1.player2_share)
        player2.set_accepted_shares(player2.player1_share, player2.player2_share)


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
        return (player.round_number == 1 or player.session.config.get('treatment') == C.TEST)


    def before_next_page(player, timeout_happened):
        player.has_read_instructions = True

class InstructionsWaitMonitor(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.session.config.get("instructions_relues", True)

class InstructionsWaitForAll(WaitPage):
    wait_for_all_groups = True

class WaitForGroup(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        players = subsession.get_players()

        # Separate players by role
        player1s = [p for p in players if p.role == C.PLAYER1_ROLE]
        player2s = [p for p in players if p.role == C.PLAYER2_ROLE]

        # Shuffle each list
        random.shuffle(player1s)
        random.shuffle(player2s)

        # Pair players with different roles
        pairs = list(zip(player1s, player2s))

        # Update group membership
        subsession.set_group_matrix(pairs)


class FinalWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class FinalResultsPage(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        # Randomly select a round to be paid
        player.paid_round = random.randint(1, C.NUM_ROUNDS)

        # Find the corresponding payoff
        selected_round_player = player.in_round(player.paid_round)
        player.main_task_payoff = int(selected_round_player.payoff)

        # Calculate the converted payoff
        player.converted_payoff = int(player.main_task_payoff * C.CONVERSION_RATE)

        # Add the participant fee (assuming it's a constant or from session config)
        participation_fee = player.session.config.get('participation_fee', 0)
        player.total_payoff = player.converted_payoff + participation_fee

        round_details = []
        for round_number, p in enumerate(player.in_all_rounds(), start=1):
            round_details.append({
                'round_number': round_number,
                'payoff': p.payoff,
                'is_paid_round': (round_number == player.paid_round)
            })

        return {
            'round_details': round_details,
            'paid_round': player.paid_round,
            'main_task_payoff': player.main_task_payoff,
            'converted_payoff': player.converted_payoff,
            'total_payoff': player.total_payoff
        }


########################################################################################################################
########################################################################################################################
########################################################################################################################


########################################################################################################################
###### PRISONER DILEMMA
########################################################################################################################

class PDDecisionPage(Page):
    form_model = 'player'
    form_fields = ['PD_decision']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 2) or \
            player.session.config.get('treatment') == C.PD and (group.is_stopped or player.timeout_occurred)

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
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 2) or \
            player.session.config.get('treatment') == C.PD and (group.is_stopped or player.timeout_occurred)

    @staticmethod
    def after_all_players_arrive(group: Group):
        PDWaitForGroup.set_payoffs_pd(group)
        PDWaitForGroup.set_shares_pd(group)

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

    @staticmethod
    def set_shares_pd(group: Group):
        player1, player2 = group.get_players()

        # Set amount_accepted to 0 for both players
        player1.amount_accepted_player1 = 0
        player1.amount_accepted_player2 = 0
        player2.amount_accepted_player1 = 0
        player2.amount_accepted_player2 = 0

        # Set accepted_shares to [0, 0] for both players
        player1.accepted_shares = str([0, 0])
        player2.accepted_shares = str([0, 0])

        # Convert payoffs to int and set player1_share and player2_share based on payoffs
        player1_payoff_as_int = int(player1.payoff)
        player2_payoff_as_int = int(player2.payoff)

        player1.player1_share = player1_payoff_as_int
        player2.player1_share = player2_payoff_as_int
        player1.player2_share = player2_payoff_as_int
        player2.player2_share = player1_payoff_as_int

        # Set group.share_price as the sum of player shares
        group.share_price = player1.player1_share + player1.player2_share

class PDResultsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 2) or \
            player.session.config.get('treatment') == C.PD and (group.is_stopped or player.timeout_occurred)

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return {
            'other_payoff': other_player.payoff,
            'other_decision_display': "Cooperate" if other_player.PD_decision else "Defect",
            'player_decision_display': "Cooperate" if player.PD_decision else "Defect",
        }

########################################################################################################################
###### STAG HUNT
########################################################################################################################

class SHDecisionPage(Page):
    form_model = 'player'
    form_fields = ['SH_decision']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 3) or \
            player.session.config.get('treatment') == C.SH and (group.is_stopped or player.timeout_occurred)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'player_id': player.id_in_group,
            'both_stag_payoff': C.both_stag_payoff,
            'hare_stag_payoff_p1': C.hare_stag_payoff_p1,
            'hare_stag_payoff_p2': C.hare_stag_payoff_p2,
            'stag_hare_payoff': C.stag_hare_payoff,
            'both_hare_payoff_p1': C.both_hare_payoff_p1,
            'both_hare_payoff_p2': C.both_hare_payoff_p2,
        }

class SHWaitForGroup(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 3) or \
            player.session.config.get('treatment') == C.SH and (group.is_stopped or player.timeout_occurred)

    @staticmethod
    def after_all_players_arrive(group: Group):
        SHWaitForGroup.set_payoffs_sh(group)
        SHWaitForGroup.set_shares_sh(group)

    @staticmethod
    def set_payoffs_sh(group: Group):
        player1 = group.get_player_by_id(1)
        player2 = group.get_player_by_id(2)

        if player1.SH_decision and player2.SH_decision:
            player1.payoff = C.both_stag_payoff
            player2.payoff = C.both_stag_payoff
        elif player1.SH_decision and not player2.SH_decision:
            player1.payoff = C.stag_hare_payoff
            player2.payoff = C.hare_stag_payoff_p1
        elif not player1.SH_decision and player2.SH_decision:
            player1.payoff = C.hare_stag_payoff_p2
            player2.payoff = C.stag_hare_payoff
        else:
            player1.payoff = C.both_hare_payoff_p1
            player2.payoff = C.both_hare_payoff_p2

    @staticmethod
    def set_shares_sh(group: Group):
        player1, player2 = group.get_players()

        # Set amount_accepted to 0 for both players
        player1.amount_accepted_player1 = 0
        player1.amount_accepted_player2 = 0
        player2.amount_accepted_player1 = 0
        player2.amount_accepted_player2 = 0

        # Set accepted_shares to [0, 0] for both players
        player1.accepted_shares = str([0, 0])
        player2.accepted_shares = str([0, 0])

        # Convert payoffs to int and set player1_share and player2_share based on payoffs
        player1_payoff_as_int = int(player1.payoff)
        player2_payoff_as_int = int(player2.payoff)

        player1.player1_share = player1_payoff_as_int
        player2.player1_share = player2_payoff_as_int
        player1.player2_share = player2_payoff_as_int
        player2.player2_share = player1_payoff_as_int

        # Set group.share_price as the sum of player shares
        group.share_price = player1.player1_share + player1.player2_share

class SHResultsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return (player.session.config.get('treatment') == C.TEST and player.round_number == 3) or \
            player.session.config.get('treatment') == C.SH and (group.is_stopped or player.timeout_occurred)

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return {
            'other_payoff': other_player.payoff,
            'other_decision_display': "Stag" if other_player.SH_decision else "Hare",
            'player_decision_display': "Stag" if player.SH_decision else "Hare",
        }

########################################################################################################################
###### ULTIMATUM
########################################################################################################################
class UGPropositionPage(Page):
    form_model = 'player'
    form_fields = ['UG_proposer_decision']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.role == C.PLAYER2_ROLE and \
            ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'player_id': player.id_in_group,
            'reject_payoff_p1': C.reject_payoff_p1,
            'reject_payoff_p2': C.reject_payoff_p2,
        }

class UGPropositionWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.role == C.PLAYER1_ROLE and \
            ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

class UGResponsePage(Page):
    form_model = 'player'
    form_fields = ['UG_responder_decision']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.role == C.PLAYER1_ROLE and \
            ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        proposer = group.get_player_by_role(C.PLAYER2_ROLE)
        return {
            'proposed_amount': proposer.UG_proposer_decision,
            'reject_payoff_p1': C.reject_payoff_p1,
            'reject_payoff_p2': C.reject_payoff_p2,
        }

class UGResponseWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.role == C.PLAYER2_ROLE and \
            ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

class UGWaitForGroup(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

    @staticmethod
    def after_all_players_arrive(group: Group):
        UGWaitForGroup.set_payoffs_ug(group)
        UGWaitForGroup.set_shares_ug(group)

    @staticmethod
    def set_payoffs_ug(group: Group):
        player1 = group.get_player_by_id(1)  # Responder
        player2 = group.get_player_by_id(2)  # Proposer

        # If the responder accepts the offer
        if player1.UG_responder_decision:
            player1.payoff = player2.UG_proposer_decision  # Amount offered to Player 1
            player2.payoff = C.PIE_SIZE - player2.UG_proposer_decision  # Remaining amount
        else:
            # If the offer is rejected, both players receive disagreement payoffs
            player1.payoff = C.DISAGREEMENT_PAYOFF_P1
            player2.payoff = C.DISAGREEMENT_PAYOFF_P2

    @staticmethod
    def set_shares_ug(group: Group):
        player1, player2 = group.get_players()

        # Set amount_accepted to 0 for both players
        player1.amount_accepted_player1 = 0
        player1.amount_accepted_player2 = 0
        player2.amount_accepted_player1 = 0
        player2.amount_accepted_player2 = 0

        # Set accepted_shares to [0, 0] for both players
        player1.accepted_shares = str([0, 0])
        player2.accepted_shares = str([0, 0])

        # Convert payoffs to int and set player1_share and player2_share based on payoffs
        player1_payoff_as_int = int(player1.payoff)
        player2_payoff_as_int = int(player2.payoff)

        player1.player1_share = player1_payoff_as_int
        player2.player1_share = player2_payoff_as_int
        player1.player2_share = player2_payoff_as_int
        player2.player2_share = player1_payoff_as_int

        # Set group.share_price as the sum of player shares
        group.share_price = player1.player1_share + player1.player2_share

class UGResultsPage(Page):

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return ((player.session.config.get('treatment') == C.TEST and player.round_number == 4) or \
             (player.session.config.get('treatment') == C.UG and (group.is_stopped or player.timeout_occurred)))

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        proposer = group.get_player_by_id(2)
        responder = group.get_player_by_id(1)

        return {
            'proposer_offer': proposer.UG_proposer_decision,
            'responder_decision': 'Accepted' if responder.UG_responder_decision else 'Rejected',
            'proposer_payoff': proposer.payoff,
            'responder_payoff': responder.payoff,
        }






page_sequence = [Introduction, Instructions, InstructionsWaitMonitor, InstructionsWaitForAll,
                 Bargain2, BLWaitForGroup, Results, WaitForGroup,
                 PDDecisionPage, PDWaitForGroup, PDResultsPage, WaitForGroup,
                 SHDecisionPage, SHWaitForGroup, SHResultsPage, WaitForGroup,
                 UGPropositionPage, UGPropositionWaitPage, UGResponsePage, UGResponseWaitPage, UGWaitForGroup, UGResultsPage, WaitForGroup,
                 FinalWaitForAll, FinalResultsPage]