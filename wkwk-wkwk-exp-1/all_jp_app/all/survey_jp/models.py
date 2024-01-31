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

    age = models.IntegerField(label='あなたは何歳ですか?', min=13, max=125)

    gender = models.StringField(
        choices=[['受諾', '受諾'], ['女性', '女性']],
        label='あなたの性別は?',
        widget=widgets.RadioSelect,
    )
    
    
    crt_bat = models.IntegerField(
        label='''
        バットとボールが合計で22ドルです。
        バットはボールよりも20ドル高い。
        ボールはいくらか？'''
        )
        
    crt_widget = models.IntegerField(
        label='''
        5台のマシーンが5分で5個のウィジェットを作るとしたら、100台のマシーンで100個のウィジェットを作るのに何分必要か？
        '''
    )

    crt_lake = models.IntegerField(
        label='''
        ある湖に、スイレンが咲いています。
        毎日、スイレンは２倍のサイズに大きくなります。
        湖全体をスイレンが覆うのに48日かかるとしたら、湖の半分をスイレンが覆うのに何日かかるだろうか？
        '''
    )
