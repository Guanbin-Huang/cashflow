"""
财富流游戏机会卡系统 - Opportunity Card System
一般投资机会卡片，包括房地产、小型商业等投资机会

文件功能概述：
==============
本文件实现了财富流游戏中的机会卡类型，代表了各种传统的投资
机会，如房地产投资、小型商业等。这些投资机会通常风险适中，
回报稳定，是游戏中主流的投资选择。

主要组件：
----------
1. OpportunityCard类 - 一般投资机会卡
   - 继承自InvestmentCard投资卡基类
   - 实现标准的投资购买和管理逻辑
   - 支持首付+贷款的传统投资模式

核心功能：
----------
- 传统投资机会展示
  * 中等规模的投资成本
  * 合理的首付比例
  * 稳定的月现金流回报
  * 无复杂的管理要求

- 标准购买流程
  * 支付首付金额
  * 创建相应的贷款负债
  * 添加投资资产到组合
  * 计算净现金流收益

技术特点：
----------
- 继承投资卡通用功能
- 标准化的投资流程
- 简单明了的购买逻辑
- 无额外复杂性要求

投资特色：
----------
- 中等风险：相对企业卡风险较低
- 稳定收益：月现金流可预期
- 适中门槛：首付要求合理
- 无管理需求：不需要额外精力投入
- 传统投资：符合一般投资者习惯

适合人群：
----------
- 中等收入水平的投资者
- 偏好稳健投资的玩家
- 初学者和中级投资者
- 寻求被动收入的玩家

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

from .base import InvestmentCard, CardType
from player import Asset, Liability

class OpportunityCard(InvestmentCard):
    """机会卡 - 各种投资机会"""
    
    def __init__(self, card_id, name, description, cost, down_payment, monthly_cash_flow):
        super().__init__(card_id, name, CardType.OPPORTUNITY, description,
                        cost, down_payment, monthly_cash_flow)
    
    def execute_purchase(self, player):
        """执行机会购买"""
        if not self.can_afford(player):
            return False, f"资金不足！需要 {self.down_payment} 现金，当前只有 {player.cash}"
        
        # 支付首付
        player.cash -= self.down_payment
        
        # 如果需要贷款，添加贷款负债
        if self.cost > self.down_payment:
            loan_amount = self.cost - self.down_payment
            monthly_payment = loan_amount * 0.08 / 12  # 假设年利率8%
            liability = Liability(f"{self.name}贷款", monthly_payment)
            player.add_liability(liability)
        
        # 添加机会资产
        asset = Asset(self.name, "opportunity", self.cost, self.monthly_cash_flow)
        player.add_asset(asset)
        
        return True, f"成功购买投资机会: {self.name}"
    
    def get_info(self):
        """获取机会详细信息"""
        info = {
            'name': self.name,
            'type': self.type.value,
            'description': self.description,
            'cost': self.cost,
            'down_payment': self.down_payment,
            'monthly_cash_flow': self.monthly_cash_flow,
            'loan_amount': self.get_loan_amount(),
            'roi': (self.monthly_cash_flow * 12 / self.cost * 100) if self.cost > 0 else 0  # 年化收益率
        }
        return info 