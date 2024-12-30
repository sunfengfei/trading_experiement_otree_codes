from otree.api import *
import random
import math

doc = """
Trading experiment with different utility functions and endowments.
Players need to calculate initial utility and can trade goods with others.
"""

class C(BaseConstants):
    NAME_IN_URL = 'trading_2'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    
    TOTAL_ENDOWMENT = 10
    UTILITY_TYPES = ['CD', 'LINEAR', 'MIN']
    ALPHA_RANGE = (0.2, 0.8)
    BETA_RANGE = (0.2, 0.8)
    UTILITY_THRESHOLD = 0.02


def creating_session(subsession):
    for player in subsession.get_players():
        # 使用 vars.get() 安全地获取 participant 变量，提供默认值
        player.student_id = player.participant.vars.get('student_id', '')
        player.utility_type = player.participant.vars.get('utility_type', random.choice(C.UTILITY_TYPES))
        player.alpha = player.participant.vars.get('alpha', round(random.uniform(0.2, 0.8), 2))
        player.beta = player.participant.vars.get('beta', round(random.uniform(0.2, 0.8), 2))
        player.endowment_a = player.participant.vars.get('endowment_a', random.randint(0, C.TOTAL_ENDOWMENT))
        player.endowment_b = player.participant.vars.get('endowment_b', C.TOTAL_ENDOWMENT - player.endowment_a)
        player.current_a = player.participant.vars.get('current_a', player.endowment_a)
        player.current_b = player.participant.vars.get('current_b', player.endowment_b)
        player.calculated_utility = player.participant.vars.get('calculated_utility', 0)
        player.partner_id = player.participant.vars.get('partner_id', '')

        # 打印调试信息
        print(f"Initializing player {player.id_in_group}:")
        print(f"student_id: {player.student_id}")
        print(f"utility_type: {player.utility_type}")
        print(f"alpha: {player.alpha}")
        print(f"beta: {player.beta}")
        print(f"endowments: A={player.endowment_a}, B={player.endowment_b}")

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
        for p in players:
            if p.field_maybe_none('trade_a') is None or p.field_maybe_none('trade_b') is None:
                print(f"Trade verification failed: Missing trade values for player {p.id_in_group}")
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

                # 更新 participant 变量
                p.participant.vars['current_a'] = p.current_a
                p.participant.vars['current_b'] = p.current_b
                p.participant.vars['last_trade_a'] = abs(p.trade_a)
                p.participant.vars['last_trade_b'] = abs(p.trade_b)
                
                print(f"  After trade: A={p.current_a}, B={p.current_b}")
                    
            # 更新最近交易记录
            self.subsession.last_trade_a = abs(players[0].trade_a)
            self.subsession.last_trade_b = abs(players[0].trade_b)
            
            return True
        return False

class Player(BasePlayer):
    # Carry over fields from previous app
    student_id = models.StringField()
    partner_id = models.StringField()
    utility_type = models.StringField()
    alpha = models.FloatField()
    beta = models.FloatField()
    endowment_a = models.IntegerField()
    endowment_b = models.IntegerField()
    current_a = models.IntegerField()
    current_b = models.IntegerField()
    calculated_utility = models.FloatField()
    
    # New fields for trading
    trade_a = models.IntegerField(blank=True)
    trade_b = models.IntegerField(blank=True)
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

# Pages
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


class Trading(Page):
    form_model = 'player'
    form_fields = ['trade_a', 'trade_b', 'trade_a_is_buy', 'trade_b_is_buy']
    
    def error_message(self, values):
        # 检查交易值是否已填写
        if values['trade_a'] is None or values['trade_b'] is None:
            return 'Please input both trade amounts'
        
    def vars_for_template(self):
        return {
            'current_a': self.current_a,
            'current_b': self.current_b,
            'utility_type': self.utility_type,
            'alpha': self.alpha,
            'beta': self.beta,
            'current_utility': self.calculate_utility(),
            'initial_utility': self.calculated_utility,
            'partner_id': self.partner_id
        }
    

class TradeWaitPage(WaitPage):
    def _reset_trades(self):
        for p in self.group.get_players():
            print(f"Resetting trades for player {p.id_in_group}")
            p.trade_a = None
            p.trade_b = None

    def after_all_players_arrive(self):
        print("TradeWaitPage: Starting trade verification...")
        
        if self.group.verify_trade():
            print("Trade verified successfully, executing trade...")
            if self.group.execute_trade():
                print("Trade executed successfully")
                # Update participant variables after successful trade
                for p in self.group.get_players():
                    p.participant.current_a = p.current_a
                    p.participant.current_b = p.current_b
            else:
                print("Trade execution failed")
                self._reset_trades()
        else:
            print("Trade verification failed")
            self._reset_trades()

class Results(Page):
    def vars_for_template(self):
        return {
            'final_a': self.current_a,
            'final_b': self.current_b,
            'final_utility': self.calculate_utility(),
            'initial_utility': self.calculated_utility,    
            # 'initial_utility': self.field_maybe_none('calculated_utility') or 0,
            'utility_type': self.utility_type,
            'alpha': self.alpha,
            'beta': self.beta,
            'initial_a': self.endowment_a,
            'initial_b': self.endowment_b
        }

page_sequence = [
    MatchingWaitPage,
    Trading,
    TradeWaitPage,
    Results
]