"""
机会卡 - 一般投资机会
包括房地产、小型商业等投资机会
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