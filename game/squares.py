"""
财富流游戏格子系统 - Game Squares System
具体的棋盘格子实现，每种格子都有自己的特殊事件和效果

文件功能概述：
==============
本文件实现了财富流游戏中所有具体的格子类型，每个格子都有独特的
游戏事件和效果。这些格子是玩家在棋盘上移动时会遇到的各种情况，
直接影响玩家的财务状况和游戏进程。

主要组件：
----------
1. StartSquare - 起始点格子
   - 游戏开始位置
   - 经过时无特殊效果

2. PaycheckSquare - 发薪水格子  
   - 收取工资和被动收入
   - 支付月支出
   - 计算净收入

3. OpportunitySquare - 机会格子
   - 抽取投资机会卡片
   - 提供各种投资选择
   - 支持不同卡片类型概率控制

4. DoodadSquare - 意外支出格子
   - 随机生成意外支出事件
   - 模拟现实生活中的突发费用
   - 预定义多种支出类型

5. MarketSquare - 市场格子
   - 进入资产买卖市场
   - 允许玩家交易资产
   - 资产价值变动处理

6. CharitySquare - 慈善格子
   - 根据孩子数量获得慈善奖励
   - 体现富爸爸理念中的回馈社会
   - 孩子数量价值体现

7. DownsizedSquare - 裁员格子
   - 模拟职业风险
   - 暂时失去工资收入
   - 持续2轮的负面效果

8. BabySquare - 生孩子格子
   - 增加孩子数量
   - 增加月支出
   - 为慈善格子提供正面效果

9. LayerTransitionSquare - 层级转换格子
   - 允许在不同圈层之间移动
   - 支持自动和手动转换
   - 特殊的星号位置处理

核心功能：
----------
- 事件驱动的格子行为系统
- 玩家财务状态的直接影响
- 随机事件生成与处理
- 复杂的层级转换逻辑
- 游戏引擎状态管理集成
- 丰富的游戏事件反馈

技术特点：
----------
- 继承自抽象基类Square
- 统一的事件触发接口
- 灵活的参数配置系统
- 完整的错误处理
- 可扩展的格子类型架构

游戏设计理念：
--------------
- 模拟真实的财务环境
- 平衡风险与机会
- 教育性与娱乐性结合
- 策略选择的重要性
- 财务管理技能培养

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
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

class LayerTransitionSquare(Square):
    """层级转换格子 - 允许在不同圈层之间移动"""
    
    def __init__(self, name, position):
        super().__init__(name, SquareType.LAYER_TRANSITION, position)
        self.description = "层级转换：自动切换到其他圈层"
        self.target_layer = "middle"  # 默认目标层级
    
    def trigger_event(self, player, game_engine):
        """触发层级转换事件"""
        # 记录当前层级
        current_layer = getattr(player, "active_layer", "middle")
        
        # 确定目标层级
        target_layer = getattr(self, "target_layer", None)
        
        if target_layer and target_layer != current_layer:
            # 直接执行层级切换
            success, message = game_engine.change_player_layer(player, target_layer)
            return message
        elif current_layer == "inner" and player.position == 5:
            # 内圈位置5（星号*）的特殊情况：自动转换到中圈
            game_engine.layer_transition_player = player
            success, message = game_engine.change_player_layer(player, "middle")
            game_engine.layer_transition_player = None
            game_engine.layer_transition_active = False
            return message
        else:
            # 其他情况：设置默认目标层级
            default_target = "inner" if current_layer == "middle" else "middle"
            success, message = game_engine.change_player_layer(player, default_target)
            return message 