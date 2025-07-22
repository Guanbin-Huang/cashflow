# Player类用于模拟“穷爸爸富爸爸”财富流游戏中的玩家。玩家可以拥有现金、资产、负债、工资、被动收入和支出。
# 该类支持添加资产和负债、收取工资和被动收入、支付支出、购买资产、贷款等操作，并可判断玩家是否财务自由。
# 玩家之间可以通过资产买卖等方式进行交互。

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
