from os import environ

SESSION_CONFIGS = [
    dict(
        name='trading_exp',
        display_name='Trading Experiment',
        app_sequence=['d_trading_two_apps_1', 'd_trading_two_apps_2'],
        num_demo_participants=2,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)

# These fields will be accessible using participant.field_name
PARTICIPANT_FIELDS = [
    'student_id',
    'partner_id',
    'utility_type',
    'alpha',
    'beta',
    'endowment_a',
    'endowment_b',
    'current_a',
    'current_b',
    'initial_utility',
    'last_trade_a',
    'last_trade_b'
]

SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'SGD'
USE_POINTS = True

DEMO_PAGE_INTRO_HTML = """
"""

SECRET_KEY = '2195771880952'