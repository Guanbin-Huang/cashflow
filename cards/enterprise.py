"""
企业卡 - 企业投资机会
通常需要更多资金投入，但回报也更高
可能需要管理和雇员
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