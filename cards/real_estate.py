"""
房地产卡片系统
处理房地产卡片数据和对玩家财务表的影响
整合同事的详细实现到标准化架构
"""

import csv
import os

class RealEstateCard:
    """房地产卡片类"""
    
    def __init__(self, property_type, down_payment, total_price, mortgage, 
                 price_range, monthly_income, energy_cost):
        self.property_type = property_type      # 房产类型
        self.down_payment = down_payment        # 首付
        self.total_price = total_price          # 房产总价
        self.mortgage = mortgage                # 抵押贷款
        self.price_range = price_range          # 价格范围
        self.monthly_income = monthly_income    # 月收入（可能为负）
        self.energy_cost = energy_cost          # 精力消耗（负值）
    
    def __str__(self):
        return (f"房地产卡片: {self.property_type}\n"
                f"首付: {self.down_payment:,}元\n"
                f"总价: {self.total_price:,}元\n"
                f"抵押贷: {self.mortgage:,}元\n"
                f"月收入: {self.monthly_income:,}元\n"
                f"精力消耗: {self.energy_cost}")
    
    def can_afford(self, player_cash):
        """检查玩家是否有足够现金支付首付"""
        return player_cash >= self.down_payment
    
    def has_enough_energy(self, player_energy):
        """检查玩家是否有足够精力购买房产"""
        # 精力消耗是负值，所以需要玩家当前精力大于等于消耗的绝对值
        return player_energy >= abs(self.energy_cost)
    
    def get_investment_data(self):
        """获取用于损益表的投资数据"""
        return {
            "代码": self.property_type,
            "首付": self.down_payment,
            "现金流": self.monthly_income
        }
    
    def get_asset_data(self):
        """获取用于资产负债表的资产数据"""
        return {
            "权益": self.total_price
        }
    
    def get_liability_data(self):
        """获取用于资产负债表的负债数据"""
        return {
            "代码": self.property_type,
            "金额": self.mortgage
        }
    
    def calculate_roi(self):
        """计算年化收益率"""
        if self.down_payment == 0:
            return float('inf')
        return (self.monthly_income * 12) / self.down_payment * 100
    
    def calculate_cash_on_cash_return(self):
        """计算现金现金回报率"""
        if self.down_payment == 0:
            return float('inf')
        return (self.monthly_income * 12) / self.down_payment * 100

class RealEstateCardManager:
    """房地产卡片管理器"""
    
    def __init__(self, csv_file_path=None):
        self.cards = []
        if csv_file_path:
            self.load_cards_from_csv(csv_file_path)
    
    def load_cards_from_csv(self, csv_file_path):
        """从CSV文件加载房地产卡片"""
        self.cards = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # 清理数据中的逗号和引号
                    down_payment = int(row['首付（元）'].replace(',', '').replace('"', ''))
                    total_price = int(row['房产总价（元）'].replace(',', '').replace('"', ''))
                    mortgage = int(row['抵押贷（元）'].replace(',', '').replace('"', ''))
                    monthly_income = int(row['被动收入 / 月（元）'].replace(',', '').replace('"', ''))
                    energy_cost = int(row['精力值'])
                    
                    card = RealEstateCard(
                        property_type=row['房产类型'],
                        down_payment=down_payment,
                        total_price=total_price,
                        mortgage=mortgage,
                        price_range=row['价格范围（元）'],
                        monthly_income=monthly_income,
                        energy_cost=energy_cost
                    )
                    
                    self.cards.append(card)
                    
        except FileNotFoundError:
            print(f"警告: 找不到文件 {csv_file_path}")
        except Exception as e:
            print(f"加载房地产卡片时出错: {e}")
    
    def get_card_by_index(self, index):
        """根据索引获取卡片"""
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def get_all_cards(self):
        """获取所有卡片"""
        return self.cards
    
    def get_cards_count(self):
        """获取卡片总数"""
        return len(self.cards)
    
    def filter_affordable_cards(self, player_cash, player_energy):
        """筛选玩家能负担得起的卡片"""
        affordable_cards = []
        for i, card in enumerate(self.cards):
            if card.can_afford(player_cash) and card.has_enough_energy(player_energy):
                affordable_cards.append((i, card))
        return affordable_cards
    
    def get_positive_cashflow_cards(self):
        """获取正现金流房产"""
        return [card for card in self.cards if card.monthly_income > 0]
    
    def get_high_roi_cards(self, min_roi=10):
        """获取高收益率房产"""
        high_roi_cards = []
        for card in self.cards:
            roi = card.calculate_roi()
            if roi >= min_roi:
                high_roi_cards.append((card, roi))
        return sorted(high_roi_cards, key=lambda x: x[1], reverse=True)
    
    def print_all_cards(self):
        """打印所有卡片信息"""
        for i, card in enumerate(self.cards):
            print(f"\n=== 卡片 {i+1} ===")
            print(card)
            roi = card.calculate_roi()
            if roi == float('inf'):
                print(f"年化收益率: 无限大（零首付）")
            else:
                print(f"年化收益率: {roi:.1f}%")

# 默认加载房地产卡片
def load_default_real_estate_cards():
    """加载默认的房地产卡片"""
    # 尝试从数据目录加载
    data_path = "data/cards/房地产卡片.csv"
    if os.path.exists(data_path):
        return RealEstateCardManager(data_path)
    
    # 如果找不到文件，创建一些示例卡片
    print("警告: 未找到房地产卡片CSV文件，使用示例数据")
    manager = RealEstateCardManager()
    
    # 添加一些示例卡片
    example_cards = [
        RealEstateCard("3室1厅1卫", 60000, 120000, 60000, "65,000-130,000", 8000, -3),
        RealEstateCard("1室1厅1卫", 40000, 80000, 40000, "45,000-60,000", 500, -2),
        RealEstateCard("2室公寓", 60000, 120000, 60000, "50,000-70,000", 2500, -3)
    ]
    
    manager.cards = example_cards
    return manager

if __name__ == "__main__":
    # 测试房地产卡片系统
    print("=== 房地产卡片系统测试 ===")
    
    # 加载卡片
    card_manager = load_default_real_estate_cards()
    print(f"成功加载 {card_manager.get_cards_count()} 张房地产卡片")
    
    # 显示所有卡片
    card_manager.print_all_cards()
    
    # 显示正现金流房产
    print(f"\n=== 正现金流房产 ===")
    positive_cards = card_manager.get_positive_cashflow_cards()
    for card in positive_cards:
        roi = card.calculate_roi()
        print(f"{card.property_type}: 首付{card.down_payment:,}元, 月收入{card.monthly_income:,}元, 年化{roi:.1f}%")
    
    # 测试玩家负担能力
    print(f"\n=== 负担能力测试 ===")
    test_cash = 70000
    test_energy = 5
    
    affordable_cards = card_manager.filter_affordable_cards(test_cash, test_energy)
    print(f"玩家现金: {test_cash:,}元, 精力: {test_energy}")
    print(f"可负担的卡片数量: {len(affordable_cards)}")
    
    for index, card in affordable_cards:
        print(f"\n可购买卡片 {index+1}:")
        print(card)