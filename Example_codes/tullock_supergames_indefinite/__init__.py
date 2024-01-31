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
    NUM_ROUNDS = 15
    
 

    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'


class Subsession(BaseSubsession):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)

def creating_session(subsession: Subsession):
   # subsession.group_randomly(fixed_id_in_group=False)
    if subsession.round_number == 1:
        print('----------------NEW GAME----------------' )
        players = subsession.get_players()
        for p in players:
            if p.id_in_subsession <= p.session.config['num_active_participants']:
                p.is_playing = True
                p.is_buffering = False
                p.is_reading_instructions=True
                p.position=p.id_in_subsession
            
            elif p.id_in_subsession <= p.session.config['num_active_participants']+p.session.config['buffer_size']:
                p.is_playing = False
                p.is_buffering = True
                p.is_reading_instructions=True
            else: 
                p.is_playing = False
                p.is_buffering = False
                p.is_reading_instructions=False
            
            p.is_out = False
          #  p.round_payoff = 0
            p.will_read_instructions=False
            
            if p.is_playing is False and not p.is_out:
                p.queue_position=p.id_in_subsession-p.session.config['num_active_participants']

        subsession.session.vars['number_of_expelled'] =0
            
          #      # make the first one
        
    Game.create(subsession=subsession, iteration=subsession.iteration)

    
class Group(BaseGroup):
    pass
  

def live_method(player, data):
    subsession = player.subsession
    my_id_game = player.position
    my_id =player.id_in_subsession
    
    if subsession.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(subsession=subsession, iteration=subsession.iteration)

    bid_field = 'bid{}'.format(my_id_game)
    prediction_field = 'prediction{}'.format(my_id_game)
    
    if 'bid' in data:
        bid = data['bid']
        bid=float(bid)
        prediction=data['prediction']
        prediction=float(prediction)
        
        print('-------------------> bid=',bid)
        print('bid_field =',bid_field)
   
      
        if getattr(game, bid_field) is not None:
            return
        setattr(game, bid_field, bid)
        setattr(game, prediction_field, prediction)
        
        print('game =',game)
        

    
        
        bids = game.bid1, game.bid2 , game.bid3, game.bid4
        
        print('bids = ',bids)
      #  print('Games =', Game.filter())
        print('-----------------------------')
        
        

        is_ready = False
        if sum(x is not None for x in bids)==player.session.config['num_active_participants']:
            is_ready = True
     
    
        if is_ready:

                   
            p_aux = [x for x in subsession.get_players() if x.is_playing is True]
            if player.session.config['num_active_participants']==3:
                p1 ,p2, p3 = sorted(p_aux, key=lambda player: player.position)
            if player.session.config['num_active_participants']==4:
                p1 ,p2, p3, p4 = sorted(p_aux, key=lambda player: player.position)
            
            total_bids = sum(filter(None, [game.bid1, game.bid2 , game.bid3, game.bid4]))
            print('total bids = ' , total_bids)
           
            if game.bid1 is not None:
                if total_bids==0:
                   game.payoff1 = round(1/player.session.config['num_active_participants']*player.session.config['V'],2)
                else:
                    game.payoff1 = round(player.session.config['endowment']+float(game.bid1)/total_bids*player.session.config['V']-float(game.bid1),2)
                p1.last_bid=game.bid1
                p1.last_payoff=game.payoff1
                p1.last_prediction=game.prediction1
            if game.bid2 is not None:
                if total_bids==0:
                    game.payoff2 = round(1/player.session.config['num_active_participants']*player.session.config['V'],2)
                else:                
                    game.payoff2 = round(player.session.config['endowment']+float(game.bid2)/total_bids*player.session.config['V']-float(game.bid2),2)
                p2.last_bid=game.bid2
                p2.last_payoff=game.payoff2
                p2.last_prediction=game.prediction2
            if game.bid3 is not None:
                if total_bids==0:
                    game.payoff3 = round(1/player.session.config['num_active_participants']*player.session.config['V'],2)
                else:
                    game.payoff3 = round(player.session.config['endowment']+float(game.bid3)/total_bids*player.session.config['V']-float(game.bid3),2)
                p3.last_bid=game.bid3
                p3.last_payoff=game.payoff3
                p3.last_prediction=game.prediction3
            if game.bid4 is not None:
                if total_bids==0:
                    game.payoff4 =round(1/player.session.config['num_active_participants']*player.session.config['V'],2)
                else:
                    game.payoff4 = round(player.session.config['endowment']+float(game.bid4)/total_bids*player.session.config['V']-float(game.bid4),2)                             
                p4.last_bid=game.bid4
                p4.last_payoff=game.payoff4
                p4.last_prediction=game.prediction4
            game.has_results = True
            subsession.iteration += 1

            print('---------------------------------- >  final game results =', game)
            
            # random stopping rule
            #if random.random() < 0:  #C.STOPPING_PROBABILITY:
            if subsession.iteration == subsession.session.config['supergames'][subsession.round_number-1]:
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
    yield ['session', 'participant_code',  'round_number', 'position', 'id_in_group', 'bids']
    for p in players:
        if p.is_playing:
            participant = p.participant
            session = p.session
            bids = Game.filter(subsession=p.subsession)
                 
            yield [session.code, participant.code, p.round_number, p.position, bids]



