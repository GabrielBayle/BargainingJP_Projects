from otree.api import *
import time
import numpy
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
#   - DONE: check Final Results screen
#   - DONE: ADD treatment where you can't buy information in settings!  And check treatment where it is public info!! 
#   - DONE:  add instructions
#   - DONE: eliminate round number ! !
#   - DONE:  RANDOM TYPES ASSIGNED IN DIVIDEND ROUND AND PAYMENT ACCORDINGLY!!!!!!!!!!!!!!!!!!!!!
#   - DONE:  SCREENS FOR EACH NEW SEQUENCE AND DIVIDEND ROUND (MAYBE A POP-UP FOR THE DIVIDEND)
#   - DONE: tell participants if their old or young in their TRADING SCREEN.... plus tell them their type in ROUND  
#   - DONE: check average price 
#   - DONE: REMPLAZAR IMAGENES INSTRUCCIONES 
#    -DONE:    CHANGE INSTRUCTIONS AND DIAGRAM TO BE CONSISTENT WITH THE GAME: TYPES ARE ASSIGNED ONCE AT THE BEGINNING
#   -DONE: ADD instructions screen or add to existing screen DIVIDEND INFO explanation



# NOT SO IMPORTANT:


#   -DONE  show entering participants  past average_price (pluc click on graph)    ask
#   - make bus/sell notice bigggerrrrr   ?????????






class C(BaseConstants):
    NAME_IN_URL = 'double_auction_OLG_practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=False)

    if subsession.session.config['OLG'] is True:  # for OLG treatment
        players = subsession.get_players()
    
        for g in subsession.get_groups():
            g.world_state='unknown'   
            g.total_sold=0
            g.total_spent=0
        
        
        for p in players:
            p.is_informed = False
       
       
       
        

class Group(BaseGroup):
    # original fields
    start_timestamp = models.IntegerField()

    # my fields
    # signal = models.FloatField()  # information about dividends
    average_price = models.FloatField()  # average round price
    total_spent=models.CurrencyField()      # total spent in trading round
    total_sold=models.FloatField()         # total sold/bought in trading round
    world_state = models.StringField()   # random state of the world
    dividend = models.FloatField()       # round dividend
    title = models.StringField()         # titles for rounds


class Player(BasePlayer):
    # original fields
    is_buyer = models.BooleanField()    # if participant is buying or selling (used just for liveSend)
    current_offer = models.CurrencyField(blank=True)
    break_even_point = models.CurrencyField()   # won't need this
    num_items = models.IntegerField()   # assets during each round

    # my fields
    money = models.CurrencyField()
    # assets = models.FloatField()        # would be the same  as num_items
    round_payoff = models.FloatField()    # for recording payments to be added in sequence
    sequence_payoff = models.FloatField() # for recording sequence to be selected at random
    is_playing = models.BooleanField()    # this is whether they are trading or just waiting and predicting
    prediction = models.FloatField()      # predicted price
    is_informed = models.BooleanField()   # whether they see the divided (or a clue) or not
    is_young = models.BooleanField()      # whether they are  young or old
    has_played = models.BooleanField()    # whether someone has already played in the sequence 
    type = models.StringField()           # random type for dividend payment A,B or C
    dividend_clue=models.FloatField()     # clue given to player dividend 
    dividend_clue_text=models.StringField() #clue given to player state of the world 
    
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
        if player.session.config['OLG'] is True:   #check this for problems!!!!!!!!!!!!!!!!!!!!!!
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
            group.total_sold += 1
            group.total_spent += price
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



# assign types 
def assign_types(group: Group):
    players = group.get_players()
    for p in players:    
        if (p.id_in_group == 1) or (p.id_in_group == 4) or (p.id_in_group == 7) or (p.id_in_group == 10) or (p.id_in_group == 13) or (p.id_in_group == 16) or (p.id_in_group == 19):
            p.type  = "A"
        if (p.id_in_group == 2) or (p.id_in_group == 5) or (p.id_in_group == 8) or (p.id_in_group == 11) or (p.id_in_group == 14) or (p.id_in_group == 17) or (p.id_in_group == 20):
            p.type  = "B"
        if (p.id_in_group == 3) or (p.id_in_group == 6) or (p.id_in_group == 9) or (p.id_in_group == 12) or (p.id_in_group == 15) or (p.id_in_group == 18) or (p.id_in_group == 21): 
            p.type  = "C"

# keep types from previos rounds within sequence
def keep_types(group: Group):
    players = group.get_players()
    for p in players:    
        p.type = p.in_round(p.round_number-1).type
        

