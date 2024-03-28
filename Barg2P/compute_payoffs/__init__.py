from otree.api import *


doc = """

"""

PLAYERS1, PLAYERS2, pairs, swap = None, None, None, None

class C(BaseConstants):
    NAME_IN_URL = 'compute_payoffs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision_making_feedback = models.LongStringField()
    experiment_feedback = models.LongStringField()


def compute_final_payoff(player: Player):
    paid_round = player.participant.vars['bargain_paid_round']
    nle_paid_round = player.participant.vars["targetNLE"]["nle_paid_round"]
    part1 = player.participant.vars["bargain_payoff"]
    part2 = player.participant.vars["targetNLE"]["payoff"]

    player.payoff = player.participant.vars["bargain_payoff"]
    player.payoff += player.participant.vars["targetNLE"]["payoff"]
    # player.payoff += player.participant.vars["svo"]["payoff"]

    participation_fee = player.session.config.get('participation_fee', 0)
    player.payoff += participation_fee

    player.participant.payoff = player.payoff

    player.participant.vars["paid_round"] = paid_round
    player.participant.vars["nle_paid_round"] = nle_paid_round
    player.participant.vars["part1"] = part1
    player.participant.vars["part2"] = part2
    player.participant.vars["participation_fee"] = participation_fee


########################################################################################################################
########################################################################################################################
########################################################################################################################

class BeforeFinal(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        compute_final_payoff(player)


class FeedbackPage(Page):
    form_model = 'player'
    form_fields = ['decision_making_feedback', 'experiment_feedback']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class EndPage(Page):

    def vars_for_template(player):
        participation_fee = player.session.config.get('participation_fee', 0)



page_sequence = [BeforeFinal, FeedbackPage, EndPage]