class Game(ExtraModel):
    subsession= models.Link(Subsession)
    iteration = models.IntegerField()
    bid1 = models.FloatField()
    bid2 = models.FloatField()
    bid3 = models.FloatField()
    bid4 = models.FloatField()

    payoff1 = models.FloatField()
    payoff2 = models.FloatField()
    payoff3 = models.FloatField()
    payoff4 = models.FloatField()

    prediction1 = models.FloatField()
    prediction2 = models.FloatField()
    prediction3 = models.FloatField()    
    prediction4 = models.FloatField()    

    has_results = models.BooleanField(initial=False)



def to_dict(game: Game):
    if game.subsession.session.config['num_active_participants']==3:
        return dict(payoffs=[game.payoff1, game.payoff2, game.payoff3,], bids=[game.bid1, game.bid2, game.bid3], predictions=[game.prediction1, game.prediction2, game.prediction3])
    if game.subsession.session.config['num_active_participants']==4:
        return dict(payoffs=[game.payoff1, game.payoff2, game.payoff3, game.payoff4], bids=[game.bid1, game.bid2, game.bid3, game.bid4], predictions=[game.prediction1, game.prediction2, game.prediction3, game.prediction4])
    
class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    last_bid=models.FloatField()
    last_prediction=models.FloatField()
    last_payoff=models.FloatField()
    
    
    
    is_playing = models.BooleanField()                  # whether they are trading or just waiting to enter
    is_out = models.BooleanField()                      # whether they already played
    is_buffering=models.BooleanField()                  #whether they are reading instructions waiting to enter
    queue_position=models.IntegerField()                  # position in the queue outside
    position=models.IntegerField()                        # position among active players
    wait_rounds=models.FloatField()                     # number of expected rounds until entering 
    is_reading_instructions=models.BooleanField()        # still reading instructions while buffering
    will_read_instructions=models.BooleanField()         # will real instructions soon (use it to skip wait pages)
    
    Q1 = models.IntegerField()                          # for the instructions quiz
    Q2 = models.IntegerField()
    Q3 = models.IntegerField()
    Q4 = models.IntegerField()
    Q5 = models.IntegerField()
    Q6 = models.IntegerField()
    Q7 = models.IntegerField()
    Q8 = models.IntegerField()
    Q9 = models.IntegerField()
    Q10 = models.IntegerField()
    
 

# FUNCTIONS

def new_round(subsession: Subsession):
    players = subsession.get_players()
    for p in players:
        if p.is_playing:
            p.in_round(p.round_number+1).position = p.position
            
        p.in_round(p.round_number+1).is_playing = p.is_playing         
        p.in_round(p.round_number+1).is_out = p.is_out
        p.in_round(p.round_number+1).is_buffering = p.is_buffering
        
        if not p.is_playing and not p.is_out:
            p.in_round(p.round_number+1).queue_position = p.queue_position-1 
        
        if p.round_number==1:
            for i in range(p.subsession.round_number+1, p.subsession.session.config['num_supergames']+1):
                p.in_round(i).is_reading_instructions = False
                p.in_round(i).will_read_instructions = False

           
     #   if p.is_reading_instructions is False:
     #       p.in_round(p.round_number+1).is_reading_instructions = p.is_reading_instructions    
     #   if p.will_read_instructions is False:
     #       p.in_round(p.round_number+1).will_read_instructions = p.will_read_instructions


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
            expelled_id.in_round(i).position = None
            
        subsession.session.vars['aux_expelled_id']=expelled_id.position

    # for the pressure treatment
    else:
        players_aux = [x for x in subsession.get_players() if x.is_playing is True]
        expelled_id = sorted(players_aux, key=lambda player: player.last_payoff)[0]
        print('player leaving is', expelled_id.id_in_subsession)
        for i in range(subsession.round_number+1, subsession.session.config['num_supergames']+1):
            expelled_id.in_round(i).is_out = True
            expelled_id.in_round(i).is_playing = False
            expelled_id.in_round(i).is_buffering = False
            expelled_id.in_round(i).position = None
            
        subsession.session.vars['aux_expelled_id']=expelled_id.position
    
    subsession.session.vars['number_of_expelled'] = subsession.session.vars['number_of_expelled']+1
    print('counting expelled players=',subsession.session.vars['number_of_expelled'])
            
