"""
副业卡 - 副业投资机会
小投资，快回报，通常不需要贷款
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