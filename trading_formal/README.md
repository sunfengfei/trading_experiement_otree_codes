# Trading Experiment Platform

This repository contains an oTree-based experimental economics platform designed for conducting trading experiments. The platform allows participants to trade goods based on personal utility functions and initial endowments.

## Repository Structure

The repository contains two main directories:

- `trading_formal/`: Contains the current stable version of the experiment
- `exp_trading-diff_versions/`: Contains different versions and iterations of the experiment for development purposes

## Experiment Workflow

The experiment follows a three-stage process:

1. **Initial Screen**
   - Participants access the experiment via web link
   - Required to input personal identifiers (Student ID and other information)

2. **Parameter Display**
   - Each participant receives:
     - Personal utility function parameters (2 parameters)
     - Initial endowments of Good A and Good B
   - Participants must calculate their initial utility level
   - Verification of calculation before proceeding

3. **Trading Interface**
   - Displays current market price (ratio of most recent trade quantities)
   - Shows current utility level
   - Provides interactive utility calculator
   - match the ID of the trading partner
   - Enables trade execution with quantity inputs for Good A and B
   - update the holdings of Good A and B, and the current utility level of the participant

## Running the Experiment

### Quick Start
1. Navigate to the `trading_formal` directory
2. Follow standard oTree setup procedures
3. Run the experiment server

### Modifying Demo Parameters
To change the number of participants in the demo:

1. Open `settings.py` in the project directory
2. Locate the `SESSION_CONFIGS` section
3. Modify the `num_demo_participants` parameter:

```python
SESSION_CONFIGS = [
    dict(
        name='trading_exp',
        display_name='Trading Experiment',
        app_sequence=['d_trading_two_apps_1','d_trading_two_apps_2'],
        num_demo_participants=4,  # Modify this number as needed
    ),
]
```

## Development

For development or testing different versions:
- Use the `exp_trading-diff_versions` directory
- Each subdirectory contains a different iteration of the experiment
- The main stable version is in `trading_formal`


## Contact

Developer: SUN Fengfei (sunfengfei@u.nus.edu)