# =============================
# d_trading_two_apps_1/__init__.py
# =============================
from otree.api import *
import csv
from pathlib import Path

class C(BaseConstants):
    NAME_IN_URL = 'trading_1'
    PLAYERS_PER_GROUP = None
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

# Read parameters from CSV and assign to players





def creating_session(subsession):
    csv_path = Path(__file__).resolve().parent.parent / "utility_parameters_50.csv"

    with csv_path.open(newline='') as f:
        reader = csv.DictReader(f)
        param_dict = {row['student_id']: row for row in reader}

    for player in subsession.get_players():
        student_id = str(player.id_in_group)
        row = param_dict[student_id]

        player.student_id = student_id
        player.utility_type = row['utility_type']
        player.alpha = float(row['alpha'])
        player.beta = float(row['beta'])
        player.endowment_a = int(row['endowment_a'])
        player.endowment_b = int(row['endowment_b'])
        player.current_a = player.endowment_a
        player.current_b = player.endowment_b

        player.participant.vars.update({
            'student_id': student_id,
            'utility_type': player.utility_type,
            'alpha': player.alpha,
            'beta': player.beta,
            'endowment_a': player.endowment_a,
            'endowment_b': player.endowment_b,
            'current_a': player.current_a,
            'current_b': player.current_b
        })

        print(f"[App1] Player {student_id} loaded from CSV: {player.utility_type}, α={player.alpha}, β={player.beta}, A={player.endowment_a}, B={player.endowment_b}")

class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return True

page_sequence = [Intro]
