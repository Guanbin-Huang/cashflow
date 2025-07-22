"""
游戏棋盘系统
定义游戏棋盘和各种格子类型
"""

from abc import ABC, abstractmethod
from enum import Enum

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

class Square(ABC):
    """棋盘格子基类"""
    
    def __init__(self, name, square_type, position):
        self.name = name
        self.type = square_type
        self.position = position
        self.description = ""
    
    @abstractmethod
    def trigger_event(self, player, game_engine):
        """触发格子事件"""
        pass
    
    def __str__(self):
        return f"{self.type.value}: {self.name}"

class GameBoard:
    """游戏棋盘"""
    
    def __init__(self):
        self.squares = []
        self.total_squares = 24  # 财富流游戏通常有24个格子
        self._create_default_board()
    
    def _create_default_board(self):
        """创建默认的游戏棋盘"""
        # 导入具体的格子类
        from .squares import (StartSquare, PaycheckSquare, OpportunitySquare, 
                             DoodadSquare, MarketSquare, CharitySquare, 
                             DownsizedSquare, BabySquare)
        
        # 创建24个格子的循环棋盘
        square_configs = [
            (0, "起始点", StartSquare),
            (1, "发薪水", PaycheckSquare),
            (2, "机会", OpportunitySquare),
            (3, "意外支出", DoodadSquare),
            (4, "机会", OpportunitySquare),
            (5, "市场", MarketSquare),
            (6, "发薪水", PaycheckSquare),
            (7, "慈善", CharitySquare),
            (8, "机会", OpportunitySquare),
            (9, "意外支出", DoodadSquare),
            (10, "机会", OpportunitySquare),
            (11, "裁员", DownsizedSquare),
            (12, "发薪水", PaycheckSquare),
            (13, "机会", OpportunitySquare),
            (14, "生孩子", BabySquare),
            (15, "机会", OpportunitySquare),
            (16, "意外支出", DoodadSquare),
            (17, "市场", MarketSquare),
            (18, "发薪水", PaycheckSquare),
            (19, "机会", OpportunitySquare),
            (20, "慈善", CharitySquare),
            (21, "机会", OpportunitySquare),
            (22, "意外支出", DoodadSquare),
            (23, "机会", OpportunitySquare),
        ]
        
        for position, name, square_class in square_configs:
            square = square_class(name, position)
            self.squares.append(square)
    
    def get_square(self, position):
        """获取指定位置的格子"""
        if 0 <= position < len(self.squares):
            return self.squares[position]
        return None
    
    def get_next_position(self, current_position, steps):
        """计算移动后的位置"""
        return (current_position + steps) % len(self.squares)
    
    def get_squares_by_type(self, square_type):
        """获取指定类型的所有格子"""
        return [square for square in self.squares if square.type == square_type]
    
    def get_board_size(self):
        """获取棋盘大小"""
        return len(self.squares)
    
    def __str__(self):
        board_str = "游戏棋盘:\n"
        for i, square in enumerate(self.squares):
            board_str += f"  {i:2d}: {square}\n"
        return board_str 