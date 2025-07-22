"""
财富流游戏金融卡系统 - Financial Card System
金融产品投资卡片，包括股票、基金、债券等投资产品

文件功能概述：
==============
本文件实现了财富流游戏中的金融卡类型，代表了股票、基金、债券等
金融产品投资机会。金融卡的特点是按股数购买，灵活性高，适合不同
资金规模的投资者。

主要组件：
----------
1. FinancialCard类 - 金融产品投资卡
   - 继承自Card基类而非InvestmentCard
   - 按股数计价的灵活投资方式
   - 支持最小和最大股数限制

核心功能：
----------
- 股数化投资机制
  * 玩家可选择购买股数
  * 灵活的投资金额控制
  * 最小和最大股数限制
  * 实时成本和收益计算

- 金融资产管理
  * 创建金融资产对象
  * 股息收入计算
  * 支持部分卖出机制
  * 投资组合多元化

技术特点：
----------
- 独特的按股数购买机制
- 灵活的投资金额控制
- 复杂的股息收益计算
- 支持动态参数配置

投资特色：
----------
- 低门槛准入：可以少量购买
- 高流动性：可随时买入卖出
- 分散风险：支持组合投资
- 稳定收益：通过股息获得被动收入
- 投资灵活：适合各种资金规模

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

from .base import Card, CardType
from player import FinancialAsset

class FinancialCard(Card):
    """金融卡 - 股票、基金等金融产品"""
    
    def __init__(self, card_id, name, description, price_per_share, 
                 dividend_per_share, min_shares=1, max_shares=1000):
        super().__init__(card_id, name, CardType.FINANCIAL, description)
        self.price_per_share = price_per_share
        self.dividend_per_share = dividend_per_share
        self.min_shares = min_shares
        self.max_shares = max_shares
    
    def can_afford(self, player, shares=None):
        """检查玩家是否能买得起指定股数"""
        shares = shares or self.min_shares
        return player.cash >= (self.price_per_share * shares)
    
    def get_required_cash(self, shares=None):
        """获取购买指定股数所需现金"""
        shares = shares or self.min_shares
        return self.price_per_share * shares
    
    def execute_purchase(self, player, shares=None):
        """执行金融产品购买"""
        shares = shares or self.min_shares
        
        if shares < self.min_shares:
            return False, f"最少需要购买 {self.min_shares} 股"
        
        if shares > self.max_shares:
            return False, f"最多只能购买 {self.max_shares} 股"
        
        total_cost = self.price_per_share * shares
        if player.cash < total_cost:
            return False, f"资金不足！需要 {total_cost} 现金，当前只有 {player.cash}"
        
        # 执行购买
        player.cash -= total_cost
        
        # 创建金融资产
        financial_asset = FinancialAsset(
            self.name, 
            shares, 
            self.price_per_share, 
            self.dividend_per_share
        )
        player.add_asset(financial_asset)
        
        return True, f"成功购买 {shares} 股 {self.name}，总计 {total_cost} 元"
    
    def calculate_max_affordable_shares(self, player):
        """计算玩家最多能买得起多少股"""
        if self.price_per_share <= 0:
            return 0
        max_affordable = int(player.cash // self.price_per_share)
        return min(max_affordable, self.max_shares)
    
    def get_info(self, shares=None):
        """获取金融产品详细信息"""
        shares = shares or self.min_shares
        total_cost = self.price_per_share * shares
        total_dividend = self.dividend_per_share * shares
        
        info = {
            'name': self.name,
            'type': self.type.value,
            'description': self.description,
            'price_per_share': self.price_per_share,
            'dividend_per_share': self.dividend_per_share,
            'min_shares': self.min_shares,
            'max_shares': self.max_shares,
            'example_shares': shares,
            'example_total_cost': total_cost,
            'example_monthly_dividend': total_dividend,
            'dividend_yield': (self.dividend_per_share / self.price_per_share * 100) if self.price_per_share > 0 else 0
        }
        return info
    
    def __str__(self):
        return (f"{self.type.value}: {self.name} - "
                f"每股价格: {self.price_per_share}, 每股股息: {self.dividend_per_share}, "
                f"购买范围: {self.min_shares}-{self.max_shares}股") 