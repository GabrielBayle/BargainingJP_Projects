from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = '調査'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    question1 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(900,100)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question2 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(800,200)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question3 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(700,300)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question4 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(600,400)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
        
    question5 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(500,500)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    breakout = models.IntegerField(
        label='''
        あなたのブレークアウトルームの番号を教えてください'''
        )

    question6 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(900,100)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question7 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(800,200)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question8 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(700,300)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question9 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(600,400)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
    
    question10 = models.StringField(
        choices=[['受諾する', '受諾する'], ['拒否する', '拒否する']],
        label='(500,500)を提案されたときあなたはどうしますか？',
        widget=widgets.RadioSelect,
    )
