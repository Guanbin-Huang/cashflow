"""
金融卡片系统
处理金融卡片数据和对玩家财务表的影响
整合同事的详细实现到标准化架构
"""

import csv
import os
import re
from .base import Card, CardType

class FinancialCard(Card):
    """金融卡片类"""
    
    def __init__(self, card_id, name, description, price_per_share, dividend_per_share, min_shares=1, max_shares=1000):
        # 调用父类构造器
        super().__init__(card_id, name, CardType.FINANCIAL, description)
        
        # 金融产品属性
        self.price_per_share = price_per_share
        self.dividend_per_share = dividend_per_share
        self.min_shares = min_shares
        self.max_shares = max_shares
        
        # 为了向后兼容，保留同事的实现
        self.card_type = name  # 使用名称作为类型
        self.trading_permission = "所有玩家可买"  # 默认权限
        self.core_params = f"{min_shares} 股起，¥{price_per_share} / 股，每股收益 ±{dividend_per_share}"
        self.energy_change = -1  # 默认精力消耗
        
        # 解析核心参数
        self.parsed_params = self._parse_core_params()
    
    def _parse_core_params(self):
        """解析核心参数"""
        return {
            "min_shares": self.min_shares,
            "price_per_share": self.price_per_share,
            "income_per_share": self.dividend_per_share
        }
    
    def __str__(self):
        return (f"金融卡片: {self.name} ({self.card_type})\n"
                f"参数: {self.core_params}\n"
                f"精力变化: {self.energy_change}")
    
    def can_afford(self, player):
        """检查玩家是否有足够现金购买最少股数"""
        min_cost = self.min_shares * self.price_per_share
        return player.cash >= min_cost
    
    def execute_purchase(self, player, shares=None):
        """执行购买"""
        if shares is None:
            shares = self.min_shares
        
        shares = max(self.min_shares, min(shares, self.max_shares))
        cost = shares * self.price_per_share
        
        if player.cash >= cost:
            player.cash -= cost
            # 可以在这里添加股票到玩家的资产
            return True
        return False
    
    def get_required_cash(self):
        """获取所需最少现金"""
        return self.min_shares * self.price_per_share
    
    def get_investment_data(self, amount=None):
        """获取用于损益表的投资数据"""
        if amount is None:
            amount = self.min_shares
            
        data = {
            "代码": self.name,
            "份数": amount,
            "现金流": amount * self.dividend_per_share
        }
        return data

class FinancialCardManager:
    """金融卡片管理器"""
    
    def __init__(self, csv_file_path=None):
        self.cards = []
        if csv_file_path:
            self.load_cards_from_csv(csv_file_path)
    
    def load_cards_from_csv(self, csv_file_path):
        """从CSV文件加载金融卡片"""
        self.cards = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    energy_change = int(row['精力变化'])
                    
                    card = FinancialCard(
                        card_type=row['类型'],
                        name=row['名称'],
                        trading_permission=row['交易权限'],
                        core_params=row['核心参数'],
                        energy_change=energy_change
                    )
                    
                    self.cards.append(card)
                    
        except FileNotFoundError:
            print(f"警告: 找不到文件 {csv_file_path}")
        except Exception as e:
            print(f"加载金融卡片时出错: {e}")
    
    def get_cards_by_type(self, card_type):
        """根据类型获取卡片"""
        return [card for card in self.cards if card.card_type == card_type]
    
    def get_safe_investments(self):
        """获取安全投资类产品"""
        safe_types = ["基金", "存款", "理财", "保险"]
        return [card for card in self.cards if card.card_type in safe_types]
    
    def get_high_risk_investments(self):
        """获取高风险投资类产品"""
        risky_types = ["股票", "外汇", "黄金"]
        return [card for card in self.cards if card.card_type in risky_types]
    
    def filter_affordable_cards(self, player_cash):
        """筛选玩家能负担得起的卡片"""
        affordable_cards = []
        for i, card in enumerate(self.cards):
            if hasattr(card, 'can_afford'):
                # 创建一个临时对象来测试购买能力
                class TempPlayer:
                    def __init__(self, cash):
                        self.cash = cash
                temp_player = TempPlayer(player_cash)
                if card.can_afford(temp_player):
                    affordable_cards.append((i, card))
        return affordable_cards
    
    def get_cards_count(self):
        """获取卡片总数"""
        return len(self.cards)
    
    def print_cards_by_type(self):
        """按类型打印卡片"""
        card_types = set(card.card_type for card in self.cards)
        
        for card_type in sorted(card_types):
            print(f"\n=== {card_type}类产品 ===")
            type_cards = self.get_cards_by_type(card_type)
            for i, card in enumerate(type_cards):
                print(f"{i+1}. {card.name}: {card.core_params}")

class FinancialAsset:
    """金融资产类 - 用于股票、基金等"""
    def __init__(self, name, shares, price_per_share, dividend_per_share):
        self.name = name
        self.shares = shares
        self.price_per_share = price_per_share
        self.dividend_per_share = dividend_per_share
        self.total_cost = shares * price_per_share
        self.total_dividend = shares * dividend_per_share
    
    def __str__(self):
        return (f"金融资产: {self.name}, 股数: {self.shares}, "
                f"每股价格: {self.price_per_share}, 总股息: {self.total_dividend}")

# 默认加载金融卡片
def load_default_financial_cards():
    """加载默认的金融卡片"""
    # 尝试从数据目录加载
    data_path = "data/cards/金融卡片.csv"
    if os.path.exists(data_path):
        return FinancialCardManager(data_path)
    
    print("警告: 未找到金融卡片CSV文件，使用示例数据")
    manager = FinancialCardManager()
    
    # 添加示例卡片
    example_cards = [
        FinancialCard("FIN001", "K01 科技公司", "科技股票投资", 30, 5, 10, 1000),
        FinancialCard("FIN002", "Z01 股票型基金", "股票型基金投资", 5000, 100, 1, 100),
        FinancialCard("FIN003", "银行存款 MO2", "银行存款产品", 10000, 100, 1, 10)
    ]
    
    manager.cards = example_cards
    return manager

if __name__ == "__main__":
    # 测试金融卡片系统
    print("=== 金融卡片系统测试 ===")
    
    card_manager = load_default_financial_cards()
    print(f"成功加载 {card_manager.get_cards_count()} 张金融卡片")
    
    # 按类型显示卡片
    card_manager.print_cards_by_type()
    
    # 测试安全投资
    print(f"\n=== 安全投资产品 ===")
    safe_cards = card_manager.get_safe_investments()
    for card in safe_cards[:3]:
        print(f"{card.name}: {card.core_params}")
    
    # 测试负担能力
    print(f"\n=== 负担能力测试（现金50,000元）===")
    affordable_cards = card_manager.filter_affordable_cards(50000)
    print(f"可负担的产品数量: {len(affordable_cards)}")
    
    for index, card in affordable_cards[:5]:
        print(f"{card.name}: {card.core_params}")