from otree.api import *
import random

doc = """
Supergames of an indefinitely repeated tullock contest
"""


class C(BaseConstants):
    NAME_IN_URL = 'supergames_tullock_indefinite'
    PLAYERS_PER_GROUP = None

    # this is the number of supergames
    NUM_ROUNDS = 5
 

    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
   # subsession.group_randomly(fixed_id_in_group=False)
    if subsession.round_number == 1:
        players = subsession.get_players()
        for p in players:
            if p.id_in_subsession <= p.session.config['num_active_participants']:
                p.is_playing = True
                p.is_buffering = False
            elif p.id_in_subsession <= p.session.config['num_active_participants']+p.session.config['buffer_size']:
                p.is_playing = False
                p.is_buffering = True
            
            else: 
                p.is_playing = False
                p.is_buffering = False
            p.is_out = False
            p.round_payoff = 0
            
            if p.is_playing is False and not p.is_out:
                p.queue_position=p.id_in_subsession-p.session.config['num_active_participants']



class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


def live_method(player, data):
    group = player.group
    my_id = player.id_in_group

    if group.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(group=group, iteration=group.iteration)

    bid_field = 'bid{}'.format(my_id)
    prediction_field = 'prediction{}'.format(my_id)

    if 'bid' in data:
        
        bid = data['bid']
        prediction=data['prediction']
        
        print('-------------------> bid=',bid)
        print('bid_field =',bid_field)
        print('game =',game)
      
        if getattr(game, bid_field) is not None:
            return
        setattr(game, bid_field, bid)
        setattr(game, prediction_field, prediction)
        print(game)

        
        bids = game.bid1, game.bid2 , game.bid3
        
        print('bids = ',bids)
        print('Games =', Game.filter())
        print('-----------------------------')
        
        

        is_ready = None not in bids
        if is_ready:
            p1, p2, p3 = group.get_players()

            total_bids = float(game.bid1) + float(game.bid2) + float(game.bid3)
            if total_bids==0:
                game.payoff1 = 1/3*player.session.config['V']-float(game.bid1)
                game.payoff2 = 1/3*player.session.config['V']-float(game.bid2)
                game.payoff3 = 1/3*player.session.config['V']-float(game.bid3)
           
            else:
                game.payoff1 = float(game.bid1)/total_bids*player.session.config['V']-float(game.bid1)
                game.payoff2 = float(game.bid2)/total_bids*player.session.config['V']-float(game.bid2)
                game.payoff3 = float(game.bid3)/total_bids*player.session.config['V']-float(game.bid3)
           
           
            p1.bid=float(game.bid1)
            p2.bid=float(game.bid2)
            p3.bid=float(game.bid3)
           
            [p1.last_payoff, p2.last_payoff, p3.last_payoff ] = [game.payoff1, game.payoff2, game.payoff3] 
            # I could do the random draw of the payoff here?? maybe

            game.has_results = True
            group.iteration += 1

            print('---------------------------------- >  final game results =', game)
            
            # random stopping rule
            #if random.random() < 0:  #C.STOPPING_PROBABILITY:
            if group.iteration == 5:
                return {0: dict(finished_sg=True)}

            Game.create(group=group, iteration=group.iteration)

            return {
                0: dict(should_wait=False, last_results=to_dict(game), iteration=group.iteration)
            }
    i_decided = getattr(game, bid_field) is not None
    if group.iteration > 0:
        [prev_game] = Game.filter(group=group, iteration=group.iteration - 1)
        last_results = to_dict(prev_game)
    else:
        last_results = None
    return {
        my_id: dict(
            should_wait=i_decided and not game.has_results,
            last_results=last_results,
            iteration=group.iteration,
        )
    }

def custom_export(players):  # to export the variables that get saved in JS
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'group' 'bids']
    for p in players:
        
        my_id = p.id_in_group
        participant = p.participant
        session = p.session
        group = p.group
        bids = Game.filter(group=p.group)

        
        yield [session.code, participant.code, p.round_number, p.id_in_group, group.id_in_subsession, bids]



class Game(ExtraModel):
    group = models.Link(Group)
    iteration = models.IntegerField()
    bid1 = models.FloatField()
    bid2 = models.FloatField()
    bid3 = models.FloatField()
    payoff1 = models.FloatField()
    payoff2 = models.FloatField()
    payoff3 = models.FloatField()
    prediction1 = models.FloatField()
    prediction2 = models.FloatField()
    prediction3 = models.FloatField()
    
    
    has_results = models.BooleanField(initial=False)


def to_dict(game: Game):
    return dict(payoffs=[game.payoff1, game.payoff2, game.payoff3], bids=[game.bid1, game.bid2, game.bid3], predictions=[game.prediction1, game.prediction2, game.prediction3])


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    bid=models.FloatField()
    last_payoff=models.FloatField()
    is_playing = models.BooleanField()                  # whether they are trading or just waiting to enter
    is_out = models.BooleanField()                      # whether they already played
    is_buffering=models.BooleanField()                  #whether they are reading instructions waiting to enter


# PAGES ---------------------------------------------------------------

class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # make the first one
        Game.create(group=group, iteration=group.iteration)


class Play(Page):
    
    form_model = 'player'
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group,
                    id_in_group=player.id_in_group)

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number==1:
            slider_default_prediction=0
            slider_default_investment=0
        else:
            if player.in_round(player.round_number-1).is_playing is False and player.is_playing is True:
                slider_default_prediction=0
                slider_default_investment=0
            if player.in_round(player.round_number-1).is_playing is True and player.is_playing is True:
                slider_default_prediction=player.in_round(player.round_number-1).prediction
                slider_default_investment=player.in_round(player.round_number-1).investment
        return dict(
            # round_number=player.session.config['num_rounds'],
            endowment= player.session.config['endowment'],
            r=player.session.config['r'],
            V=player.session.config['V'],
            num_others=player.session.config['num_active_participants']-1,
            slider_max=player.session.config['V'],
            slider_min=0,
            slider_default_prediction=slider_default_prediction,
            slider_default_investment=slider_default_investment,  

        )


class Results(Page):
    pass


page_sequence = [WaitToStart, Play, Results]