# determines round payoff
def round_payoff_olg(group: Group):
    players = group.get_players()
    for p in players:
        if p.is_playing is True:    # players  payoff
            # final rounds for both old and young 
            
            if (p.round_number == p.session.config['dividend_1_period_practice']) or (p.round_number == p.session.config['dividend_2_period_practice']) :                 
                if p.type == p.group.world_state:

                    p.round_payoff =  max(p.group.dividend*p.num_items + float(p.money), 0)
                else:
                    p.round_payoff = max(float(p.money), 0)
                
                
            # normal rounds
            else:                                                                            
                if p.is_young is True:                                                      # for young
                    p.round_payoff = 0        
                if p.is_young is False:                                                     # for old
                    p.round_payoff = max(float(p.money), 0)      
            print('items=',p.num_items,'dividend=', p.group.dividend, 'type=', p.type, 'world=', p.group.world_state , 'payoff=' ,p.round_payoff)
        
        else:                       # non-players prediction payoff
            p.round_payoff = max(p.session.config['prediction_endowment']-p.session.config['scale_prediction'] * \
                             abs(p.prediction - p.group.average_price), 0)
           
            print('average_price=', p.group.average_price, 'prediction=', p.prediction ,'payoff=', p.round_payoff)
                    

def sequence_payoff_olg(group: Group):
    players = group.get_players()
    for p in players:
            if p.round_number == p.session.config['dividend_1_period_practice'] \
            or p.round_number == p.session.config['dividend_2_period_practice']:
                
                if p.session.config['info_acquisition'] is True:
                    if p.is_informed is True:
                        p.sequence_payoff=p.round_payoff+p.in_round(p.round_number-1).round_payoff+p.in_round(p.round_number-2).round_payoff+p.session.config['info_endowment']-p.session.config['info_cost']
                    else:
                        p.sequence_payoff=p.round_payoff+p.in_round(p.round_number-1).round_payoff+p.in_round(p.round_number-2).round_payoff+p.session.config['info_endowment']
                else:
                     p.sequence_payoff=p.round_payoff+p.in_round(p.round_number-1).round_payoff+p.in_round(p.round_number-2).round_payoff
                print('CALCULATED SEQUENCE PAYMENT = ',  p.sequence_payoff )
               


# include this at the beginning of each round (except the first in each sequence)
def new_sequence(group: Group):
    players = group.get_players()
    for p in players:
        p.is_young= p.id_in_group > p.session.config['num_sellers']
        p.is_playing = p.id_in_group <= p.session.config['num_sellers']+p.session.config['num_buyers']
        if p.is_playing:
            if  p.is_young is True:
                p.is_buyer = True
                p.num_items = 0
                    # p.break_even_point = random.randint(C.VALUATION_MIN, C.VALUATION_MAX)
                p.break_even_point = 0
                p.current_offer = 0
                p.money = p.session.config['money']
                p.has_played = True

            else:
                p.is_young=False
                p.is_buyer = False
                p.num_items = p.session.config['assets_per_seller']
                    # p.break_even_point = random.randint(
                    #  C.PRODUCTION_COSTS_MIN, C.PRODUCTION_COSTS_MAX
                    # )
                p.break_even_point = 0
                    # p.current_offer = C.VALUATION_MAX + 1
                p.current_offer = 999  # try with NA later
                p.money = 0
                p.has_played = True
                    
        else:
            p.num_items = 0
            p.break_even_point = 0
            p.current_offer = 0
            p.money = 0
            p.has_played=False
            p.is_buyer = True
            p.is_young= True
            p.is_playing = False






