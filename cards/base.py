"""
财富流游戏卡片系统基础类 - Card System Foundation
定义了所有卡片的基本结构和行为接口

文件功能概述：
==============
本文件定义了财富流游戏卡片系统的基础架构，包括所有卡片类型的枚举、
抽象基类和通用投资卡片基类。这是整个卡片系统的核心基础，为不同类型
的投资机会卡片提供了统一的接口和行为规范。

主要组件：
----------
1. CardType枚举 - 定义所有卡片类型
   - ENTERPRISE: 企业卡，高投入高回报的企业投资
   - OPPORTUNITY: 机会卡，一般投资机会如房地产
   - FINANCIAL: 金融卡，股票、基金等金融产品
   - SIDE_BUSINESS: 副业卡，小投入快回报的副业

2. Card抽象基类 - 所有卡片的基础接口
   - 定义卡片基本属性（ID、名称、类型、描述）
   - 抽象方法确保子类实现必要功能
   - 统一的卡片行为接口

3. InvestmentCard类 - 投资类卡片基类
   - 继承自Card，专门用于投资机会
   - 包含成本、首付、月现金流等财务属性
   - 提供贷款需求和购买能力判断

核心功能：
----------
- 卡片类型分类管理
- 统一的卡片接口定义
- 投资成本和收益计算
- 玩家购买能力验证
- 贷款金额计算
- 卡片信息格式化显示

技术特点：
----------
- 抽象基类确保接口一致性
- 枚举类型提供类型安全
- 面向对象的设计模式
- 可扩展的卡片类型系统
- 清晰的职责分离

投资卡片设计理念：
------------------
- 企业卡：高风险高回报，需要管理能力
- 机会卡：中等风险收益，传统投资方式
- 金融卡：灵活投资，按股数购买
- 副业卡：低门槛快回报，适合起步

财务模型：
----------
- 总成本 = 首付 + 贷款金额
- 月现金流 = 被动收入 - 贷款利息
- 购买门槛 = 首付金额
- ROI计算 = 月现金流 / 首付金额

扩展指南：
----------
- 新增卡片类型：扩展CardType枚举
- 新增卡片类：继承Card或InvestmentCard
- 重写抽象方法：can_afford, execute_purchase, get_required_cash
- 实现特定逻辑：根据卡片类型特点定制

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
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