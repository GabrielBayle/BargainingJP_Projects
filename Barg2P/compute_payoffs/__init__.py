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
    paid_round = models.IntegerField()
    main_task_payoff = models.IntegerField()
    converted_payoff = models.IntegerField()
    total_payoff = models.CurrencyField()
    participation_fee = models.CurrencyField()
    decision_making_feedback = models.LongStringField()
    experiment_feedback = models.LongStringField()

# def vars_for_admin_report(subsession: Subsession):
#     infos = list()
#     for p in subsession.get_players():
#         infos.append(
#             dict(
#                 label=p.participant.label,
#                 part_1=cu(0) if not "live_bargaining" in p.participant.vars.keys() else
#                 p.participant.vars["live_bargaining"]["payoff"],
#                 part_2=cu(0) if not "targetNLE" in p.participant.vars.keys() else
#                 p.participant.vars["targetNLE"]["payoff"],
#                 payoff=p.participant.payoff
#             )
#         )
#     return dict(infos=infos)

def compute_final_payoff(player: Player):

    player.payoff = player.participant.vars["bargain_payoff"]
    player.payoff += player.participant.vars["targetNLE"]["payoff"]
    # player.payoff += player.participant.vars["svo"]["payoff"]

    participation_fee = player.session.config.get('participation_fee', 0)
    player.payoff += participation_fee

    player.participant.payoff = player.payoff

    final_text = f"Your final payoff for the experiment is {player.participant.payoff}."

    player.participant.vars["final_text"] = final_text


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