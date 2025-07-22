"""
财富流游戏玩家系统 - Player Management System  
Player类用于模拟"穷爸爸富爸爸"财富流游戏中的玩家

文件功能概述：
==============
本文件实现了财富流游戏的核心玩家系统，包括玩家的财务管理、资产负债
系统、收支计算和财务自由判断。这是游戏中最重要的业务逻辑组件之一，
直接体现了富爸爸理念中的财务教育核心。

主要组件：
----------
1. Player类 - 玩家主体类
   - 基础属性管理（姓名、职业、工资等）
   - 财务状态跟踪（现金、被动收入、支出）
   - 资产负债组合管理
   - 收支操作和历史记录

2. Asset类 - 资产基础类
   - 资产基本属性定义
   - 被动收入计算
   - 资产类型分类管理

3. Liability类 - 负债基础类
   - 负债基本属性定义
   - 月支出影响计算

4. FinancialAsset类 - 金融资产专用类
   - 股票、基金等金融产品
   - 股数和股价管理
   - 股息收入计算

核心功能：
----------
- 玩家财务状态管理
  * 现金流量控制
  * 被动收入累积
  * 月支出管理
  * 财务自由判断逻辑

- 资产负债系统
  * 资产购买和持有
  * 负债借贷管理
  * 资产被动收入计算
  * 负债支出影响

- 玩家交互操作
  * 工资和被动收入收取
  * 月支出支付
  * 资产购买决策
  * 玩家间资产交易

- 财务记录系统
  * 收入历史跟踪
  * 财务操作记录
  * 状态变化监控

技术特点：
----------
- 面向对象的财务模型设计
- 完整的财务状态管理
- 灵活的资产负债架构
- 支持复杂的财务计算
- 可扩展的资产类型系统

财务教育理念：
--------------
- 现金流思维：重视被动收入vs支出的关系
- 资产负债区分：清晰区分增值资产和消费负债
- 财务自由目标：被动收入超过支出的终极目标
- 投资组合管理：多样化资产配置的重要性
- 风险收益平衡：不同资产类型的风险收益特征

游戏机制实现：
--------------
- 支持多种职业起始配置
- 动态的收支平衡计算
- 复杂的资产交易系统
- 真实的财务状况模拟
- 渐进式财富积累过程

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

class Player:
    """
    玩家类，适用于穷爸爸富爸爸的财富流游戏。
    """

    def __init__(self, name, profession, salary, cash=0, assets=None, liabilities=None, passive_income=0, expenses=0):
        """
        初始化玩家属性
        :param name: 玩家姓名
        :param profession: 职业
        :param salary: 工资收入
        :param cash: 现金
        :param assets: 资产列表
        :param liabilities: 负债列表
        :param passive_income: 被动收入
        :param expenses: 支出
        """
        self.name = name
        self.profession = profession
        self.salary = salary
        self.cash = cash
        self.assets = assets if assets is not None else []
        self.liabilities = liabilities if liabilities is not None else []
        self.passive_income = passive_income
        self.expenses = expenses
        self.income_history = []

    def add_asset(self, asset):
        """
        增加资产
        :param asset: 资产对象或描述
        """
        self.assets.append(asset)
        if hasattr(asset, 'passive_income'):
            self.passive_income += asset.passive_income

    def add_liability(self, liability):
        """
        增加负债
        :param liability: 负债对象或描述
        """
        self.liabilities.append(liability)
        if hasattr(liability, 'expense'):
            self.expenses += liability.expense

    def receive_salary(self):
        """
        收取工资
        """
        self.cash += self.salary
        self.income_history.append(('salary', self.salary))

    def receive_passive_income(self):
        """
        收取被动收入
        """
        self.cash += self.passive_income
        self.income_history.append(('passive_income', self.passive_income))

    def pay_expenses(self):
        """
        支付支出
        """
        self.cash -= self.expenses
        self.income_history.append(('expenses', -self.expenses))

    def buy_asset(self, asset, price):
        """
        购买资产
        :param asset: 资产对象或描述
        :param price: 价格
        """
        if self.cash >= price:
            self.cash -= price
            self.add_asset(asset)
            return True
        return False

    def take_loan(self, liability, amount):
        """
        贷款
        :param liability: 负债对象或描述
        :param amount: 金额
        """
        self.cash += amount
        self.add_liability(liability)

    def is_financially_free(self):
        """
        判断是否财务自由（被动收入 >= 支出）
        """
        return self.passive_income >= self.expenses

    def transfer_asset_to(self, other_player, asset, price):
        """
        将资产出售/转让给另一个玩家
        :param other_player: 另一个Player对象
        :param asset: 资产对象
        :param price: 交易价格
        :return: 是否交易成功
        """
        if asset in self.assets and other_player.cash >= price:
            self.assets.remove(asset)
            if hasattr(asset, 'passive_income'):
                self.passive_income -= asset.passive_income
            other_player.cash -= price
            self.cash += price
            other_player.add_asset(asset)
            return True
        return False

    def __str__(self):
        return (f"玩家: {self.name}, 职业: {self.profession}, 现金: {self.cash}, "
                f"工资: {self.salary}, 被动收入: {self.passive_income}, 支出: {self.expenses}, "
                f"资产数: {len(self.assets)}, 负债数: {len(self.liabilities)}")

class Asset:
    """资产类"""
    def __init__(self, name, asset_type, cost=0, passive_income=0):
        self.name = name
        self.type = asset_type  # 'real_estate', 'business', 'stocks', 'enterprise', etc.
        self.cost = cost
        self.passive_income = passive_income
    
    def __str__(self):
        return f"资产: {self.name} ({self.type}), 成本: {self.cost}, 被动收入: {self.passive_income}"

class Liability:
    """负债类"""
    def __init__(self, name, expense):
        self.name = name
        self.expense = expense  # 月支出
    
    def __str__(self):
        return f"负债: {self.name}, 月支出: {self.expense}"

class FinancialAsset(Asset):
    """金融资产类 - 用于股票、基金等"""
    def __init__(self, name, shares, price_per_share, dividend_per_share):
        total_cost = shares * price_per_share
        total_dividend = shares * dividend_per_share
        super().__init__(name, "financial", total_cost, total_dividend)
        self.shares = shares
        self.price_per_share = price_per_share
        self.dividend_per_share = dividend_per_share
    
    def __str__(self):
        return (f"金融资产: {self.name}, 股数: {self.shares}, "
                f"每股价格: {self.price_per_share}, 总股息: {self.passive_income}")

# 测试代码
if __name__ == "__main__":

    # 创建两个玩家
    p1 = Player("小明", "工程师", salary=5000, cash=10000, expenses=2000)
    p2 = Player("小红", "医生", salary=8000, cash=15000, expenses=3000)

    # 玩家1购买资产
    house = Asset("小公寓", "real_estate", cost=8000, passive_income=800)
    print(f"玩家1购买资产前: {p1}")
    p1.buy_asset(house, price=8000)
    print(f"玩家1购买资产后: {p1}")

    # 玩家2贷款并购买资产
    loan = Liability("房贷", expense=500)
    villa = Asset("别墅", "real_estate", cost=12000, passive_income=2000)
    p2.take_loan(loan, amount=5000)
    p2.buy_asset(villa, price=12000)
    print(f"玩家2贷款并购入资产后: {p2}")

    # 玩家1和玩家2进行资产交易
    print("\n玩家1将小公寓以7000元卖给玩家2")
    success = p1.transfer_asset_to(p2, house, price=7000)
    print("交易成功" if success else "交易失败")
    print(f"玩家1: {p1}")
    print(f"玩家2: {p2}")

    # 收取工资和被动收入，支付支出
    p1.receive_salary()
    p1.receive_passive_income()
    p1.pay_expenses()
    print(f"玩家1收支后: {p1}")

    p2.receive_salary()
    p2.receive_passive_income()
    p2.pay_expenses()
    print(f"玩家2收支后: {p2}")

    # 判断财务自由
    print(f"玩家1财务自由: {p1.is_financially_free()}")
    print(f"玩家2财务自由: {p2.is_financially_free()}")
