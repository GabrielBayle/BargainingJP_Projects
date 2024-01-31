from otree.api import *
import random
import numpy
import time

doc = """
Supergames of an indefinitely repeated tullock contest
"""


class C(BaseConstants):
    NAME_IN_URL = 'supergames_tullock_indefinite'
    PLAYERS_PER_GROUP = None

    # this is the number of supergames
    NUM_ROUNDS = 10
    
 

    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'


class Subsession(BaseSubsession):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)

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

          #      # make the first one
        
    Game.create(subsession=subsession, iteration=subsession.iteration)

class Group(BaseGroup):
    pass
  #  iteration = models.IntegerField(initial=0)



def live_method(player, data):
    subsession = player.subsession
    my_id = player.id_in_subsession

    if subsession.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(subsession=subsession, iteration=subsession.iteration)

    bid_field = 'bid{}'.format(my_id)
    prediction_field = 'prediction{}'.format(my_id)
    
    if 'bid' in data:
        bid = data['bid']
        bid=float(bid)
        prediction=data['prediction']
        prediction=float(prediction)
        
        print('-------------------> bid=',bid)
        print('bid_field =',bid_field)
        print('game =',game)
      
        if getattr(game, bid_field) is not None:
            return
        setattr(game, bid_field, bid)
        setattr(game, prediction_field, prediction)
        print(game)

    
        
        bids = game.bid1, game.bid2 , game.bid3, game.bid4, game.bid5, game.bid6 
        
        print('bids = ',bids)
        print('Games =', Game.filter())
        print('-----------------------------')
        
        

        is_ready = False
        if sum(x is not None for x in bids)==3:
            is_ready = True
     
     
        if is_ready:
            if  subsession.session.config['num_demo_participants']==3:
                p1, p2, p3 = [p for p in  subsession.get_players() ]
            else:
                p1, p2, p3,p4,p5,p6 = [p for p in  subsession.get_players() ]
           
            total_bids = sum(filter(None, [game.bid1, game.bid2 , game.bid3, game.bid4, game.bid5, game.bid6]))
            print('total bids = ' , total_bids)
           
            if game.bid1 is not None:
                if total_bids==0:
                   game.payoff1 = round(1/3*player.session.config['V'],2)
                else:
                    game.payoff1 = round(player.session.config['endowment']+float(game.bid1)/total_bids*player.session.config['V']-float(game.bid1),2)
                p1.last_bid=game.bid1
                p1.last_payoff=game.payoff1
                p1.last_prediction=game.prediction1
            if game.bid2 is not None:
                if total_bids==0:
                    game.payoff2 = round(1/3*player.session.config['V'],2)
                else:                
                    game.payoff2 = round(player.session.config['endowment']+float(game.bid2)/total_bids*player.session.config['V']-float(game.bid2),2)
                p2.last_bid=game.bid2
                p2.last_payoff=game.payoff2
                p2.last_prediction=game.prediction2
            if game.bid3 is not None:
                if total_bids==0:
                    game.payoff3 = round(1/3*player.session.config['V'],2)
                else:
                    game.payoff3 = round(player.session.config['endowment']+float(game.bid3)/total_bids*player.session.config['V']-float(game.bid3),2)
                p3.last_bid=game.bid3
                p3.last_payoff=game.payoff3
                p3.last_prediction=game.prediction3
            if game.bid4 is not None:
                if total_bids==0:
                    game.payoff4 = 1/3*player.session.config['V']
                else:
                    game.payoff4 = player.session.config['endowment']+float(game.bid4)/total_bids*player.session.config['V']-float(game.bid4)                               
                p4.last_bid=game.bid4
                p4.last_payoff=game.payoff4
                p4.last_prediction=game.prediction4
            if game.bid5 is not None:
                if total_bids==0:
                    game.payoff5 = 1/3*player.session.config['V']
                else:      
                    game.payoff5 = player.session.config['endowment']+float(game.bid5)/total_bids*player.session.config['V']-float(game.bid5)
                p5.last_bid=game.bid5
                p5.last_payoff=game.payoff5
                p5.last_prediction=game.prediction5
            if game.bid6 is not None:
                if total_bids==0:
                    game.payoff6 = 1/3*player.session.config['V']
                else:
                    game.payoff6 = player.session.config['endowment']+float(game.bid6)/total_bids*player.session.config['V']-float(game.bid6)
                p6.last_bid=game.bid6
                p6.last_payoff=game.payoff6
                p6.last_prediction=game.prediction6
           
            game.has_results = True
            subsession.iteration += 1

            print('---------------------------------- >  final game results =', game)
            
            # random stopping rule
            #if random.random() < 0:  #C.STOPPING_PROBABILITY:
            if subsession.iteration == 7:
                return {0: dict(finished_sg=True)}

            Game.create(subsession=subsession, iteration=subsession.iteration)

            return {
                0: dict(should_wait=False, last_results=to_dict(game), iteration=subsession.iteration)
            }
    i_decided = getattr(game, bid_field) is not None
    if subsession.iteration > 0:
        [prev_game] = Game.filter(subsession=subsession, iteration=subsession.iteration - 1)
        last_results =  to_dict(prev_game)
    else:
        last_results = None
    return {
        my_id: dict(
            should_wait=i_decided and not game.has_results,
            last_results=last_results,
            iteration=subsession.iteration,
        )
    }

