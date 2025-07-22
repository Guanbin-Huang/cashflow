"""
财富流游戏企业卡系统 - Enterprise Card System
企业投资机会卡片，高投入高回报的企业投资类型

文件功能概述：
==============
本文件实现了财富流游戏中的企业卡类型，代表了高风险高回报的企业投资
机会。企业卡通常需要更多的资金投入和管理经验，但能提供可观的被动收入
回报，是游戏中最具挑战性的投资选择。

主要组件：
----------
1. EnterpriseCard类 - 企业投资卡片
   - 继承自InvestmentCard投资卡基类
   - 包含员工数量和管理要求属性
   - 实现企业特有的购买和管理逻辑

核心功能：
----------
- 企业投资机会展示
  * 高额投资成本和首付要求
  * 显著的月现金流回报
  * 员工雇佣和管理需求
  * 复杂的运营要求

- 投资条件验证
  * 玩家资金充足性检查
  * 管理能力要求（可选）
  * 员工成本计算
  * 投资风险评估

- 企业资产管理
  * 创建企业资产对象
  * 计算净现金流收益
  * 考虑管理和员工成本
  * 资产添加到玩家投资组合

技术特点：
----------
- 继承投资卡通用功能
- 扩展企业特有属性和行为
- 复杂的成本效益计算
- 灵活的管理要求配置

投资特色：
----------
- 高投入门槛：通常需要较高的首付
- 高回报潜力：月现金流收益显著
- 管理复杂性：可能需要玩家投入时间管理
- 员工成本：需要考虑人员开支
- 规模效应：大型企业投资的典型特征

风险收益分析：
--------------
- 风险等级：高（资金需求大，管理复杂）
- 收益潜力：高（月现金流可观）
- 流动性：低（难以快速变现）
- 管理需求：高（可能需要持续关注）
- 适合人群：有经验的投资者和企业家

游戏教育价值：
--------------
- 体验企业投资的高风险高回报特征
- 理解规模经济和管理的重要性
- 学习评估复杂投资机会
- 培养企业家思维和投资决策能力

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

from .base import InvestmentCard, CardType
from player.player import Asset, Liability

class EnterpriseCard(InvestmentCard):
    """企业卡 - 通常需要更多资金，但回报更高"""
    
    def __init__(self, card_id, name, description, cost, down_payment, 
                 monthly_cash_flow, employee_count=0, management_required=False):
        super().__init__(card_id, name, CardType.ENTERPRISE, description,
                        cost, down_payment, monthly_cash_flow, True, cost - down_payment)
        self.employee_count = employee_count
        self.management_required = management_required
    
    def execute_purchase(self, player):
        """执行企业购买"""
        if not self.can_afford(player):
            return False, f"资金不足！需要 {self.down_payment} 现金，当前只有 {player.cash}"
        
        # 支付首付
        player.cash -= self.down_payment
        
        # 如果需要贷款，添加贷款负债
        if self.cost > self.down_payment:
            loan_amount = self.cost - self.down_payment
            monthly_payment = loan_amount * 0.1 / 12  # 假设年利率10%
            liability = Liability(f"{self.name}贷款", monthly_payment)
            player.add_liability(liability)
        
        # 添加企业资产
        asset = Asset(self.name, "enterprise", self.cost, self.monthly_cash_flow)
        player.add_asset(asset)
        
        return True, f"成功购买企业: {self.name}"
    
    def get_info(self):
        """获取企业详细信息"""
        info = {
            'name': self.name,
            'type': self.type.value,
            'description': self.description,
            'cost': self.cost,
            'down_payment': self.down_payment,
            'monthly_cash_flow': self.monthly_cash_flow,
            'employee_count': self.employee_count,
            'management_required': self.management_required,
            'loan_amount': self.get_loan_amount()
        }
        return info
    
    def __str__(self):
        base_str = super().__str__()
        additional = f", 员工数: {self.employee_count}"
        if self.management_required:
            additional += ", 需要管理"
        return base_str + additional 