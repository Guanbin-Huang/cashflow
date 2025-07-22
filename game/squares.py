"""
具体的棋盘格子实现
每种格子都有自己的特殊事件和效果
"""

import random
from .board import Square, SquareType
from cards.base import CardType

class StartSquare(Square):
    """起始点格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.START, position)
        self.description = "游戏起始点，经过时无特殊效果"
    
    def trigger_event(self, player, game_engine):
        """起始点无特殊效果"""
        return f"{player.name} 经过了起始点"

class PaycheckSquare(Square):
    """发薪水格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.PAYCHECK, position)
        self.description = "收取工资和被动收入，支付月支出"
    
    def trigger_event(self, player, game_engine):
        """处理月收支"""
        # 收取工资
        player.receive_salary()
        
        # 收取被动收入
        player.receive_passive_income()
        
        # 支付支出
        player.pay_expenses()
        
        # 计算净收入
        net_income = player.salary + player.passive_income - player.expenses
        
        return (f"{player.name} 收支结算: "
                f"工资 {player.salary} + 被动收入 {player.passive_income} "
                f"- 支出 {player.expenses} = 净收入 {net_income}")

class OpportunitySquare(Square):
    """机会格子 - 抽取投资机会卡片"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.OPPORTUNITY, position)
        self.description = "抽取投资机会卡片"
    
    def trigger_event(self, player, game_engine):
        """抽取机会卡片"""
        # 随机选择卡片类型（可以根据游戏规则调整概率）
        card_types = [CardType.ENTERPRISE, CardType.OPPORTUNITY, 
                     CardType.FINANCIAL, CardType.SIDE_BUSINESS]
        weights = [0.2, 0.4, 0.3, 0.1]  # 不同卡片类型的出现概率
        
        card_type = random.choices(card_types, weights=weights)[0]
        card = game_engine.card_manager.draw_card(card_type)
        
        if card:
            # 将卡片提供给玩家选择
            game_engine.current_opportunity_card = card
            return f"{player.name} 抽到了机会卡片: {card}"
        else:
            return f"{player.name} 抽卡失败，没有可用的 {card_type.value}"

class DoodadSquare(Square):
    """意外支出格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.DOODAD, position)
        self.description = "遇到意外支出"
        # 预定义一些意外支出事件
        self.doodad_events = [
            ("汽车维修", 800, 1500),
            ("医疗费用", 500, 2000),
            ("家电维修", 300, 800),
            ("宠物医疗", 400, 1200),
            ("房屋维修", 1000, 3000),
            ("罚款", 200, 600),
            ("朋友聚会", 300, 800),
            ("购物冲动", 500, 1200)
        ]
    
    def trigger_event(self, player, game_engine):
        """处理意外支出"""
        event_name, min_cost, max_cost = random.choice(self.doodad_events)
        cost = random.randint(min_cost, max_cost)
        
        # 扣除现金
        player.cash -= cost
        
        return f"{player.name} 遇到意外支出: {event_name}，花费 {cost} 元"

class MarketSquare(Square):
    """市场格子 - 可以买卖资产"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.MARKET, position)
        self.description = "市场：可以买卖资产"
    
    def trigger_event(self, player, game_engine):
        """进入市场"""
        game_engine.market_mode = True
        return f"{player.name} 进入了市场，可以买卖资产"

class CharitySquare(Square):
    """慈善格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.CHARITY, position)
        self.description = "做慈善，根据孩子数量获得奖励"
    
    def trigger_event(self, player, game_engine):
        """慈善事件"""
        # 假设玩家有children属性，如果没有则为0
        children = getattr(player, 'children', 0)
        charity_amount = children * 100  # 每个孩子100元慈善奖励
        
        if charity_amount > 0:
            player.cash += charity_amount
            return f"{player.name} 做慈善，{children} 个孩子获得 {charity_amount} 元奖励"
        else:
            return f"{player.name} 做慈善，但没有孩子，无奖励"

class DownsizedSquare(Square):
    """裁员格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.DOWNSIZED, position)
        self.description = "被裁员，失去2轮工资收入"
    
    def trigger_event(self, player, game_engine):
        """处理裁员事件"""
        # 设置裁员状态
        player.downsized_turns = getattr(player, 'downsized_turns', 0) + 2
        return f"{player.name} 被裁员了！将失去接下来2轮的工资收入"

class BabySquare(Square):
    """生孩子格子"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.BABY, position)
        self.description = "生孩子，增加支出但也有潜在好处"
    
    def trigger_event(self, player, game_engine):
        """处理生孩子事件"""
        # 增加孩子数量
        if not hasattr(player, 'children'):
            player.children = 0
        player.children += 1
        
        # 增加月支出
        additional_expense = 300  # 每个孩子增加300元月支出
        player.expenses += additional_expense
        
        return f"{player.name} 生了一个孩子！现在有 {player.children} 个孩子，月支出增加 {additional_expense} 元" 