def player_enters_buffer(subsession: Subsession): 
# selects the entering participant  to buffer  
    players = subsession.get_players()
    for p in players:
        if not p.is_playing  and not p.is_out and not p.is_buffering  and p.queue_position==subsession.session.config['buffer_size']+1:  
            new_entrant_buffer=p
            
            r=0
            for i in range(subsession.round_number+1, subsession.round_number+subsession.session.config['buffer_size']+1):
                new_entrant_buffer.in_round(i).is_buffering = True
                new_entrant_buffer.in_round(i).is_playing = False
                new_entrant_buffer.in_round(i).is_out = False
                new_entrant_buffer.in_round(i).will_read_instructions = True
                new_entrant_buffer.in_round(i).queue_position = subsession.session.config['buffer_size']-r
                r=r+1
            for k in range(subsession.round_number+1, subsession.round_number+subsession.session.config['buffer_size']):
                new_entrant_buffer.in_round(k).is_reading_instructions=False
            
            new_entrant_buffer.in_round(subsession.round_number+subsession.session.config['buffer_size']).is_reading_instructions=True

            new_entrant_buffer.participant.vars['own_number_of_expelled']=subsession.session.vars['number_of_expelled']
            print('new entrant to buffer  is =',new_entrant_buffer.id_in_subsession)
            break 

def player_enters(subsession: Subsession): 
# selects the entering participant   from buffer to game
    players = subsession.get_players()
    for p in players:
        if not p.is_playing  and not p.is_out and p.is_buffering  and p.queue_position==1:   
            new_entrant=p 
            print('new entrant is =',new_entrant.id_in_subsession)
            new_entrant.in_round(subsession.round_number+1).is_playing = True
            new_entrant.in_round(subsession.round_number + 1).is_out = False
            new_entrant.in_round(subsession.round_number + 1).is_buffering = False
            new_entrant.in_round(subsession.round_number + 1).is_reading_instructions = False
            new_entrant.in_round(subsession.round_number + 1).will_read_instructions = False
    
            # new entrant takes the position of whoever i leaving
            new_entrant.in_round(subsession.round_number + 1).position = subsession.session.vars['aux_expelled_id']
            break
       

def queue_and_time(player:Player):
    supergames = player.session.config['supergames']
   # max_queue=player.session.config['num_demo_participants']-player.session.config['num_active_participants']-player.subsession.session.vars['number_of_expelled']   
   # for j in range(max_queue+1):
    #if not player.is_out and not player.is_playing and player.queue_position==j and j<=player.session.config['buffer_size']:
    
    if not player.is_out and not player.is_playing  and player.queue_position<=player.session.config['buffer_size']:    
            player.wait_rounds=sum(supergames[i] for i in range(player.subsession.session.vars['number_of_expelled'] , min(player.subsession.session.vars['number_of_expelled'] +player.queue_position,10),1))
    if not player.is_out and not player.is_playing and player.queue_position>player.session.config['buffer_size']:
        player.wait_rounds=sum(supergames[i] for i in range(player.subsession.session.vars['number_of_expelled'],min(player.subsession.session.vars['number_of_expelled']+player.queue_position-player.session.config['buffer_size'],10),1))



# PAGES ---------------------------------------------------------------

class WaitToStart(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out and not player.is_reading_instructions and not player.will_read_instructions
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
           return player.round_number <= player.session.config['num_supergames'] and not player.is_out and player.is_reading_instructions    

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            pressure=player.session.config['pressure'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            
        )

    

class Instructions3(Page):
    @staticmethod
    def is_displayed(player: Player):
      return player.round_number <= player.session.config['num_supergames'] and not player.is_out and player.is_reading_instructions      
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            
            endowment=player.session.config['endowment'],
            r=player.session.config['r'],
            V=player.session.config['V'],
            num_others=player.session.config['num_active_participants']-1,
            slider_max=player.session.config['V'],
            slider_min=0,
            theta_hat_prize=1,
            tlimit=player.session.config['tlimit'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,
            pressure=player.session.config['pressure']
        )


class Quiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out and player.is_reading_instructions    
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            pressure=player.session.config['pressure'],
          #  proportional=player.session.config['proportional'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,
            )

    


