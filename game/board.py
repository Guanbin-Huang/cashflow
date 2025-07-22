"""
财富流游戏棋盘系统 - Game Board System
定义游戏棋盘和各种格子类型

文件功能概述：
==============
本文件定义了财富流游戏的核心棋盘系统，包括三层圈的棋盘结构、
各种格子类型和棋盘配置管理。它是游戏空间逻辑的基础架构。

主要组件：
----------
1. SquareType枚举 - 定义所有格子类型
   - PAYCHECK: 发薪水格子
   - OPPORTUNITY: 机会格子（抽卡）
   - DOODAD: 意外支出格子
   - MARKET: 市场格子
   - CHARITY: 慈善格子
   - DOWNSIZED: 裁员格子
   - BABY: 生孩子格子
   - START: 起始点格子
   - LAYER_TRANSITION: 层级转换格子

2. Square抽象基类 - 格子基础接口
   - 定义格子的基本属性和行为
   - 抽象方法trigger_event()需要子类实现

3. GameBoard类 - 游戏棋盘主控制器
   - 管理三层圈棋盘结构
   - 处理玩家位置计算
   - 支持配置文件驱动的棋盘生成

核心功能：
----------
- 三层圈棋盘系统设计
  * 内圈（逆流层）：10个格子，Z字形布局，高风险高回报
  * 中圈（平流层）：24个格子，圆形布局，标准游戏区域
  * 外圈（顺流层）：32个格子，圆形布局，低风险稳健投资

- 位置计算算法
  * 圆形布局的角度计算
  * Z字形布局的特殊路径计算
  * 跨层级的位置转换

- 配置系统
  * JSON配置文件支持
  * 默认配置回退机制
  * 动态格子属性设置

技术特点：
----------
- 面向对象的格子系统设计
- 支持配置驱动的棋盘生成
- 抽象基类确保格子行为一致性
- 灵活的多层圈架构
- 向后兼容的接口设计

棋盘设计理念：
--------------
- 内圈：挑战模式，高风险高回报，适合有经验的投资者
- 中圈：标准模式，平衡的风险和机会，主要游戏区域
- 外圈：入门模式，低风险稳健投资，适合初学者
- 层级转换：提供策略选择，增加游戏深度

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

from abc import ABC, abstractmethod
from enum import Enum
import json
import os

class SquareType(Enum):
    """格子类型枚举"""
    PAYCHECK = "发薪水"          # 发薪水格子
    OPPORTUNITY = "机会"         # 机会格子（抽卡）
    DOODAD = "意外支出"          # 意外支出格子
    MARKET = "市场"             # 市场格子
    CHARITY = "慈善"            # 慈善格子
    DOWNSIZED = "裁员"          # 裁员格子
    BABY = "生孩子"             # 生孩子格子
    START = "起始点"            # 起始点
    LAYER_TRANSITION = "层级转换" # 层级转换格子

class Square(ABC):
    """棋盘格子基类"""
    
    def __init__(self, name, square_type, position):
        self.name = name
        self.type = square_type
        self.position = position
        self.description = ""
        self.layer = "middle"  # 默认在中圈
    
    @abstractmethod
    def trigger_event(self, player, game_engine):
        """触发格子事件"""
        pass
    
    def __str__(self):
        return f"{self.type.value}: {self.name}"

class GameBoard:
    """游戏棋盘"""
    
    def __init__(self, config_file=None):
        self.circles = {
            "inner": [],  # 逆流层 (绿色) - 10个格子 (包含⭐中心)
            "middle": [], # 平流层 (红色) - 24个格子
            "outer": []   # 顺流层 (蓝色) - 32个格子
        }
        self.circle_sizes = {"inner": 10, "middle": 24, "outer": 32}
        self.circle_colors = {"inner": "green", "middle": "red", "outer": "lightblue"}
        
        # 加载配置或使用默认配置
        self.config = self._load_config(config_file) if config_file else self._default_config()
        self._create_board_from_config()
        
        # 向后兼容 - 使用中圈作为默认棋盘
        self.squares = self.circles["middle"]
        self.total_squares = len(self.squares)
    
    def _load_config(self, config_file):
        """从配置文件加载棋盘配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self._default_config()
    
    def _default_config(self):
        """默认棋盘配置"""
        return {
            "circle_sizes": {"inner": 10, "middle": 24, "outer": 32},
            "circle_colors": {"inner": "green", "middle": "red", "outer": "lightblue"},
            "squares": {
                "inner": [
                    {"position": 0, "name": "空位", "type": "START"},
                    {"position": 1, "name": "逆流起点", "type": "START"},
                    {"position": 2, "name": "裁员", "type": "DOWNSIZED"},
                    {"position": 3, "name": "高额意外支出", "type": "DOODAD", "multiplier": 2.0},
                    {"position": 4, "name": "高风险机会", "type": "OPPORTUNITY", "risk_level": "high"},
                    {"position": 5, "name": "⭐转换点", "type": "LAYER_TRANSITION", "target_layer": "middle", "special": "star"},
                    {"position": 6, "name": "生孩子", "type": "BABY"},
                    {"position": 7, "name": "高额意外支出", "type": "DOODAD", "multiplier": 2.0},
                    {"position": 8, "name": "高风险市场", "type": "MARKET", "volatility": "high"},
                    {"position": 9, "name": "裁员", "type": "DOWNSIZED"}
                ],
                "middle": [
                    {"position": 0, "name": "起始点", "type": "START"},
                    {"position": 1, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 2, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 3, "name": "意外支出", "type": "DOODAD"},
                    {"position": 4, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 5, "name": "市场", "type": "MARKET"},
                    {"position": 6, "name": "层级转换(发薪水)", "type": "LAYER_TRANSITION", "target_layer": "inner"},
                    {"position": 7, "name": "慈善", "type": "CHARITY"},
                    {"position": 8, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 9, "name": "意外支出", "type": "DOODAD"},
                    {"position": 10, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 11, "name": "裁员", "type": "DOWNSIZED"},
                    {"position": 12, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 13, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 14, "name": "生孩子", "type": "BABY"},
                    {"position": 15, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 16, "name": "市场", "type": "MARKET"},
                    {"position": 17, "name": "意外支出", "type": "DOODAD"},
                    {"position": 18, "name": "层级转换(市场)", "type": "LAYER_TRANSITION", "target_layer": "inner"},
                    {"position": 19, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 20, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 21, "name": "慈善", "type": "CHARITY"},
                    {"position": 22, "name": "机会", "type": "OPPORTUNITY"},
                    {"position": 23, "name": "意外支出", "type": "DOODAD"}
                ],
                "outer": [
                    {"position": 0, "name": "顺流起点", "type": "START"},
                    {"position": 1, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 2, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 3, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 4, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 5, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 6, "name": "慈善", "type": "CHARITY"},
                    {"position": 7, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 8, "name": "低风险市场", "type": "MARKET", "volatility": "low"},
                    {"position": 9, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 10, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 11, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 12, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 13, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 14, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 15, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 16, "name": "慈善", "type": "CHARITY"},
                    {"position": 17, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 18, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 19, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 20, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 21, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 22, "name": "低风险市场", "type": "MARKET", "volatility": "low"},
                    {"position": 23, "name": "慈善", "type": "CHARITY"},
                    {"position": 24, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 25, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 26, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 27, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 28, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"},
                    {"position": 29, "name": "发薪水", "type": "PAYCHECK"},
                    {"position": 30, "name": "小额意外支出", "type": "DOODAD", "multiplier": 0.5},
                    {"position": 31, "name": "低风险机会", "type": "OPPORTUNITY", "risk_level": "low"}
                ]
            }
        }
    
    def _create_board_from_config(self):
        """根据配置创建棋盘"""
        # 导入具体的格子类
        from .squares import (StartSquare, PaycheckSquare, OpportunitySquare, 
                             DoodadSquare, MarketSquare, CharitySquare, 
                             DownsizedSquare, BabySquare, LayerTransitionSquare)
        
        # 更新圈层尺寸和颜色
        self.circle_sizes = self.config.get("circle_sizes", self.circle_sizes)
        self.circle_colors = self.config.get("circle_colors", self.circle_colors)
        
        # 创建格子类型映射
        square_classes = {
            "START": StartSquare,
            "PAYCHECK": PaycheckSquare,
            "OPPORTUNITY": OpportunitySquare,
            "DOODAD": DoodadSquare,
            "MARKET": MarketSquare,
            "CHARITY": CharitySquare,
            "DOWNSIZED": DownsizedSquare,
            "BABY": BabySquare,
            "LAYER_TRANSITION": LayerTransitionSquare,
        }
        
        # 为每个圈创建格子
        for layer_name, squares_config in self.config["squares"].items():
            for square_config in squares_config:
                position = square_config["position"]
                name = square_config["name"]
                square_type = square_config["type"]
                
                # 创建格子
                square_class = square_classes.get(square_type)
                if square_class:
                    square = square_class(name, position)
                    square.layer = layer_name
                    
                    # 添加额外配置参数
                    for key, value in square_config.items():
                        if key not in ["position", "name", "type"]:
                            setattr(square, key, value)
                    
                    # 添加到对应圈层
                    self.circles[layer_name].append(square)
            
            # 确保格子按位置排序
            self.circles[layer_name].sort(key=lambda x: x.position)
    
    def get_square(self, position, layer="middle"):
        """获取指定位置和层级的格子"""
        if layer in self.circles and 0 <= position < len(self.circles[layer]):
            return self.circles[layer][position]
        return None
    
    def get_next_position(self, current_position, steps, layer="middle"):
        """计算移动后的位置"""
        if layer in self.circles and self.circles[layer]:
            if layer == "inner":
                # 内圈特殊规则：内圈有明确的转折点和边界
                # 路径模式: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 8 → 7 → 6 → 5 → 4 → 3 → 2 → 1 → 2...
                
                # 处理内圈位置0，这是一个占位符，不应该出现
                if current_position == 0:
                    return 1  # 默认回到1
                
                # 如果当前位置是一个元组，提取位置和方向
                if isinstance(current_position, tuple):
                    position, is_moving_forward = current_position
                else:
                    position = current_position
                    is_moving_forward = position != 9  # 位置9向后移动，其他位置向前移动
                
                for _ in range(steps):
                    if is_moving_forward:  # 向前移动(数字增大)
                        position += 1
                        if position == 9:  # 到达9后，下一步开始向后
                            is_moving_forward = False
                    else:  # 向后移动(数字减小)
                        position -= 1
                        if position == 1:  # 到达1后，下一步开始向前
                            is_moving_forward = True
                
                # 为了兼容原有接口，只返回位置值，不返回方向
                return position
            else:
                # 其他层使用圆形模运算
                return (current_position + steps) % len(self.circles[layer])
        return current_position
    
    def get_circle_size(self, layer="middle"):
        """获取圈层大小"""
        return len(self.circles.get(layer, []))
    
    def get_circle_color(self, layer="middle"):
        """获取圈层颜色"""
        return self.circle_colors.get(layer, "black")
    
    def get_squares_by_type(self, square_type, layer="middle"):
        """获取指定类型的所有格子 (向后兼容)"""
        return [square for square in self.circles.get(layer, []) if square.type == square_type]
    
    def get_board_size(self):
        """获取棋盘大小 (向后兼容)"""
        return len(self.squares)
    
    def __str__(self):
        board_str = "游戏棋盘:\n"
        for layer_name, squares in self.circles.items():
            board_str += f"=== {layer_name} ===\n"
            for square in squares:
                board_str += f"  {square.position:2d}: {square}\n"
        return board_str 

