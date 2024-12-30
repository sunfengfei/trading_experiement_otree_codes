from otree.api import *
import random
import math

doc = """
Trading experiment with different utility functions and endowments.
Players need to calculate initial utility and can trade goods with others.
"""

class C(BaseConstants):
    NAME_IN_URL = 'trading'
    PLAYERS_PER_GROUP = 2
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
    # market price
    last_trade_a = models.IntegerField(initial=0, default=0)
    last_trade_b = models.IntegerField(initial=0, default=0)

    def get_market_price(self):
        if self.last_trade_b == 0:
            return None
        return self.last_trade_a / self.last_trade_b
    
     
class Group(BaseGroup):
    
    
    def verify_trade(self):
        players = self.get_players()
        if len(players) != 2:
            print("Trade verification failed: Not exactly 2 players")
            return False
            
        # 计算实际交易量
        # A: 根据is_buy方向转换正负
        # B: 数值保持不变，只用于验证
        p0_trade_a = players[0].trade_a if players[0].trade_a_is_buy else -players[0].trade_a
        p0_trade_b = players[0].trade_b
        p1_trade_a = players[1].trade_a if players[1].trade_a_is_buy else -players[1].trade_a
        p1_trade_b = players[1].trade_b
        
        print(f"Verifying trades:")
        print(f"Player 1: A={p0_trade_a}, B={p0_trade_b}")
        print(f"Player 2: A={p1_trade_a}, B={p1_trade_b}")
        
        # 简化的验证：A检查正负匹配，B检查数值相等
        trades_match = (p0_trade_a == -p1_trade_a) and (p0_trade_b == p1_trade_b)
        print(f"Trades match: {trades_match}")
        
        if not trades_match:
            print("Trade verification failed: Trades don't match")
            return False
        
        # 验证交易后数量为非负数
        for p in players:
            # A: 保持原有的买卖方向逻辑
            actual_trade_a = p.trade_a if p.trade_a_is_buy else -p.trade_a
            # B: trade_b的符号与trade_a_is_buy相反
            actual_trade_b = -p.trade_b if p.trade_a_is_buy else p.trade_b
            
            final_a = p.current_a + actual_trade_a
            final_b = p.current_b + actual_trade_b
            
            print(f"Player {p.id_in_group} final calculation:")
            print(f"  Current holdings: A={p.current_a}, B={p.current_b}")
            print(f"  Actual trades: A={actual_trade_a}, B={actual_trade_b}")
            print(f"  Final holdings: A={final_a}, B={final_b}")
            
            if final_a < 0 or final_b < 0:
                print(f"Trade verification failed: Negative holdings for player {p.id_in_group}")
                return False
                
        print("Trade verification passed")
        return True
    
    def execute_trade(self):
        if self.verify_trade():
            players = self.get_players()
            print("Executing trade...")
            
            for p in players:
                # A: 保持原有的买卖方向逻辑
                actual_trade_a = p.trade_a if p.trade_a_is_buy else -p.trade_a
                # B: trade_b的符号与trade_a_is_buy相反
                actual_trade_b = -p.trade_b if p.trade_a_is_buy else p.trade_b
                
                print(f"Player {p.id_in_group}:")
                print(f"  Before trade: A={p.current_a}, B={p.current_b}")
                print(f"  Trading: A={actual_trade_a}, B={actual_trade_b}")
                
                # 更新持有量
                p.current_a += actual_trade_a
                p.current_b += actual_trade_b
                
                print(f"  After trade: A={p.current_a}, B={p.current_b}")
                    
            # 更新最近交易记录
            self.subsession.last_trade_a = abs(players[0].trade_a)
            self.subsession.last_trade_b = abs(players[0].trade_b)
            
            return True
        return False