class Quiz_II(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out and player.is_reading_instructions   
    form_model = 'player'
    form_fields = ['Q7', 'Q8', 'Q9', 'Q10']
    
    @staticmethod
    
    def js_vars(player: Player):
        return dict(id_in_group=player.id_in_group)
    
    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            
            endowment=player.session.config['endowment'],
            r=player.session.config['r'],
            V=player.session.config['V'],
            num_others=player.session.config['num_active_participants']-1,
            slider_max=player.session.config['V'],
            slider_min=0,
            slider_default_prediction=0,
            slider_default_investment=0,
            signal=5,
            theta_hat_prize=1,
            tlimit=player.session.config['tlimit'],
            pressure=player.session.config['pressure'],
         #   proportional=player.session.config['proportional'],
            continuation_prob=round(1-player.session.config['stop_prob'],2)*100,
            stop_prob=player.session.config['stop_prob']*100,

        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        
        if player.round_number>1:
            player.is_playing  = False
            player.in_round(player.round_number+1).is_playing = False
        
            player.is_buffering  = True
            player.in_round(player.round_number+1).is_buffering = True
        
        player.is_out=False
        player.in_round(player.round_number+1).is_out=False
        player.in_round(player.round_number+2).is_out=False
        
        
        for i in range(player.subsession.round_number, player.subsession.session.config['num_supergames']+1):
            player.in_round(i).is_reading_instructions = False
            player.in_round(i).will_read_instructions = False


class PayingIntro(WaitPage):
    template_name = 'tullock_supergames_indefinite/PayingIntro.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
        )
    wait_for_all_groups = True
   
    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        pass


class  WaitToPlay(WaitPage): 
    def is_displayed(player: Player):
        return  player.round_number>1 and  player.round_number <= player.session.config['num_supergames'] and not player.is_out and player.in_round(player.round_number-1).will_read_instructions and not player.will_read_instructions
    
    template_name = 'tullock_supergames_indefinite/WaitToPlay.html'  
    wait_for_all_groups = True 
   # title_text = "Waiting to enter "
   # body_text = "Please wait you'll join soon"
        
    def vars_for_template(player: Player):
        player.queue_position=player.session.config['buffer_size']-(player.session.vars['number_of_expelled']-player.participant.vars['own_number_of_expelled'])
        #player.queue_position=1
        queue_and_time(player)
        if not player.is_playing:
            tlimit=round(player.session.config['tlimit']*player.wait_rounds,0)
            queue_position=player.queue_position-int(player.session.config['buffer_size']),
            buffer_queue_position=player.queue_position
        else:
            tlimit=0
            queue_position=0
            buffer_queue_position=0
                
        return dict(
            tlimit=tlimit,
            queue_position=queue_position,
            buffer_queue_position=buffer_queue_position
            )

    
    @staticmethod
    def after_all_players_arrive(subsession : Subsession):
        pass


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
            num_demo=player.session.config['num_demo_participants'],       
            num_active_participants=player.session.config['num_active_participants'],
            tlimit=player.session.config['tlimit'],
        )
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.last_bid=0
            player.last_prediction=0
            player.last_payoff=0
            
class Ready(Page):
    form_model = 'player'
    form_fields = ['queue_position']
    timeout_seconds = 30
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out and not player.is_playing  and player.queue_position==player.session.config['buffer_size']+1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            pressure=player.session.config['pressure'],
            ready_position=player.session.config['buffer_size']+1 
        )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print('timeout happend at Ready page')
            for p in player.get_others_in_subsession():   
                if not p.is_out and not p.is_playing and p.queue_position==player.session.config['buffer_size']+2:
                    p.queue_position=p.session.config['buffer_size']+1
                    p.in_round(p.round_number+1).queue_position=p.session.config['buffer_size']
                    lose_position=True
                    print('participant lost position:', lose_position)
                    break
                else:
                    lose_position=False
                    print('participant lost position:', lose_position)
                
            if lose_position is True:
                player.queue_position=player.session.config['buffer_size']+2
                player.in_round(player.round_number+1).queue_position=player.session.config['buffer_size']+1
            else:
                player.queue_position=player.session.config['buffer_size']+1
                player.in_round(player.round_number+1).queue_position=player.session.config['buffer_size']
 
        else:
            print('timeout DID NOT happend at Ready page')
            player.in_round(player.round_number+1).queue_position=player.session.config['buffer_size']
            

