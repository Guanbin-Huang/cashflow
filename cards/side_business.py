"""
副业卡片系统
处理副业卡片数据和对玩家财务表的影响
整合同事的详细实现到标准化架构
"""

import csv
import os
from .base import InvestmentCard, CardType

class SideBusinessCard(InvestmentCard):
    """副业卡片类"""
    
    def __init__(self, card_id, name, description, cost, monthly_cash_flow, time_required_hours=0):
        # 调用父类构造器
        super().__init__(card_id, name, CardType.SIDE_BUSINESS, description, cost, cost, monthly_cash_flow)
        
        # 副业特有属性
        self.time_required_hours = time_required_hours
        
        # 为了向后兼容，保留同事的实现
        self.business_id = card_id
        self.business_name = name
        self.investment = cost
        self.monthly_income = monthly_cash_flow
        self.energy_cost = -time_required_hours  # 时间作为精力消耗
    
    def __str__(self):
        return (f"副业卡片: {self.business_name} ({self.business_id})\n"
                f"描述: {self.description}\n"
                f"投资: {self.investment:,}元\n"
                f"月收入: {self.monthly_income:,}元\n"
                f"精力消耗: {self.energy_cost}")
    
    def execute_purchase(self, player):
        """执行购买"""
        if self.can_afford(player):
            player.cash -= self.cost
            return True
        return False
    
    def get_required_cash(self):
        """获取所需现金"""
        return self.cost
    
    def can_afford(self, player):
        """检查玩家是否有足够现金支付投资"""
        return player.cash >= self.investment
    
    def has_enough_energy(self, player_energy):
        """检查玩家是否有足够精力经营副业"""
        return player_energy >= abs(self.energy_cost)
    
    def get_investment_data(self):
        """获取用于损益表的投资数据"""
        return {
            "代码": self.business_name,
            "投资": self.investment,
            "现金流": self.monthly_income
        }
    
    def calculate_roi(self):
        """计算年化收益率"""
        if self.investment == 0:
            return float('inf')  # 无限大收益率
        return (self.monthly_income * 12) / self.investment * 100

class SideBusinessCardManager:
    """副业卡片管理器"""
    
    def __init__(self, csv_file_path=None):
        self.cards = []
        if csv_file_path:
            self.load_cards_from_csv(csv_file_path)
    
    def load_cards_from_csv(self, csv_file_path):
        """从CSV文件加载副业卡片"""
        self.cards = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # 清理数据中的逗号和引号
                    investment = int(row['副业投资（元）'].replace(',', '').replace('"', '')) if row['副业投资（元）'] != '0' else 0
                    monthly_income = int(row['月收入（元 / 月）'].replace(',', '').replace('"', ''))
                    energy_cost = int(row['精力变化'])
                    
                    card = SideBusinessCard(
                        business_id=row['副业编号'],
                        business_name=row['副业名称'],
                        description=row['副业描述'],
                        investment=investment,
                        monthly_income=monthly_income,
                        energy_cost=energy_cost
                    )
                    
                    self.cards.append(card)
                    
        except FileNotFoundError:
            print(f"警告: 找不到文件 {csv_file_path}")
        except Exception as e:
            print(f"加载副业卡片时出错: {e}")
    
    def get_card_by_index(self, index):
        """根据索引获取卡片"""
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def get_card_by_id(self, business_id):
        """根据ID获取卡片"""
        for card in self.cards:
            if card.business_id == business_id:
                return card
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
    
    def get_zero_investment_cards(self):
        """获取零投资副业卡片"""
        return [card for card in self.cards if card.investment == 0]
    
    def get_high_roi_cards(self, min_roi=200):
        """获取高收益率副业卡片"""
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
                print(f"年化收益率: 无限大（零投资）")
            else:
                print(f"年化收益率: {roi:.1f}%")

# 默认加载副业卡片
def load_default_side_business_cards():
    """加载默认的副业卡片"""
    # 尝试从数据目录加载
    data_path = "data/cards/副业卡片.csv"
    if os.path.exists(data_path):
        return SideBusinessCardManager(data_path)
    
    # 如果找不到文件，创建一些示例卡片
    print("警告: 未找到副业卡片CSV文件，使用示例数据")
    manager = SideBusinessCardManager()
    
    # 添加一些示例卡片
    example_cards = [
        SideBusinessCard("P01", "办摄影公司", "利用业余时间创办摄影公司", 3000, 3500, -3),
        SideBusinessCard("P04", "整理收纳师", "提供整理收纳服务", 0, 2500, -3),
        SideBusinessCard("P05", "自媒体写作", "写作发文获得收入", 0, 3500, -4)
    ]
    
    manager.cards = example_cards
    return manager

if __name__ == "__main__":
    # 测试副业卡片系统
    print("=== 副业卡片系统测试 ===")
    
    # 加载卡片
    card_manager = load_default_side_business_cards()
    print(f"成功加载 {card_manager.get_cards_count()} 张副业卡片")
    
    # 显示零投资卡片
    print(f"\n=== 零投资副业卡片 ===")
    zero_investment_cards = card_manager.get_zero_investment_cards()
    for card in zero_investment_cards:
        print(f"{card.business_name}: 月收入{card.monthly_income:,}元, 精力{card.energy_cost}")
    
    # 显示高收益率卡片
    print(f"\n=== 高收益率副业卡片（>200%）===")
    high_roi_cards = card_manager.get_high_roi_cards(200)
    for card, roi in high_roi_cards[:5]:  # 显示前5个
        print(f"{card.business_name}: 年化收益率{roi:.1f}%, 投资{card.investment:,}元")
    
    # 测试玩家负担能力
    print(f"\n=== 负担能力测试 ===")
    test_cash = 5000
    test_energy = 4
    
    affordable_cards = card_manager.filter_affordable_cards(test_cash, test_energy)
    print(f"玩家现金: {test_cash:,}元, 精力: {test_energy}")
    print(f"可负担的卡片数量: {len(affordable_cards)}")
    
    for index, card in affordable_cards[:3]:  # 显示前3个
        print(f"\n可开展副业 {index+1}:")
        print(f"{card.business_name}: 投资{card.investment:,}元, 月收入{card.monthly_income:,}元")