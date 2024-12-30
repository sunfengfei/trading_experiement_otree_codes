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
    UTILITY_TYPES = ['CD', 'Linear', 'Min']
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
    # Utility function parameters
    utility_type = models.StringField()
    alpha = models.FloatField()
    beta = models.FloatField()
    
    # Endowments and current holdings
    endowment_a = models.IntegerField()
    endowment_b = models.IntegerField()
    current_a = models.IntegerField()
    current_b = models.IntegerField()
    
    # Trading fields
    partner_id = models.StringField(label="Enter your trading partner's Student ID")
    trade_a = models.IntegerField(blank=True)
    trade_b = models.IntegerField(blank=True)
    trade_complete = models.BooleanField(initial=False)
    
    # User inputs
    utility_answer = models.FloatField(
        label="Calculate your current utility based on your utility function and current holdings:"
    )
    
    def calculate_utility(self):
        if self.utility_type == 'CD':
            return round(math.pow(self.current_a, self.alpha) * math.pow(self.current_b, self.beta), 2)
        elif self.utility_type == 'Linear':
            return self.alpha * self.current_a + self.beta * self.current_b
        else:  # Min function
            return min(self.alpha * self.current_a, self.beta * self.current_b)
    
    def verify_utility_calculation(self, submitted_value):
        actual_utility = self.calculate_utility()
        print(f"Verifying: submitted={submitted_value}, actual={actual_utility}, diff={abs(actual_utility - submitted_value)}")
        return abs(actual_utility - submitted_value) <= C.UTILITY_THRESHOLD
    
    def get_partner(self):
        for p in self.subsession.get_players():
            if p.participant.vars.get('student_id') == self.partner_id and p != self:
                return p
        return None
    
    def execute_trade(self):
        partner = self.get_partner()
        if partner and partner.partner_id == self.participant.vars.get('student_id'):
            if self.trade_a == -partner.trade_a and self.trade_b == -partner.trade_b:
                # Execute trade
                self.current_a += self.trade_a
                self.current_b += self.trade_b
                partner.current_a += partner.trade_a
                partner.current_b += partner.trade_b
                # Update market price
                self.group.last_trade_a = abs(self.trade_a)
                self.group.last_trade_b = abs(self.trade_b)
                # Mark trade as complete
                self.trade_complete = True
                partner.trade_complete = True
                return True
        return False
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


# Pages

class ParameterDisplay(Page):
    form_model = 'player'
    form_fields = ['utility_answer']
    
    def error_message(self, values):
        if not self.verify_utility_calculation(values['utility_answer']):
            return 'Your calculation is incorrect. Please try again.'
            
    def vars_for_template(self):
        return {
            'current_utility': self.calculate_utility()
        }

class Trading(Page):
    form_model = 'player'
    form_fields = ['partner_id', 'trade_a', 'trade_b']
    
    def error_message(self, values):
        if not values['partner_id']:
            return 'Please enter your trading partner\'s ID'
            
        partner = self.player.get_partner()
        if not partner:
            return 'Trading partner not found'
            
        # Check if trade would result in negative holdings
        if self.player.current_a + values['trade_a'] < 0:
            return 'You cannot sell more Good A than you have'
        if self.player.current_b + values['trade_b'] < 0:
            return 'You cannot sell more Good B than you have'

class WaitForTrade(WaitPage):
    title_text = "Waiting for your trading partner"
    body_text = "Please wait for your trading partner to input their trade."
    
    def after_all_players_arrive(self):
        for p in self.subsession.get_players():
            if not p.trade_complete:
                p.execute_trade()

class ResultsPage(Page):
    timeout_seconds = 10
    
    def vars_for_template(self):
        return {
            'executed': self.player.trade_complete,
            'new_utility': self.player.calculate_utility()
        }

page_sequence = [ParameterDisplay, Trading, WaitForTrade, ResultsPage]