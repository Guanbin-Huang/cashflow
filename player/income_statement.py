"""
Income Statement (损益表) Module
Manages player income and expense tracking for the cash flow game
"""

class IncomeStatement:
    """Income Statement class for tracking player financial flows"""
    
    def __init__(self):
        # Initialize income structure
        self.income = {
            # Active Income (主动收入)
            "active_income": {
                "work_income": {
                    "personal_salary": {"cashflow": 0},
                    "spouse_salary": {"cashflow": 0}
                },
                "side_business_income": {}  # Will be populated with side business data
            },
            # Passive Income (被动收入)
            "passive_income": {
                "financial": {},        # Financial investments
                "real_estate": {},      # Real estate investments
                "enterprise": {}        # Enterprise investments
            }
        }
        
        # Initialize expense structure
        self.expenses = {
            "living_expenses": {
                "children": {
                    "count": 0,
                    "cost_per_child": 0,
                    "total_cost": 0
                },
                "personal": {"total_cost": 0},
                "spouse": {"total_cost": 0}
            },
            "taxes": {"total_cost": 0},
            "home_mortgage": {"total_cost": 0},
            "rent": {"total_cost": 0},
            "car_loan": {"total_cost": 0},
            "credit_card": {"total_cost": 0},
            "additional_debt": {"total_cost": 0},
            "insurance": {"total_cost": 0},
            "health": {"total_cost": 0},
            "bank_loan_interest": {"total_cost": 0}
        }
    
    def set_work_income(self, personal_salary=0, spouse_salary=0):
        """Set work income for personal and spouse"""
        self.income["active_income"]["work_income"]["personal_salary"]["cashflow"] = personal_salary
        self.income["active_income"]["work_income"]["spouse_salary"]["cashflow"] = spouse_salary
    
    def add_side_business(self, code, cashflow):
        """Add side business income"""
        self.income["active_income"]["side_business_income"][code] = {"cashflow": cashflow}
    
    def remove_side_business(self, code):
        """Remove side business income"""
        if code in self.income["active_income"]["side_business_income"]:
            del self.income["active_income"]["side_business_income"][code]
    
    def add_financial_investment(self, code, shares, cashflow):
        """Add financial investment income"""
        self.income["passive_income"]["financial"][code] = {
            "shares": shares,
            "cashflow": cashflow
        }
    
    def add_real_estate_investment(self, code, down_payment, cashflow):
        """Add real estate investment income"""
        self.income["passive_income"]["real_estate"][code] = {
            "down_payment": down_payment,
            "cashflow": cashflow
        }
    
    def add_enterprise_investment(self, code, down_payment, cashflow):
        """Add enterprise investment income"""
        self.income["passive_income"]["enterprise"][code] = {
            "down_payment": down_payment,
            "cashflow": cashflow
        }
    
    def set_living_expenses(self, children_count=0, cost_per_child=0, personal_cost=0, spouse_cost=0):
        """Set living expenses"""
        self.expenses["living_expenses"]["children"]["count"] = children_count
        self.expenses["living_expenses"]["children"]["cost_per_child"] = cost_per_child
        self.expenses["living_expenses"]["children"]["total_cost"] = children_count * cost_per_child
        self.expenses["living_expenses"]["personal"]["total_cost"] = personal_cost
        self.expenses["living_expenses"]["spouse"]["total_cost"] = spouse_cost
    
    def set_expense(self, expense_type, amount):
        """Set specific expense amount"""
        if expense_type in self.expenses:
            self.expenses[expense_type]["total_cost"] = amount
    
    def update_data(self, income_data=None, expense_data=None):
        """更新损益表数据 - 为了兼容player.py中的调用"""
        if income_data:
            # 更新收入数据
            for category, data in income_data.items():
                if category == "主动收入":
                    if "工作收入" in data:
                        work_income = data["工作收入"]
                        if "本人工资" in work_income:
                            personal_salary = work_income["本人工资"].get("现金流", 0)
                            self.set_work_income(personal_salary=personal_salary)
                elif category == "被动收入":
                    # 处理被动收入
                    pass
        
        if expense_data:
            # 更新支出数据
            for expense_type, amount in expense_data.items():
                if isinstance(amount, dict) and "total_cost" in amount:
                    self.set_expense(expense_type, amount["total_cost"])
                elif isinstance(amount, (int, float)):
                    self.set_expense(expense_type, amount)
    
    def get_data(self):
        """获取完整的损益表数据"""
        return {
            "收入": self.income,
            "支出": self.expenses,
            "总收入": self.get_total_income(),
            "总支出": self.get_total_expenses(),
            "月现金流": self.get_monthly_cashflow()
        }
    
    def print_summary(self):
        """打印损益表摘要"""
        print(f"总收入: {self.get_total_income():,}")
        print(f"总支出: {self.get_total_expenses():,}")
        print(f"月现金流: {self.get_monthly_cashflow():,}")

    def get_total_active_income(self):
        """Calculate total active income"""
        total = 0
        # Work income
        work_income = self.income["active_income"]["work_income"]
        total += work_income["personal_salary"]["cashflow"]
        total += work_income["spouse_salary"]["cashflow"]
        
        # Side business income  
        for business in self.income["active_income"]["side_business_income"].values():
            total += business["cashflow"]
        
        return total
    
    def get_total_passive_income(self):
        """Calculate total passive income"""
        total = 0
        
        # Financial investments
        for investment in self.income["passive_income"]["financial"].values():
            total += investment["cashflow"]
        
        # Real estate investments
        for investment in self.income["passive_income"]["real_estate"].values():
            total += investment["cashflow"]
        
        # Enterprise investments
        for investment in self.income["passive_income"]["enterprise"].values():
            total += investment["cashflow"]
        
        return total
    
    def get_total_income(self):
        """Calculate total income"""
        return self.get_total_active_income() + self.get_total_passive_income()
    
    def get_total_expenses(self):
        """Calculate total expenses"""
        total = 0
        
        # Living expenses
        living = self.expenses["living_expenses"]
        total += living["children"]["total_cost"]
        total += living["personal"]["total_cost"]
        total += living["spouse"]["total_cost"]
        
        # Other expenses
        for expense_type in ["taxes", "home_mortgage", "rent", "car_loan", 
                           "credit_card", "additional_debt", "insurance", 
                           "health", "bank_loan_interest"]:
            total += self.expenses[expense_type]["total_cost"]
        
        return total
    
    def get_monthly_cashflow(self):
        """Calculate monthly cash flow (income - expenses)"""
        return self.get_total_income() - self.get_total_expenses()
    
    def print_statement(self):
        """Print formatted income statement"""
        print("=== 损益表 (Income Statement) ===")
        print("\n收入 (Income):")
        
        # Active income
        print("  主动收入 (Active Income):")
        work_income = self.income["active_income"]["work_income"]
        print(f"    本人工资: {work_income['personal_salary']['cashflow']:,}元")
        print(f"    配偶工资: {work_income['spouse_salary']['cashflow']:,}元")
        
        if self.income["active_income"]["side_business_income"]:
            print("    副业收入:")
            for code, data in self.income["active_income"]["side_business_income"].items():
                print(f"      {code}: {data['cashflow']:,}元")
        
        # Passive income
        print("  被动收入 (Passive Income):")
        if self.income["passive_income"]["financial"]:
            print("    金融投资:")
            for code, data in self.income["passive_income"]["financial"].items():
                print(f"      {code} ({data['shares']}份): {data['cashflow']:,}元")
        
        if self.income["passive_income"]["real_estate"]:
            print("    房地产投资:")
            for code, data in self.income["passive_income"]["real_estate"].items():
                print(f"      {code}: {data['cashflow']:,}元")
        
        if self.income["passive_income"]["enterprise"]:
            print("    企业投资:")
            for code, data in self.income["passive_income"]["enterprise"].items():
                print(f"      {code}: {data['cashflow']:,}元")
        
        print(f"\n总收入: {self.get_total_income():,}元")
        
        # Expenses
        print("\n支出 (Expenses):")
        living = self.expenses["living_expenses"]
        print(f"  生活支出: {living['children']['total_cost'] + living['personal']['total_cost'] + living['spouse']['total_cost']:,}元")
        print(f"    孩子 ({living['children']['count']}个): {living['children']['total_cost']:,}元")
        print(f"    本人: {living['personal']['total_cost']:,}元")
        print(f"    配偶: {living['spouse']['total_cost']:,}元")
        
        for expense_type in ["taxes", "home_mortgage", "rent", "car_loan", 
                           "credit_card", "additional_debt", "insurance", 
                           "health", "bank_loan_interest"]:
            amount = self.expenses[expense_type]["total_cost"]
            if amount > 0:
                print(f"  {expense_type}: {amount:,}元")
        
        print(f"\n总支出: {self.get_total_expenses():,}元")
        print(f"月现金流: {self.get_monthly_cashflow():,}元")
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "income": self.income,
            "expenses": self.expenses
        }
    
    def from_dict(self, data):
        """Load from dictionary"""
        if "income" in data:
            self.income = data["income"]
        if "expenses" in data:
            self.expenses = data["expenses"]

if __name__ == "__main__":
    # Test the income statement
    statement = IncomeStatement()
    
    # Set work income
    statement.set_work_income(personal_salary=50000, spouse_salary=30000)
    
    # Add side business
    statement.add_side_business("摄影公司", 3500)
    
    # Add investments
    statement.add_financial_investment("股票基金", 10, 1000)
    statement.add_real_estate_investment("公寓A", 60000, 2500)
    statement.add_enterprise_investment("咖啡机", 50000, 22000)
    
    # Set expenses
    statement.set_living_expenses(children_count=2, cost_per_child=5000, 
                                personal_cost=15000, spouse_cost=12000)
    statement.set_expense("taxes", 8000)
    statement.set_expense("home_mortgage", 18000)
    
    # Print statement
    statement.print_statement()