class EnterPage(WaitPage):   # Show  message for those waiting outside
    template_name = 'tullock_supergames_indefinite/EnterPage.html'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] \
                and not player.is_out and not player.is_playing and not player.is_buffering
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                )


class  WaitForResults(WaitPage): 
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and not player.is_out and not player.is_reading_instructions and not player.will_read_instructions
    
    template_name = 'tullock_supergames_indefinite/WaitToEnter.html'  
    wait_for_all_groups = True 
   # title_text = "Waiting to enter "
   # body_text = "Please wait you'll join soon"
        
    def vars_for_template(player: Player):
        queue_and_time(player)
        if not player.is_playing:
            tlimit=round(player.session.config['tlimit']*player.wait_rounds,0)
            queue_position=player.queue_position-player.session.config['buffer_size'],
            buffer_queue_position=player.queue_position
        else:
            tlimit=0
            queue_position=(0,0)
            buffer_queue_position=0
            
                
        return dict(
            tlimit=tlimit,
            queue_position=queue_position[0],
            buffer_queue_position=buffer_queue_position,
            )
    
    @staticmethod
    def after_all_players_arrive(subsession : Subsession):
        print('aaaaaaaaaaaaa')
        for p in subsession.get_players():
            if p.is_playing:
                p.payoff=p.last_payoff/p.session.config['us_exchange_rate']
        player_leaves(subsession)
        player_enters_buffer(subsession)
        player_enters(subsession)

        

class Results(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and player.is_playing is True

    @staticmethod
    def vars_for_template(player: Player):
        others_investment= list(p.last_bid for p in player.get_others_in_subsession() if p.is_playing)
        others_payoff=list(p.last_payoff for p in player.get_others_in_subsession() if p.is_playing)
        average_investment=sum(p.last_bid for p in player.subsession.get_players() if p.is_playing)/player.session.config['num_active_participants']
        average_payoff=sum(p.last_payoff for p in player.subsession.get_players() if p.is_playing)/player.session.config['num_active_participants']
        
        
        
        if player.session.config['num_active_participants'] == 4:
            others3_payoff=others_payoff[2],
            others3_investment=others_investment[2],

        else:
            others3_payoff=(0,),
            others3_investment=(0,),
            
        return dict(
            
            is_playing_next_round=player.in_round(player.round_number+1).is_playing,
            is_leaving=player.in_round(player.round_number+1).is_out,
            is_gonna_buffer=player.in_round(player.round_number+1).is_buffering,
            
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_supergames'],
            pressure=player.session.config['pressure'],
            others1_investment=others_investment[0],
            others1_payoff=others_payoff[0],
            others2_investment=others_investment[1],
            others2_payoff=others_payoff[1],
            others3_payoff=others3_payoff[0],
            others3_investment=others3_investment[0],
            num_active_participants= player.session.config['num_active_participants'],
            average_investment=average_investment,
            average_payoff=average_payoff,            
        )

class NewSequence(WaitPage):
    template_name = 'tullock_supergames_indefinite/NewSequence.html'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_supergames'] and \
                  not player.is_out  and not player.will_read_instructions

    @staticmethod
    def vars_for_template(player: Player):
        return dict(pressure=player.session.config['pressure'],
              #  participated_previous_round=player.in_round(player.round_number-1).is_playing,
                is_playing_next_round=player.in_round(player.round_number+1).is_playing,
                is_leaving=player.in_round(player.round_number+1).is_out,
                is_gonna_buffer=player.in_round(player.round_number+1).is_buffering
                )
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        pass


#class WaitBeforeNextRound(WaitPage):
 #   template_name = 'tullock_supergames_indefinite/WaitToEnter.html'
 #   @staticmethod
 #   def is_displayed(player: Player):
 #       return player.round_number <= player.session.config['num_supergames'] and not player.is_playing and not player.is_out
#
#    wait_for_all_groups = True
#    title_text = "Waiting to enter "
#    body_text = "Please wait you'll join soon"
  




page_sequence = [WaitToStart, 
                 Instructions1, 
                 Instructions2,  
                 Instructions3,  
                 Quiz,
                 Quiz_II,
                 PayingIntro,
                 Ready,
                 EnterPage,
                 WaitToPlay,
                 Play, 
                 WaitForResults, 
                 Results, 
                 NewSequence,
                ]
