from otree.api import *
import random
import math

doc = """
Trading experiment with different utility functions and endowments.
Players need to calculate initial utility and can trade goods with others.
"""

class C(BaseConstants):
    NAME_IN_URL = 'trading'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    TOTAL_ENDOWMENT = 10
    UTILITY_TYPES = ['CD', 'LINEAR', 'MIN']
    ALPHA_RANGE = (0.2, 0.8)
    BETA_RANGE = (0.2, 0.8)
    UTILITY_THRESHOLD = 0.02

def creating_session(subsession):
    for player in subsession.get_players():
        # Assign utility function type
        player.utility_type = random.choice(C.UTILITY_TYPES)
        print('Set utility type to', player.utility_type)
        
        # Assign parameters
        player.alpha = round(random.uniform(0.2, 0.8), 2)
        player.beta = round(random.uniform(0.2, 0.8), 2)
        print(f'Set alpha={player.alpha}, beta={player.beta}')
        
        # Assign endowments
        player.endowment_a = random.randint(0, C.TOTAL_ENDOWMENT)
        player.endowment_b = C.TOTAL_ENDOWMENT - player.endowment_a
        print(f'Set endowments: A={player.endowment_a}, B={player.endowment_b}')
        
        # Set current holdings
        player.current_a = player.endowment_a
        player.current_b = player.endowment_b

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    last_trade_a = models.IntegerField(initial=0)
    last_trade_b = models.IntegerField(initial=0)
    
    def get_market_price(self):
        if self.last_trade_b == 0:
            return None
        return self.last_trade_a / self.last_trade_b
    

class Player(BasePlayer):
    student_id=models.StringField(
        label="Please input your student ID",
    )
    # Utility function parameters
    utility_type = models.StringField()
    alpha = models.FloatField()
    beta = models.FloatField()
    
    # Endowments and current holdings
    endowment_a = models.IntegerField()
    endowment_b = models.IntegerField()
    current_a = models.IntegerField()
    current_b = models.IntegerField()
    
    # User inputs
    calculated_utility = models.FloatField()
    trading_with_id = models.StringField(
        label="Enter the student ID of your trading partner",
        blank=True  # 允许为空很重要
    )
    trade_a = models.IntegerField()
    trade_b = models.IntegerField()
    
    def calculate_utility(self):
        if self.utility_type == 'CD':
            return round(math.pow(self.current_a, self.alpha) * math.pow(self.current_b, self.beta), 2)
        elif self.utility_type == 'LINEAR':
            return self.alpha * self.current_a + self.beta * self.current_b
        elif self.utility_type == 'MIN':  # Explicit check for MIN
            return min(self.alpha * self.current_a, self.beta * self.current_b)
        else:
            raise ValueError(f"Unknown utility type: {self.utility_type}")
    
    def verify_utility_calculation(self, submitted_value):
        actual_utility = self.calculate_utility()
        print(f"Verifying: submitted={submitted_value}, actual={actual_utility}, diff={abs(actual_utility - submitted_value)}")
        return abs(actual_utility - submitted_value) <= C.UTILITY_THRESHOLD

# Pages
class Intro(Page):
    form_model="player"
    form_fields=["student_id"]

    def before_next_page(self, timeout_happened):
        # Store student_id in participant.vars for use in other apps
        self.participant.vars['student_id'] = self.student_id

class ParameterDisplay(Page):
    form_model = 'player'
    form_fields = ['calculated_utility']
    
    def error_message(self, values):
        if not self.verify_utility_calculation(values['calculated_utility']):
            return 'Your calculation is incorrect. Please try again.'

class Trading(Page):
    form_model = 'player'
    form_fields = ['trade_a', 'trade_b']
    
    
    def error_message(self, values):
        # Check if trade would result in negative holdings
        if self.current_a + values['trade_a'] < 0:
            return 'You cannot sell more Good A than you have'
        if self.current_b + values['trade_b'] < 0:
            return 'You cannot sell more Good B than you have'
        
        # # Check if trade would exceed total capacity
        # if self.current_a + values['trade_a'] > C.TOTAL_ENDOWMENT:
        #     return 'You cannot hold more than 10 units of Good A'
        # if self.current_b + values['trade_b'] > C.TOTAL_ENDOWMENT:
        #     return 'You cannot hold more than 10 units of Good B'
    
    def before_next_page(self, timeout_happened=False):
        self.current_a += self.trade_a
        self.current_b += self.trade_b
        self.group.last_trade_a = self.trade_a
        self.group.last_trade_b = self.trade_b

class Results(Page):
    def vars_for_template(self):
        return {
            'final_a': self.current_a,
            'final_b': self.current_b,
            'final_utility': self.calculate_utility()
        }
    
page_sequence = [Intro, ParameterDisplay, Trading,Results]