def round_change_olg(group: Group):
    players = group.get_players()

    total_unsold = sum(player.in_round(player.round_number - 1).num_items for player in players if
                       player.in_round(player.round_number - 1).is_young is False)

    print('unsold items in previous round = ', total_unsold)

    # Transforms buyers (aka young) into  sellers (aka old), and sellers (old) into non-playing.
    count = 1
    for p in players:
        # among those who played the last round
        if p.in_round(p.round_number - 1).is_playing is True:

            # old to non-players
            if p.in_round(p.round_number - 1).is_young is False:
                p.is_playing = False
                p.is_young = True
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.money = 0
                p.is_informed = p.in_round(p.round_number - 1).is_informed
                p.has_played = True
                p.is_buyer = True
                

            # young to old
            else:
                p.is_young = False
                p.is_buyer = False
                p.is_playing = True
                p.num_items = p.in_round(p.round_number - 1).num_items
                p.break_even_point = 0
                p.current_offer = 999
                p.money = p.in_round(p.round_number - 1).money
                p.is_informed = p.in_round(p.round_number - 1).is_informed
                p.has_played = True

         
        # among those who did not play last round
        else:
            # non-player who has never played to buyer
            if p.in_round(p.round_number - 1).has_played is False:
                if (count <= p.session.config['num_buyers']):
                    p.is_playing = True
                    p.is_buyer = True
                    p.is_young = True
                    p.num_items = 0
                    p.break_even_point = 0
                    p.current_offer = 0
                    p.money = p.session.config['money']
                    p.is_informed = p.in_round(p.round_number - 1).is_informed
                    print('total new buyers count', count)
                    p.has_played =  True
                    count+=1
                
            # non-player who stays out because he is not selected due to enough participants already selected 
                else:
                    p.is_playing = False
                    p.num_items = 0
                    p.break_even_point = 0
                    p.current_offer = 0
                    p.is_young = True
                    p.money = 0
                    p.is_informed = p.in_round(p.round_number - 1).is_informed
                    p.has_played = False
                    p.is_buyer = True
            
             # non-player who stays out because he is not selected because he already has played           
            else:
                p.is_playing = False
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.is_young = True
                p.money = 0
                p.is_informed = p.in_round(p.round_number - 1).is_informed
                p.has_played = True
                p.is_buyer = True
            
            
            # non-player to be recycled   
            # (this can only happen in the third round )
    for p in players:        
            # non-player in the last round who has played before but did not play the last round              
        if count <= p.session.config['num_buyers']:
            if p.in_round(p.round_number-1).is_playing is False and p.is_playing is False :
                p.is_playing = True
                p.is_buyer = True
                p.is_young = True
                p.num_items = 0
                p.break_even_point = 0
                p.current_offer = 0
                p.money = p.session.config['money']
                p.is_informed = p.in_round(p.round_number - 1).is_informed
                print('recycled buyers count', count)
                p.has_played =  True
                count+=1      
            

        
    # assigns unsold units to those buyers that will become sellers
    # (this assigns in order but order changes every round)
    counter = 1
    while counter <= total_unsold:
        for p in players:
            if counter <= total_unsold:
                if p.is_playing is True and p.is_young is True:
                    print('assigning unsold assets count', counter)
                    counter += 1
                    p.num_items += 1


def dividends_titles_and_clues(group: Group):
    players = group.get_players()    
    for player in players:
    
    # clues for even and odd participants 
        if player.participant.id_in_session % 2 == 0:   # receive clue number one
            if player.round_number <= player.session.config['dividend_2_period_practice']:
                player.dividend_clue = player.session.config['dividend_2_alt1_practice']
                player.dividend_clue_text=player.session.config['dividend_2_alt1_text_practice']  
            if player.round_number <= player.session.config['dividend_1_period_practice']:
                player.dividend_clue = player.session.config['dividend_1_alt1_practice'] 
                player.dividend_clue_text=player.session.config['dividend_1_alt1_text_practice']  
        else:                                            # receive clue number two                      
            if player.round_number <= player.session.config['dividend_2_period_practice']:
                player.dividend_clue = player.session.config['dividend_2_alt2_practice']
                player.dividend_clue_text = player.session.config['dividend_2_alt2_text_practice']                
            if player.round_number <= player.session.config['dividend_1_period_practice']:
                player.dividend_clue = player.session.config['dividend_1_alt2_practice']                 
                player.dividend_clue_text = player.session.config['dividend_1_alt2_text_practice'] 
    
    # dividend per sequence     
  
        if player.round_number <= player.session.config['dividend_2_period_practice']:
            player.group.dividend = player.session.config['dividend_2_practice']
            player.group.world_state = player.session.config['state_2_practice']
        if player.round_number <= player.session.config['dividend_1_period_practice']:
            player.group.dividend = player.session.config['dividend_1_practice'] 
            player.group.world_state = player.session.config['state_1_practice']

    # titles for rounds in sequences     
    if (group.round_number == group.session.config['dividend_1_period_practice']) or (group.round_number ==group.session.config['dividend_2_period_practice']):
        group.title = 'Third and Period Round of the Sequence'
    elif (group.round_number == group.session.config['dividend_1_period_practice']-1) or (group.round_number == group.session.config['dividend_2_period_practice']-1):
        group.title = 'Second Period of the Sequence'
    elif (group.round_number == group.session.config['dividend_1_period_practice']-2) or (group.round_number == group.session.config['dividend_2_period_practice']-2):
        group.title = 'First Period of the Sequence'


