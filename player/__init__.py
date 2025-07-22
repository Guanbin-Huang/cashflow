"""
财富流游戏玩家系统
包含玩家类和相关的资产、负债管理
"""

from .player import Player, Asset, Liability, FinancialAsset

__all__ = [
    'Player', 'Asset', 'Liability', 'FinancialAsset'
] 