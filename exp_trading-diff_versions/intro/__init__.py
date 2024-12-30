from otree.api import *


doc = """
1. input student's ID to start the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    student_id=models.StringField(
        label="Please input your student ID",
    )


# PAGES
class MyPage(Page):
    form_model="player"
    form_fields=["student_id"]

    def before_next_page(self, timeout_happened):
        # Store student_id in participant.vars for use in other apps
        self.participant.vars['student_id'] = self.student_id
class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage]