def average_price(group: Group):
    players = group.get_players()

   # total_sold = sum(player.num_items for player in players if (player.is_buyer is True and player.is_playing))
   # total_paid = sum(player.money for player in players if (player.is_buyer is False and player.is_playing))

    print('sold items in current round = ', group.total_sold)
    print('total payments  in current round = ', group.total_spent)

    if group.total_sold > 0:
        group.average_price = float(group.total_spent/group.total_sold)
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
            num_sequences=int(C.NUM_ROUNDS/3),
            num_practice_sequences=player.session.config['practice_num_rounds'],
            endowment=player.session.config['money'],
            us_exchange_rate=player.session.config['us_exchange_rate'],
            show_up_fee=float(player.session.config['participation_fee']),
            others=player.session.num_participants-1,
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
            endowment=player.session.config['money'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],
            money=player.session.config['money'],
            shares=player.session.config['assets_per_seller'],
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'] ,
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
            money=player.session.config['money'],
            shares=player.session.config['assets_per_seller'],
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'] ,
            info_cost=player.session.config['info_cost'],
            info_endowment=player.session.config['info_endowment'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],

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
            money=player.session.config['money'],
            shares=player.session.config['assets_per_seller'],
            prediction_endowment=player.session.config['prediction_endowment'],
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'] ,
            info_cost=player.session.config['info_cost'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],            
        )
class Instructions5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
            money=player.session.config['money'],
            shares=player.session.config['assets_per_seller'],
            prediction_endowment=player.session.config['prediction_endowment'],
            
        )



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
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
             prediction_endowment=player.session.config['prediction_endowment'],
        )




class PracticeIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            practice_num_rounds=player.session.config['practice_num_rounds'],
             prediction_endowment=player.session.config['prediction_endowment'],
        )




class PayingIntro(Page):
    timeout_seconds = 20
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_rounds=player.session.config['num_rounds'],
            OLG=player.session.config['OLG'],
            num_sequences=int(player.session.config['num_rounds']/3)
            
        )


class WaitToStart(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        print('ROUND NUMBER --->', group.round_number)
        if (group.round_number == 1) or group.round_number == (group.session.config['dividend_1_period_practice']+1) or group.round_number == (group.session.config['dividend_2_period_practice']+1):
            new_sequence(group)
            assign_types(group)
        else:
            round_change_olg(group)
            keep_types(group)   
        
        dividends_titles_and_clues(group)
        

        group.start_timestamp = int(time.time())


class TradingOLG_practice(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_playing is True and player.round_number <= player.session.config['num_rounds'] 

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
        if player.is_young is True:
            cohort = 'Young'
        else:
            cohort = 'Old'
        return dict(
            num_rounds=player.session.config['num_rounds'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],
            info_cost=player.session.config['info_cost'],
            cohort=cohort,
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'] ,
            player_in_previous_rounds=reversed(player.in_previous_rounds()),)


class Prediction_practice(Page):
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
            player_in_previous_rounds=reversed(player.in_previous_rounds()),
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],)

class ResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.session.config['OLG'] is True:
            average_price(group)
            round_payoff_olg(group)
            if (group.round_number == group.session.config['dividend_1_period_practice'] or
                group.round_number == group.session.config['dividend_2_period_practice']):
                    sequence_payoff_olg(group)


class ResultsOlg_practice(Page):
    timeout_seconds = 30
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.session.config['num_rounds'] 
    @staticmethod
    def vars_for_template(player: Player): 

        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            dividend_payment=player.num_items*player.group.dividend,
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],)


class SequenceResults_practice(Page):
  #  timeout_seconds = 30
    @staticmethod
    def is_displayed(player: Player):
        return  (player.round_number == player.session.config['dividend_1_period_practice'] or
                player.round_number == player.session.config['dividend_2_period_practice'])


    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player_in_all_rounds=reversed(player.in_all_rounds()),
            num_rounds=player.session.config['num_rounds'],
            dividend_payment=player.num_items*player.group.dividend,
            info_acquisition=player.session.config['info_acquisition'],
            public_information=player.session.config['public_information'],
            dividend_range_1=player.session.config['dividend_range'][0],
            dividend_range_2=player.session.config['dividend_range'][1],
            dividend_range_3=player.session.config['dividend_range'][2],
            dividend_range_1_text=player.session.config['dividend_range_text'][0],
            dividend_range_2_text=player.session.config['dividend_range_text'][1],
            dividend_range_3_text=player.session.config['dividend_range_text'][2],
            info_cost=player.session.config['info_cost'])


class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.session.config['num_rounds']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            payoff_plus_participation_fee=player.participant.payoff_plus_participation_fee(),
            total_earnings=player.participant.vars['aux_payoff'],
            show_up_fee=float(player.session.config['participation_fee']),
            total_earnings_US=float(player.participant.payoff),
            total_payoff_US=float(player.participant.payoff_plus_participation_fee()),
            paying_round=int(player.participant.vars['paying_round'][0]),
            paying_sequence=int(player.participant.vars['paying_round'][0]/3),
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
                 #PayingIntro,
                 WaitToStart,
                 TradingOLG_practice,
                 Prediction_practice,
                 ResultsWaitPage,
                 ResultsOlg_practice,
                 SequenceResults_practice,
               #  FinalResults
                ]
