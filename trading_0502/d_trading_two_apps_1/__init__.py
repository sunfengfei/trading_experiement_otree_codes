from otree.api import *
import random
import math
import csv
import os

doc = """
Trading experiment with different utility functions and endowments.
1. Players need to calculate initial utility
"""

class C(BaseConstants):
    NAME_IN_URL = 'trading_1'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    
    TOTAL_ENDOWMENT = 10
    UTILITY_TYPES = ['CD', 'LINEAR', 'MIN']
    ALPHA_RANGE = (0.2, 0.8)
    BETA_RANGE = (0.2, 0.8)
    UTILITY_THRESHOLD = 0.02
    
    # CSV file location - assuming it's in _static/global
    CSV_PATH = "_static/global/player_parameters.csv"


def get_player_parameters(student_id):
    """Load player parameters from CSV file based on student ID"""
    csv_path = os.path.join('_static', 'global', 'player_parameters.csv')
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['student_id'] == student_id:
                    return {
                        'utility_type': row['utility_type'],
                        'alpha': float(row['alpha']),
                        'beta': float(row['beta']),
                        'endowment_a': int(row['endowment_a']),
                        'endowment_b': int(row['endowment_b'])
                    }
    except Exception as e:
        print(f"Error loading parameters from CSV: {e}")
    
    # If student ID not found or error occurs, return None
    return None


def creating_session(subsession):
    for player in subsession.get_players():
        # Parameters will be assigned after student_id is input
        pass


class Subsession(BaseSubsession):
    last_trade_a = models.IntegerField(initial=0)
    last_trade_b = models.IntegerField(initial=0)

    def get_market_price(self):
        if self.last_trade_b == 0:
            return None
        return self.last_trade_a / self.last_trade_b
     
     
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    student_id = models.StringField(
        label="Please input your student ID",
    )

    partner_id = models.StringField(
        label="Trading partner's student ID",
        blank=True
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
    form_model = "player"
    form_fields = ["student_id"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Load parameters from CSV based on student_id
        params = get_player_parameters(player.student_id)
        
        if params:
            # Assign parameters from CSV file
            player.utility_type = params['utility_type']
            player.alpha = params['alpha']
            player.beta = params['beta']
            player.endowment_a = params['endowment_a']
            player.endowment_b = params['endowment_b']
            
            # Output for debugging
            print(f"Loaded parameters for student {player.student_id}:")
            print(f"Utility type: {player.utility_type}")
            print(f"Alpha: {player.alpha}, Beta: {player.beta}")
            print(f"Endowments: A={player.endowment_a}, B={player.endowment_b}")
        else:
            # If not found in CSV, generate random parameters
            print(f"Student ID {player.student_id} not found in CSV. Using random parameters.")
            player.utility_type = random.choice(C.UTILITY_TYPES)
            player.alpha = round(random.uniform(0.2, 0.8), 2)
            player.beta = round(random.uniform(0.2, 0.8), 2)
            player.endowment_a = random.randint(0, C.TOTAL_ENDOWMENT)
            player.endowment_b = C.TOTAL_ENDOWMENT - player.endowment_a
        
        # Set current holdings
        player.current_a = player.endowment_a
        player.current_b = player.endowment_b
        
        # Store parameters in participant for app 2
        participant = player.participant
        participant.student_id = player.student_id
        participant.utility_type = player.utility_type
        participant.alpha = player.alpha
        participant.beta = player.beta
        participant.endowment_a = player.endowment_a
        participant.endowment_b = player.endowment_b
        participant.current_a = player.current_a
        participant.current_b = player.current_b


class ParameterDisplay(Page):
    form_model = 'player'
    form_fields = ['calculated_utility']
    
    def error_message(self, values):
        if not self.player.verify_utility_calculation(values['calculated_utility']):
            return 'Your calculation is incorrect. Please try again.'
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        actual_utility = player.calculate_utility()
        # Store the initial utility in participant vars
        player.participant.initial_utility = actual_utility


class Calculator(Page):
    form_model = 'player'
    form_fields = ['partner_id']

    def error_message(self, values):
        if values['partner_id'] == self.player.student_id:
            return 'You cannot trade with yourself'
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Store partner ID in participant vars
        player.participant.partner_id = player.partner_id


page_sequence = [
    Intro,
    # ParameterDisplay,
    Calculator,
]