class Player(BasePlayer):
    student_id=models.StringField(
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
    
    trade_a = models.IntegerField()
    trade_b = models.IntegerField()

    # Add new fields to track trade direction
    trade_a_is_buy = models.BooleanField(initial=True)
    trade_b_is_buy = models.BooleanField(initial=True)

    
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

    def calculate_actual_trade(self, trade_amount, is_buy):
        """Helper function to calculate actual trade amount based on direction"""
        if trade_amount is None:
            return 0
        return trade_amount if is_buy else -trade_amount

    def get_final_holdings(self):
        """Calculate final holdings based on trade direction"""
        # Calculate actual trade amounts
        actual_trade_a = self.calculate_actual_trade(self.trade_a, self.trade_a_is_buy)
        actual_trade_b = self.calculate_actual_trade(self.trade_b, self.trade_b_is_buy)
        
        # Calculate final holdings
        final_a = self.current_a + actual_trade_a
        final_b = self.current_b + actual_trade_b
            
        return final_a, final_b
    
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

class Calculator(Page):
    form_model = 'player'
    form_fields = ['partner_id']

    def error_message(self, values):
        if values['partner_id'] == self.student_id:
            return 'You cannot trade with yourself'


class MatchingWaitPage(WaitPage):
    title_text = "Waiting for matching"
    body_text = "Waiting for your trading partner"
    wait_for_all_groups = False
    group_by_arrival_time = True

    @staticmethod
    def group_by_arrival_time_method(subsession, waiting_players):
        """根据到达时间动态配对"""
        print(f"Current waiting players: {[p.student_id for p in waiting_players]}")
        
        for p1 in waiting_players:
            if not p1.partner_id:
                continue
                
            # 在等待的玩家中寻找匹配的交易对象
            p2 = next(
                (p for p in waiting_players 
                 if p != p1 and  # 不是同一个玩家
                 p.student_id == p1.partner_id),  # p2的学号与p1选择的交易对象匹配
                None
            )
            
            if p2:
                print(f"Matching successful:")
                print(f"Player 1 (ID: {p1.student_id}) with partner_id: {p1.partner_id}")
                print(f"Player 2 (ID: {p2.student_id}) with partner_id: {p2.partner_id}")
                return [p1, p2]
                
        print("No match found in current waiting players")
        return None

    
    @staticmethod
    def is_displayed(player):
        return player.field_maybe_none('student_id') is not None and player.field_maybe_none('partner_id') is not None

# 去掉了get_players_for_wait_page方法,因为使用group_by_arrival_time_method时不需要它
class Trading(Page):
    form_model = 'player'
    form_fields = ['trade_a', 'trade_b', 'trade_a_is_buy', 'trade_b_is_buy']  # 确保包含买卖方向字段
    
    # def before_next_page(self, timeout_happened=False):
    #     # 这里会使得哪怕失败的交易也会更新
    #     self.subsession.last_trade_a = abs(self.trade_a) if self.trade_a else 0
    #     self.subsession.last_trade_b = abs(self.trade_b) if self.trade_b else 0


class TradeWaitPage(WaitPage):
    title_text = "Waiting for Trade Confirmation"
    body_text = "Please wait patiently while the system verifies the trade."
    
    def after_all_players_arrive(self):
        print("TradeWaitPage: Starting trade verification...")
        
        if self.group.verify_trade():
            print("Trade verified successfully, executing trade...")
            if self.group.execute_trade():
                print("Trade executed successfully")
            else:
                print("Trade execution failed")
                self._reset_trades()
        else:
            print("Trade verification failed")
            self._reset_trades()
    
    def _reset_trades(self):
        for p in self.group.get_players():
            print(f"Resetting trades for player {p.id_in_group}")
            p.trade_a = None
            p.trade_b = None
            

class Results(Page):
    def vars_for_template(self):
        return {
            'final_a': self.current_a,
            'final_b': self.current_b,
            'final_utility': self.calculate_utility(),
            'initial_utility': self.field_maybe_none('calculated_utility') or 0,
            'utility_type': self.utility_type,
            'alpha': self.alpha,
            'beta': self.beta,
            'initial_a': self.endowment_a,
            'initial_b': self.endowment_b
        }

page_sequence = [
    
    Intro,
    # ParameterDisplay,
    Calculator,
    MatchingWaitPage,
    Trading,
    TradeWaitPage,
    Results
]