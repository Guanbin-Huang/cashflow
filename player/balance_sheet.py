"""
Balance Sheet (资产负债表) Module
Manages player assets and liabilities tracking for the cash flow game
"""

class BalanceSheet:
    """Balance Sheet class for tracking player assets and liabilities"""
    
    def __init__(self):
        # Initialize assets structure
        self.assets = {
            # Awareness investments (觉察投资)
            "awareness_investments": {},
            
            # Bank deposits (银行存款)
            "bank_deposits": {"amount": 0},
            
            # Stock investments (股票投资)
            "stock_investments": {},
            
            # Real estate investments (房地产投资)
            "real_estate_investments": {},
            
            # Enterprise investments (企业投资)
            "enterprise_investments": {}
        }
        
        # Initialize liabilities structure
        self.liabilities = {
            # Home mortgage (自住房抵押贷款)
            "home_mortgage": {"amount": 0},
            
            # Car loan (购车贷款)
            "car_loan": {"amount": 0},
            
            # Credit card debt (信用卡负债)
            "credit_card_debt": {"amount": 0},
            
            # Additional debt (额外负债)
            "additional_debt": {"amount": 0},
            
            # Real estate mortgages (房产抵押贷款)
            "real_estate_mortgages": {},
            
            # Enterprise debts (企业负债)
            "enterprise_debts": {},
            
            # Bank loans (银行贷款)
            "bank_loans": {"amount": 0}
        }
    
    def add_awareness_investment(self, name, equity):
        """Add awareness investment"""
        self.assets["awareness_investments"][name] = {"equity": equity}
    
    def remove_awareness_investment(self, name):
        """Remove awareness investment"""
        if name in self.assets["awareness_investments"]:
            del self.assets["awareness_investments"][name]
    
    def update_data(self, asset_data=None, liability_data=None):
        """更新资产负债表数据 - 为了兼容player.py中的调用"""
        if asset_data:
            # 更新资产数据
            for asset_type, data in asset_data.items():
                if asset_type == "银行存款":
                    if isinstance(data, dict) and "金额" in data:
                        self.set_bank_deposits(data["金额"])
                    elif isinstance(data, (int, float)):
                        self.set_bank_deposits(data)
                elif asset_type in ["股票投资", "房地产投资", "企业投资"]:
                    # 处理投资类资产
                    pass
        
        if liability_data:
            # 更新负债数据
            for liability_type, data in liability_data.items():
                if isinstance(data, dict) and "金额" in data:
                    amount = data["金额"]
                    if liability_type == "自住房抵押贷款":
                        self.set_home_mortgage(amount)
                    elif liability_type == "购车贷款":
                        self.set_car_loan(amount)
                    elif liability_type == "信用卡负债":
                        self.set_credit_card_debt(amount)
    
    def get_data(self):
        """获取完整的资产负债表数据"""
        return {
            "资产": self.assets,
            "负债": self.liabilities,
            "总资产": self.get_total_assets(),
            "总负债": self.get_total_liabilities(),
            "净资产": self.get_net_worth()
        }
    
    def print_summary(self):
        """打印资产负债表摘要"""
        print(f"总资产: {self.get_total_assets():,}")
        print(f"总负债: {self.get_total_liabilities():,}")
        print(f"净资产: {self.get_net_worth():,}")

    def set_bank_deposits(self, amount):
        """Set bank deposit amount"""
        self.assets["bank_deposits"]["amount"] = amount
    
    def add_stock_investment(self, code, cost_per_share, shares):
        """Add stock investment"""
        self.assets["stock_investments"][code] = {
            "cost_per_share": cost_per_share,
            "shares": shares,
            "total_value": cost_per_share * shares
        }
    
    def remove_stock_investment(self, code):
        """Remove stock investment"""
        if code in self.assets["stock_investments"]:
            del self.assets["stock_investments"][code]
    
    def add_real_estate_investment(self, code, equity):
        """Add real estate investment asset"""
        self.assets["real_estate_investments"][code] = {"equity": equity}
    
    def add_real_estate_mortgage(self, code, amount):
        """Add real estate mortgage liability"""
        self.liabilities["real_estate_mortgages"][code] = {"amount": amount}
    
    def add_enterprise_investment(self, code, equity):
        """Add enterprise investment asset"""
        self.assets["enterprise_investments"][code] = {"equity": equity}
    
    def add_enterprise_debt(self, code, amount):
        """Add enterprise debt liability"""
        self.liabilities["enterprise_debts"][code] = {"amount": amount}
    
    def set_liability(self, liability_type, amount):
        """Set specific liability amount"""
        if liability_type in self.liabilities:
            self.liabilities[liability_type]["amount"] = amount
    
    def get_total_assets(self):
        """Calculate total assets"""
        total = 0
        
        # Awareness investments
        for investment in self.assets["awareness_investments"].values():
            total += investment["equity"]
        
        # Bank deposits
        total += self.assets["bank_deposits"]["amount"]
        
        # Stock investments
        for stock in self.assets["stock_investments"].values():
            total += stock["total_value"]
        
        # Real estate investments
        for investment in self.assets["real_estate_investments"].values():
            total += investment["equity"]
        
        # Enterprise investments
        for investment in self.assets["enterprise_investments"].values():
            total += investment["equity"]
        
        return total
    
    def get_total_liabilities(self):
        """Calculate total liabilities"""
        total = 0
        
        # Fixed liabilities
        for liability_type in ["home_mortgage", "car_loan", "credit_card_debt", 
                             "additional_debt", "bank_loans"]:
            total += self.liabilities[liability_type]["amount"]
        
        # Real estate mortgages
        for mortgage in self.liabilities["real_estate_mortgages"].values():
            total += mortgage["amount"]
        
        # Enterprise debts
        for debt in self.liabilities["enterprise_debts"].values():
            total += debt["amount"]
        
        return total
    
    def get_net_worth(self):
        """Calculate net worth (assets - liabilities)"""
        return self.get_total_assets() - self.get_total_liabilities()
    
    def print_statement(self):
        """Print formatted balance sheet"""
        print("=== 资产负债表 (Balance Sheet) ===")
        
        # Assets
        print("\n资产 (Assets):")
        
        if self.assets["awareness_investments"]:
            print("  觉察投资:")
            for name, data in self.assets["awareness_investments"].items():
                print(f"    {name}: {data['equity']:,}元")
        
        bank_amount = self.assets["bank_deposits"]["amount"]
        if bank_amount > 0:
            print(f"  银行存款: {bank_amount:,}元")
        
        if self.assets["stock_investments"]:
            print("  股票投资:")
            for code, data in self.assets["stock_investments"].items():
                print(f"    {code}: {data['shares']:,}股 @ {data['cost_per_share']:,}元 = {data['total_value']:,}元")
        
        if self.assets["real_estate_investments"]:
            print("  房地产投资:")
            for code, data in self.assets["real_estate_investments"].items():
                print(f"    {code}: {data['equity']:,}元")
        
        if self.assets["enterprise_investments"]:
            print("  企业投资:")
            for code, data in self.assets["enterprise_investments"].items():
                print(f"    {code}: {data['equity']:,}元")
        
        print(f"\n总资产: {self.get_total_assets():,}元")
        
        # Liabilities
        print("\n负债 (Liabilities):")
        
        for liability_type, chinese_name in [
            ("home_mortgage", "自住房抵押贷款"),
            ("car_loan", "购车贷款"),
            ("credit_card_debt", "信用卡负债"),
            ("additional_debt", "额外负债"),
            ("bank_loans", "银行贷款")
        ]:
            amount = self.liabilities[liability_type]["amount"]
            if amount > 0:
                print(f"  {chinese_name}: {amount:,}元")
        
        if self.liabilities["real_estate_mortgages"]:
            print("  房产抵押贷款:")
            for code, data in self.liabilities["real_estate_mortgages"].items():
                print(f"    {code}: {data['amount']:,}元")
        
        if self.liabilities["enterprise_debts"]:
            print("  企业负债:")
            for code, data in self.liabilities["enterprise_debts"].items():
                print(f"    {code}: {data['amount']:,}元")
        
        total_liabilities = self.get_total_liabilities()
        net_worth = self.get_net_worth()
        
        print(f"\n总负债: {total_liabilities:,}元")
        print(f"净资产: {net_worth:,}元")
    
    def get_debt_to_asset_ratio(self):
        """Calculate debt to asset ratio"""
        total_assets = self.get_total_assets()
        if total_assets == 0:
            return 0
        return self.get_total_liabilities() / total_assets
    
    def get_investment_breakdown(self):
        """Get breakdown of investments by type"""
        breakdown = {}
        total_assets = self.get_total_assets()
        
        if total_assets == 0:
            return breakdown
        
        # Calculate percentages
        awareness_total = sum(inv["equity"] for inv in self.assets["awareness_investments"].values())
        stock_total = sum(stock["total_value"] for stock in self.assets["stock_investments"].values())
        real_estate_total = sum(inv["equity"] for inv in self.assets["real_estate_investments"].values())
        enterprise_total = sum(inv["equity"] for inv in self.assets["enterprise_investments"].values())
        cash_total = self.assets["bank_deposits"]["amount"]
        
        breakdown = {
            "觉察投资": (awareness_total, awareness_total / total_assets * 100),
            "股票投资": (stock_total, stock_total / total_assets * 100),
            "房地产投资": (real_estate_total, real_estate_total / total_assets * 100),
            "企业投资": (enterprise_total, enterprise_total / total_assets * 100),
            "现金": (cash_total, cash_total / total_assets * 100)
        }
        
        return breakdown
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "assets": self.assets,
            "liabilities": self.liabilities
        }
    
    def from_dict(self, data):
        """Load from dictionary"""
        if "assets" in data:
            self.assets = data["assets"]
        if "liabilities" in data:
            self.liabilities = data["liabilities"]

if __name__ == "__main__":
    # Test the balance sheet
    balance_sheet = BalanceSheet()
    
    # Add assets
    balance_sheet.add_awareness_investment("觉察投资1", 100000)
    balance_sheet.set_bank_deposits(50000)
    balance_sheet.add_stock_investment("科技股", 30, 1000)
    balance_sheet.add_real_estate_investment("公寓A", 120000)
    balance_sheet.add_enterprise_investment("咖啡机", 100000)
    
    # Add liabilities
    balance_sheet.set_liability("home_mortgage", 300000)
    balance_sheet.set_liability("car_loan", 50000)
    balance_sheet.add_real_estate_mortgage("公寓A", 60000)
    
    # Print balance sheet
    balance_sheet.print_statement()
    
    # Print analysis
    print(f"\n=== 财务分析 ===")
    print(f"负债率: {balance_sheet.get_debt_to_asset_ratio():.1%}")
    
    print(f"\n投资组合分析:")
    breakdown = balance_sheet.get_investment_breakdown()
    for category, (amount, percentage) in breakdown.items():
        if amount > 0:
            print(f"  {category}: {amount:,}元 ({percentage:.1f}%)")