def custom_export(players):  # to export the variables that get saved in JS
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'group' 'bids']
    for p in players:
        
        participant = p.participant
        session = p.session
        bids = Game.filter(subsession=p.subsession)
        
        yield [session.code, participant.code, p.round_number, p.id_in_group, p.id_in_subsession, bids]



class Game(ExtraModel):
    subsession= models.Link(Subsession)
    iteration = models.IntegerField()
    bid1 = models.FloatField()
    bid2 = models.FloatField()
    bid3 = models.FloatField()
    bid4 = models.FloatField()
    bid5 = models.FloatField()
    bid6 = models.FloatField()
    payoff1 = models.FloatField()
    payoff2 = models.FloatField()
    payoff3 = models.FloatField()
    payoff4 = models.FloatField()
    payoff5 = models.FloatField()
    payoff6 = models.FloatField()
    prediction1 = models.FloatField()
    prediction2 = models.FloatField()
    prediction3 = models.FloatField()    
    prediction4 = models.FloatField()
    prediction5 = models.FloatField()
    prediction6 = models.FloatField()
    has_results = models.BooleanField(initial=False)


def to_dict(game: Game):
    return dict(payoffs=[game.payoff1, game.payoff2, game.payoff3, game.payoff4, game.payoff5, game.payoff6], bids=[game.bid1, game.bid2, game.bid3, game.bid4, game.bid5, game.bid6], predictions=[game.prediction1, game.prediction2, game.prediction3, game.prediction3, game.prediction4, game.prediction5, game.prediction6])

class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    last_bid=models.FloatField()
    last_payoff=models.FloatField()
    
    
    last_prediction=models.FloatField()
    is_playing = models.BooleanField()                  # whether they are trading or just waiting to enter
    is_out = models.BooleanField()                      # whether they already played
    is_buffering=models.BooleanField()                  #whether they are reading instructions waiting to enter
    queue_position=models.FloatField()                  # position in the queue outside

# FUNCTIONS

def new_round(subsession: Subsession):
    players = subsession.get_players()
    for p in players:
        p.in_round(p.round_number+1).is_playing = p.is_playing
        p.in_round(p.round_number+1).is_out = p.is_out
        p.in_round(p.round_number+1).is_buffering = p.is_buffering
        if not p.is_playing and not p.is_out:
            p.in_round(p.round_number+1).queue_position = p.queue_position-1 


def player_leaves(subsession: Subsession):
    players = subsession.get_players()
    # for the random treatment
    if subsession.session.config['pressure'] is False:
        expelled_id = numpy.random.choice([x for x in players if x.is_playing is True])
        print('player leaving is', expelled_id.id_in_subsession)
        for i in range(subsession.round_number+1, subsession.session.config['num_supergames']+1):
            expelled_id.in_round(i).is_out = True
            expelled_id.in_round(i).is_playing = False
            expelled_id.in_round(i).is_buffering = False

    # for the pressure treatment
    else:
        players_aux = [x for x in subsession.get_players() if x.is_playing is True]
        expelled_id = sorted(players_aux, key=lambda player: player.last_payoff)[0]
        print('player leaving is', expelled_id.id_in_subsession)
        for i in range(subsession.round_number+1, subsession.session.config['num_supergames']+1):
            expelled_id.in_round(i).is_out = True
            expelled_id.in_round(i).is_playing = False
            expelled_id.in_round(i).is_buffering = False
            
