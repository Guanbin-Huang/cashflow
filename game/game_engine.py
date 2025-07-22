"""
财富流游戏引擎 - Game Engine Core
控制整个财富流游戏的核心逻辑

文件功能概述：
==============
本文件是财富流游戏的核心控制器，负责管理游戏的整个生命周期，
从游戏初始化到结束的所有逻辑控制。它是连接游戏界面、玩家操作
和游戏规则的中枢神经系统。

主要组件：
----------
1. GamePhase枚举 - 游戏阶段状态
   - WAITING: 等待开始
   - PLAYING: 游戏进行中
   - PAUSED: 游戏暂停
   - FINISHED: 游戏结束

2. TurnPhase枚举 - 回合阶段状态
   - ROLL_DICE: 投骰子阶段
   - MOVE: 移动阶段
   - SQUARE_EVENT: 格子事件处理阶段
   - CARD_DECISION: 卡片决策阶段
   - MARKET: 市场操作阶段
   - LAYER_TRANSITION: 层级转换阶段
   - END_TURN: 结束回合阶段

3. GameEngine类 - 游戏主控制器
   - 游戏状态管理
   - 玩家轮次控制
   - 事件触发和处理
   - 规则验证和执行

核心功能：
----------
- 游戏初始化和玩家配置
- 回合制游戏流程控制
- 骰子投掷和玩家移动逻辑
- 格子事件触发和处理
- 卡片抽取和决策处理
- 市场交易管理
- 三层圈转换机制
- 财务自由判断和游戏胜利条件
- 游戏日志记录和状态跟踪

技术特点：
----------
- 状态机模式管理游戏流程
- 事件驱动的游戏架构
- 模块化的组件集成
- 完整的错误处理机制
- 可扩展的游戏规则系统

游戏规则实现：
--------------
- 支持2-6人游戏
- 三层圈棋盘系统（内圈、中圈、外圈）
- 复杂的层级转换规则
- 多种格子事件处理
- 投资机会卡片系统
- 市场买卖机制
- 裁员、生孩子等生活事件
- 财务自由胜利条件

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

import random
from enum import Enum

from .board import GameBoard
from cards import CardManager
from player import Player

class GamePhase(Enum):
    """游戏阶段"""
    WAITING = "等待开始"
    PLAYING = "游戏中"
    PAUSED = "暂停"
    FINISHED = "游戏结束"

class TurnPhase(Enum):
    """回合阶段"""
    ROLL_DICE = "投骰子"
    MOVE = "移动"
    SQUARE_EVENT = "格子事件"
    CARD_DECISION = "卡片决策"
    MARKET = "市场操作"
    LAYER_TRANSITION = "层级转换"  # 新增层级转换阶段
    END_TURN = "结束回合"

class GameEngine:
    """游戏引擎主类"""
    
    def __init__(self, players_data=None, config_file=None):
        # 游戏状态
        self.game_phase = GamePhase.WAITING
        self.turn_phase = TurnPhase.ROLL_DICE
        self.turn_count = 0
        self.current_player_index = 0
        
        # 调试模式
        self.debug_mode = False
        
        # 游戏组件
        self.board = GameBoard(config_file)
        self.card_manager = CardManager()
        self.players = []
        
        # 当前状态
        self.current_dice_roll = 0
        self.current_opportunity_card = None
        self.market_mode = False
        self.layer_transition_active = False  # 是否激活层级转换
        self.layer_transition_player = None   # 正在转换层级的玩家
        self.game_log = []
        
        # 初始化玩家
        if players_data:
            self._initialize_players(players_data)
    
    def _initialize_players(self, players_data):
        """初始化玩家"""
        for player_data in players_data:
            player = Player(**player_data)
            player.position = 0  # 起始位置
            self.players.append(player)
        
        self.log(f"游戏初始化完成，{len(self.players)} 名玩家准备就绪")
    
    def start_game(self):
        """开始游戏"""
        if len(self.players) < 2:
            return False, "至少需要2名玩家才能开始游戏"
        
        self.game_phase = GamePhase.PLAYING
        self.turn_phase = TurnPhase.ROLL_DICE
        self.current_player_index = 0
        self.turn_count = 1
        
        self.log("游戏开始！")
        return True, f"游戏开始，{self.get_current_player().name} 先行"
    
    def roll_dice(self):
        """投骰子"""
        if self.turn_phase != TurnPhase.ROLL_DICE:
            return False, "现在不是投骰子阶段"
        
        self.current_dice_roll = random.randint(1, 6)
        self.turn_phase = TurnPhase.MOVE
        
        current_player = self.get_current_player()
        self.log(f"{current_player.name} 投出了 {self.current_dice_roll} 点")
        
        return True, f"投出 {self.current_dice_roll} 点"
    
    def roll_dice_debug(self, dice_value):
        """调试模式投骰子"""
        if self.turn_phase != TurnPhase.ROLL_DICE:
            return False, "现在不是投骰子阶段"
        
        if not self.debug_mode:
            return False, "调试模式未启用"
        
        if not (1 <= dice_value <= 6):
            return False, "骰子点数必须在1-6之间"
        
        self.current_dice_roll = dice_value
        self.turn_phase = TurnPhase.MOVE
        
        current_player = self.get_current_player()
        self.log(f"{current_player.name} 投出了 {self.current_dice_roll} 点")
        
        return True, f"投出 {self.current_dice_roll} 点"
    
    def move_player(self):
        """移动当前玩家"""
        if self.turn_phase != TurnPhase.MOVE:
            return False, "现在不是移动阶段"
        
        current_player = self.get_current_player()
        old_position = current_player.position
        
        # 获取玩家当前所在层级
        current_layer = getattr(current_player, "active_layer", "middle")
        
        # 使用当前层级计算新位置
        new_position = self.board.get_next_position(old_position, self.current_dice_roll, current_layer)
        
        # 无论在哪个层级，都设置新位置
        current_player.position = new_position
        self.log(f"{current_player.name} 从位置 {old_position} 移动到位置 {new_position}: ({current_layer}层)")
        
        self.turn_phase = TurnPhase.SQUARE_EVENT
        
        # 获取新位置的格子
        square = self.board.get_square(current_player.position, getattr(current_player, "active_layer", "middle"))
        if square:
            self.log(f"到达: {square.name}")
        
        # 触发格子事件
        return self.trigger_square_event()
    
    def trigger_square_event(self):
        """触发格子事件"""
        if self.turn_phase != TurnPhase.SQUARE_EVENT:
            return False, "现在不是格子事件阶段"
        
        current_player = self.get_current_player()
        current_layer = getattr(current_player, "active_layer", "middle")
        square = self.board.get_square(current_player.position, current_layer)
        
        # 处理裁员状态
        if hasattr(current_player, 'downsized_turns') and current_player.downsized_turns > 0:
            if square.type.value == "发薪水":
                current_player.downsized_turns -= 1
                self.log(f"{current_player.name} 被裁员中，跳过工资收入。剩余 {current_player.downsized_turns} 回合")
                self.turn_phase = TurnPhase.END_TURN
                return True, "裁员中，跳过工资收入"
        
        # 触发格子事件
        event_result = square.trigger_event(current_player, self)
        self.log(event_result)
        
        # 根据格子类型决定下一阶段
        if square.type.value == "机会" and self.current_opportunity_card:
            self.turn_phase = TurnPhase.CARD_DECISION
        elif square.type.value == "市场" and self.market_mode:
            self.turn_phase = TurnPhase.MARKET
        elif square.type.value == "层级转换" and self.layer_transition_active:
            self.turn_phase = TurnPhase.LAYER_TRANSITION
        else:
            self.turn_phase = TurnPhase.END_TURN
        
        return True, event_result
    
    def handle_card_decision(self, decision, additional_data=None):
        """处理卡片决策"""
        if self.turn_phase != TurnPhase.CARD_DECISION or not self.current_opportunity_card:
            return False, "现在不是卡片决策阶段或没有可用卡片"
        
        current_player = self.get_current_player()
        card = self.current_opportunity_card
        
        if decision == "buy":
            # 处理购买
            if card.type.value == "金融卡":
                # 金融卡需要额外的股数信息
                shares = additional_data.get('shares', card.min_shares) if additional_data else card.min_shares
                success, message = card.execute_purchase(current_player, shares)
            else:
                success, message = card.execute_purchase(current_player)
            
            self.log(f"{current_player.name}: {message}")
            result_message = message
            
        elif decision == "pass":
            result_message = f"{current_player.name} 放弃了卡片: {card.name}"
            self.log(result_message)
        else:
            return False, "无效的决策"
        
        # 清除当前卡片
        self.current_opportunity_card = None
        self.turn_phase = TurnPhase.END_TURN
        
        return True, result_message
    
    def handle_market_action(self, action, data=None):
        """处理市场操作"""
        if self.turn_phase != TurnPhase.MARKET:
            return False, "现在不是市场阶段"
        
        current_player = self.get_current_player()
        
        if action == "sell_asset":
            # 卖出资产
            asset_index = data.get('asset_index')
            price = data.get('price')
            buyer_index = data.get('buyer_index', None)
            
            if asset_index is not None and asset_index < len(current_player.assets):
                asset = current_player.assets[asset_index]
                
                if buyer_index is not None:
                    # 卖给其他玩家
                    buyer = self.players[buyer_index]
                    success = current_player.transfer_asset_to(buyer, asset, price)
                    message = f"资产交易{'成功' if success else '失败'}"
                else:
                    # 卖给银行
                    current_player.assets.remove(asset)
                    current_player.cash += price
                    if hasattr(asset, 'passive_income'):
                        current_player.passive_income -= asset.passive_income
                    message = f"卖出资产 {asset.name}，获得 {price} 元"
                
                self.log(f"{current_player.name}: {message}")
                return True, message
            
        elif action == "exit_market":
            self.market_mode = False
            self.turn_phase = TurnPhase.END_TURN
            return True, "退出市场"
        
        return False, "无效的市场操作"
        
    def change_player_layer(self, player, target_layer):
        """改变玩家所在层级"""
        if target_layer not in ["inner", "middle", "outer"]:
            return False, f"无效的层级: {target_layer}"
        
        # 记录原层级和位置
        original_layer = getattr(player, "active_layer", "middle")
        original_position = player.position
        
        # 设置新层级
        player.active_layer = target_layer
        
        # 根据转换规则设置新位置
        if original_layer == "middle" and target_layer == "inner":
            # 中层转换到内层：中层18->内层1，中层6->内层9
            if original_position == 18:
                player.position = 1
            elif original_position == 6:
                player.position = 9
            else:
                # 其他位置默认到内层1
                player.position = 1
        elif original_layer == "inner" and target_layer == "middle":
            # 内层位置5（星号*）的转换会在handle_layer_transition中特殊处理
            # 其他内层位置转换到中层
            if original_position == 1:
                player.position = 18
            elif original_position == 9:
                player.position = 6
            else:
                # 其他位置默认到中层0
                player.position = 0
        else:
            # 其他层级转换默认到起点
            player.position = 0
        
        self.log(f"{player.name} 从 {original_layer} 层级位置 {original_position} 移动到 {target_layer} 层级位置 {player.position}")
        return True, f"成功切换到 {target_layer} 层级"

    def handle_layer_transition(self, target_layer, target_position=None):
        """处理层级转换决策"""
        if not self.layer_transition_active:
            return False, "当前不在层级转换阶段"
        
        if not self.layer_transition_player:
            return False, "没有要转换层级的玩家"
        
        player = self.layer_transition_player
        current_layer = getattr(player, "active_layer", "middle")
        
        # 执行层级切换
        success = False
        message = ""
        
        # 如果玩家在内层且位于位置5（星号*位置），可以选择中层的任一格子
        if current_layer == "inner" and player.position == 5 and target_layer == "middle" and target_position is not None:
            # 设置新层级
            player.active_layer = "middle"
            # 设置新位置
            middle_circle_size = self.board.get_circle_size("middle")
            if 0 <= target_position < middle_circle_size:
                player.position = target_position
                success = True
                message = f"{player.name} 从内层的*位置移动到中层位置 {target_position}"
                self.log(message)
            else:
                # 无效位置，默认到中层起始点
                player.position = 0
                success = True
                message = f"{player.name} 指定的中层位置无效，移动到中层起始点"
                self.log(message)
        else:
            # 常规层级切换
            success, message = self.change_player_layer(player, target_layer)
        
        # 重置层级转换状态
        self.layer_transition_active = False
        self.layer_transition_player = None
        
        if success:
            self.turn_phase = TurnPhase.END_TURN
        
        return success, message
    
    def end_turn(self):
        """结束当前回合"""
        if self.turn_phase != TurnPhase.END_TURN and self.turn_phase != TurnPhase.LAYER_TRANSITION:
            return False, "回合尚未结束"
        
        current_player = self.get_current_player()
        
        # 清除任何可能的层级转换状态
        self.layer_transition_active = False
        self.layer_transition_player = None
        
        # 检查财务自由
        if current_player.is_financially_free():
            self.game_phase = GamePhase.FINISHED
            self.log(f"游戏结束！{current_player.name} 达到了财务自由！")
            return True, f"{current_player.name} 获胜！"
        
        # 切换到下一个玩家
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # 如果回到第一个玩家，增加回合数
        if self.current_player_index == 0:
            self.turn_count += 1
        
        # 重置回合状态
        self.turn_phase = TurnPhase.ROLL_DICE
        self.current_dice_roll = 0
        self.current_opportunity_card = None
        self.market_mode = False
        self.layer_transition_active = False
        self.layer_transition_player = None
        
        next_player = self.get_current_player()
        self.log(f"轮到 {next_player.name}")
        
        return True, f"轮到 {next_player.name}"
    
    def get_current_player(self):
        """获取当前玩家"""
        if 0 <= self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
    
    def get_game_state(self):
        """获取游戏状态"""
        return {
            'game_phase': self.game_phase.value,
            'turn_phase': self.turn_phase.value,
            'turn_count': self.turn_count,
            'current_player': self.get_current_player().name if self.get_current_player() else None,
            'current_dice_roll': self.current_dice_roll,
            'current_card': str(self.current_opportunity_card) if self.current_opportunity_card else None,
            'market_mode': self.market_mode,
            'players': [self._get_player_summary(p) for p in self.players]
        }
    
    def _get_player_summary(self, player):
        """获取玩家摘要信息"""
        return {
            'name': player.name,
            'position': player.position,
            'cash': player.cash,
            'passive_income': player.passive_income,
            'expenses': player.expenses,
            'financially_free': player.is_financially_free(),
            'assets_count': len(player.assets),
            'liabilities_count': len(player.liabilities)
        }
    
    def log(self, message):
        """记录游戏日志"""
        self.game_log.append(f"回合{self.turn_count}: {message}")
        print(f"[游戏日志] {message}")
    
    def get_recent_log(self, count=10):
        """获取最近的游戏日志"""
        return self.game_log[-count:] if len(self.game_log) > count else self.game_log.copy()
    
    def save_game(self, filename):
        """保存游戏状态"""
        # 这里可以实现游戏保存功能
        pass
    
    def load_game(self, filename):
        """加载游戏状态"""
        # 这里可以实现游戏加载功能
        pass 