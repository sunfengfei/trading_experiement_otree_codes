# =============================
# d_trading_two_apps_2/__init__.py
# =============================
from otree.api import *
import math

class C(BaseConstants):
    NAME_IN_URL = 'trading_2'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    student_id = models.StringField()
    utility_type = models.StringField()
    alpha = models.FloatField()
    beta = models.FloatField()
    endowment_a = models.IntegerField()
    endowment_b = models.IntegerField()
    current_a = models.IntegerField()
    current_b = models.IntegerField()
    partner_id = models.StringField(blank=True)
    calculated_utility = models.FloatField(blank=True)

    def calculate_utility(self):
        if self.utility_type == 'CD':
            return round(math.pow(self.current_a, self.alpha) * math.pow(self.current_b, self.beta), 2)
        elif self.utility_type == 'LINEAR':
            return self.alpha * self.current_a + self.beta * self.current_b
        elif self.utility_type == 'MIN':
            return min(self.alpha * self.current_a, self.beta * self.current_b)
        else:
            return 0

def creating_session(subsession):
    for player in subsession.get_players():
        v = player.participant.vars
        player.student_id = v['student_id']
        player.utility_type = v['utility_type']
        player.alpha = v['alpha']
        player.beta = v['beta']
        player.endowment_a = v['endowment_a']
        player.endowment_b = v['endowment_b']
        player.current_a = v['current_a']
        player.current_b = v['current_b']
        player.partner_id = v.get('partner_id', '')
        player.calculated_utility = v.get('initial_utility', 0)

class Display(Page):
    def vars_for_template(player):
        return dict(
            student_id=player.student_id,
            utility_type=player.utility_type,
            alpha=player.alpha,
            beta=player.beta,
            a=player.current_a,
            b=player.current_b,
            utility=player.calculate_utility()
        )

page_sequence = [Display]
