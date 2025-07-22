"""
卡片系统基础类
定义了所有卡片的基本结构和行为
"""

from abc import ABC, abstractmethod
from enum import Enum

class CardType(Enum):
    """卡片类型枚举"""
    ENTERPRISE = "企业卡"      # 企业投资机会
    OPPORTUNITY = "机会卡"     # 一般投资机会
    FINANCIAL = "金融卡"       # 金融产品
    SIDE_BUSINESS = "副业卡"   # 副业机会

class Card(ABC):
    """卡片基类"""
    def __init__(self, card_id, name, card_type, description):
        self.card_id = card_id
        self.name = name
        self.type = card_type
        self.description = description
    
    @abstractmethod
    def can_afford(self, player):
        """玩家是否买得起"""
        pass
    
    @abstractmethod
    def execute_purchase(self, player):
        """执行购买"""
        pass
    
    @abstractmethod
    def get_required_cash(self):
        """获取所需现金"""
        pass
    
    def __str__(self):
        return f"{self.type.value}: {self.name}"
    
    def __repr__(self):
        return f"Card(id={self.card_id}, name='{self.name}', type={self.type.value})"

class InvestmentCard(Card):
    """投资类卡片基类"""
    def __init__(self, card_id, name, card_type, description, 
                 cost, down_payment, monthly_cash_flow, 
                 requires_loan=False, loan_amount=0):
        super().__init__(card_id, name, card_type, description)
        self.cost = cost                    # 总价
        self.down_payment = down_payment    # 首付
        self.monthly_cash_flow = monthly_cash_flow  # 月现金流
        self.requires_loan = requires_loan  # 是否需要贷款
        self.loan_amount = loan_amount      # 贷款金额
    
    def can_afford(self, player):
        """检查玩家是否有足够现金支付首付"""
        return player.cash >= self.down_payment
    
    def get_required_cash(self):
        """获取所需现金（首付金额）"""
        return self.down_payment
    
    def get_loan_amount(self):
        """获取贷款金额"""
        return self.cost - self.down_payment if self.cost > self.down_payment else 0
    
    def __str__(self):
        return (f"{self.type.value}: {self.name} - "
                f"总价: {self.cost}, 首付: {self.down_payment}, "
                f"月现金流: {self.monthly_cash_flow}") 