def player_enters_buffer(subsession: Subsession): 
# selects the entering participant  to buffer  
    players = subsession.get_players()
    for p in players:
        if not p.is_playing  and not p.is_out and not p.is_buffering  and p.queue_position==subsession.session.config['buffer_size']+1:  
            new_entrant_buffer=p
            new_entrant_buffer.in_round(subsession.round_number + 1).is_buffering = True
            break 

def player_enters(subsession: Subsession): 
# selects the entering participant   from buffer to game
    players = subsession.get_players()
    for p in players:
        if not p.is_playing  and not p.is_out and p.is_buffering  and p.queue_position==1:   
            new_entrant=p 
            break
       
    print('new entrant is =',new_entrant.id_in_subsession)
    new_entrant.in_round(subsession.round_number+1).is_playing = True
    new_entrant.in_round(subsession.round_number + 1).is_out = False
    new_entrant.in_round(subsession.round_number + 1).is_buffering = False
    

# PAGES ---------------------------------------------------------------

class WaitToStart(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_out is False
    wait_for_all_groups=True
    def after_all_players_arrive(subsession : Subsession):
        new_round(subsession)

class Instructions1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_supergames'],
            endowment=player.session.config['endowment'],
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            duration=player.session.config['duration'],
            pressure=player.session.config['pressure'],
           # proportional=player.session.config['proportional'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,
        )

class Instructions2(Page):
    @staticmethod
    def is_displayed(player: Player):
          # needs to change depending on how many rounds we give them to read instructions 
        return (player.round_number == 1 and player.is_playing) or (player.round_number == 1 and player.is_buffering) or (player.round_number > 1 and player.is_buffering and not player.in_round(player.round_number-1).is_buffering)
    #or (player.is_buffering and player.round_number == 1) or (player.round_number>1 and player.in_round(player.round_number-1).is_buffering is False and player.is_buffering)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            pressure=player.session.config['pressure'],
         #   proportional=player.session.config['proportional'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            
        )

class Play(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and player.is_playing is True 
    
    form_model = 'player'
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_subsession,
                    id_in_group=player.id_in_subsession)

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
                slider_default_prediction=player.in_round(player.round_number-1).last_prediction
                slider_default_investment=player.in_round(player.round_number-1).last_bid
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
            num_demo=player.session.config['num_demo_participants']

        )
class  WaitForResults(WaitPage): 
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out
      
    wait_for_all_groups = True 
    title_text = "Waiting to enter "
    body_text = "Please wait you'll join soon"
    wait_for_all_groups=True
    @staticmethod
    def after_all_players_arrive(subsession : Subsession):
        print('aaaaaaaaaaaaa')
        player_leaves(subsession)
        player_enters_buffer(subsession)
        player_enters(subsession)

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and player.is_playing is True 
    

class WaitBeforeNextRound(WaitPage):
   # template_name = 'Tullock/WaitToEnter.html'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_playing and not player.is_out

    wait_for_all_groups = True
    title_text = "Waiting to enter "
    body_text = "Please wait you'll join soon"

    @staticmethod
    def vars_for_template(player: Player):
        pass
   #     queue_and_time(player)
   #     if player.is_buffering:
   #         tlimit=(player.session.config['tlimit'])*player.buffer_wait_rounds
   #     else:
   #          tlimit=(player.session.config['tlimit'])*player.wait_rounds
   #     
   #     return dict(
   #                 queue_position=player.queue_position-player.session.config['buffer_size'],
   #                 buffer_queue_position=player.queue_position,
   #                 tlimit=tlimit
   #             )

page_sequence = [WaitToStart, 
                 #Instructions1, 
                 Instructions2,  
                 Play, 
                 WaitForResults, 
                 Results, 
                 WaitBeforeNextRound]
