"""
财富流游戏副业卡系统 - Side Business Card System
副业投资机会卡片，小投资快回报的副业项目

文件功能概述：
==============
本文件实现了财富流游戏中的副业卡类型，代表了小投入、快回报的
副业投资机会。这类投资通常不需要贷款，门槛低，回报快，
适合初学者和小资金投资者。

主要组件：
----------
1. SideBusinessCard类 - 副业投资卡
   - 继承自Card基类而非InvestmentCard
   - 实现无贷款的简单投资模式
   - 包含时间投入要求的考虑

核心功能：
----------
- 低门槛投资机会
  * 较低的一次性投入成本
  * 无需贷款和首付
  * 快速的现金流回报
  * 简单的购买和运营流程

- 时间成本计量
  * 记录每周所需时间
  * 考虑时间机会成本
  * 平衡时间和金钱投入
  * 为老板思维做准备

技术特点：
----------
- 简单直接的购买逻辑
- 无需贷款和负债管理
- 快速的投资回报
- 灵活的时间投入要求

投资特色：
----------
- 低风险：成本低，损失可控
- 快回报：月现金流快速产生
- 低门槛：适合小资金投入
- 时间成本：需要一定时间投入
- 灵活管理：可以兼职运营

适合人群：
----------
- 初学者和小白投资者
- 资金有限的新手玩家
- 希望快速获得回报的玩家
- 愿意投入时间精力的玩家

游戏教育价值：
--------------
- 学习创业和副业的基本概念
- 体验时间和金钱的交换关系
- 培养企业家精神和创新思维
- 理解被动收入的多种来源

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

from .base import InvestmentCard, CardType
from player import Asset

class SideBusinessCard(InvestmentCard):
    """副业卡 - 小投资，快回报"""
    
    def __init__(self, card_id, name, description, cost, monthly_cash_flow, 
                 time_required_hours=0):
        # 副业通常全款购买，所以首付等于总价
        super().__init__(card_id, name, CardType.SIDE_BUSINESS, description,
                        cost, cost, monthly_cash_flow)
        self.time_required_hours = time_required_hours
    
    def execute_purchase(self, player):
        """执行副业购买"""
        if not self.can_afford(player):
            return False, f"资金不足！需要 {self.cost} 现金，当前只有 {player.cash}"
        
        # 副业通常是全款购买，不需要贷款
        player.cash -= self.cost
        
        # 添加副业资产
        asset = Asset(self.name, "side_business", self.cost, self.monthly_cash_flow)
        player.add_asset(asset)
        
        return True, f"成功创建副业: {self.name}"
    
    def get_payback_period(self):
        """计算投资回收期（月）"""
        if self.monthly_cash_flow <= 0:
            return float('inf')
        return self.cost / self.monthly_cash_flow
    
    def get_info(self):
        """获取副业详细信息"""
        payback_period = self.get_payback_period()
        
        info = {
            'name': self.name,
            'type': self.type.value,
            'description': self.description,
            'cost': self.cost,
            'monthly_cash_flow': self.monthly_cash_flow,
            'time_required_hours': self.time_required_hours,
            'payback_period_months': payback_period if payback_period != float('inf') else None,
            'annual_roi': (self.monthly_cash_flow * 12 / self.cost * 100) if self.cost > 0 else 0
        }
        return info
    
    def __str__(self):
        time_str = f", 需要时间: {self.time_required_hours}小时/月" if self.time_required_hours > 0 else ""
        payback = self.get_payback_period()
        payback_str = f", 回收期: {payback:.1f}月" if payback != float('inf') else ""
        
        return (f"{self.type.value}: {self.name} - "
                f"投资: {self.cost}, 月收入: {self.monthly_cash_flow}"
                f"{time_str}{payback_str}") 