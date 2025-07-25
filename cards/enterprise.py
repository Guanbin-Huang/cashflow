"""
企业卡片系统
处理企业卡片数据和对玩家财务表的影响
整合同事的详细实现到标准化架构
"""

import csv
import os
import re
from .base import InvestmentCard, CardType

class EnterpriseCard(InvestmentCard):
    """企业卡片类"""
    
    def __init__(self, card_id, name, description, cost, down_payment, monthly_cash_flow, employee_count=0, management_required=False):
        # 调用父类构造器
        super().__init__(card_id, name, CardType.ENTERPRISE, description, cost, down_payment, monthly_cash_flow)
        
        # 企业特有属性
        self.employee_count = employee_count
        self.management_required = management_required
        
        # 为了向后兼容，保留同事的实现
        self.enterprise_id = card_id
        self.enterprise_name = name
        self.market_value = cost
        self.monthly_cashflow = monthly_cash_flow
        self.energy_cost = -employee_count  # 员工数作为精力消耗
        
        # 解析特殊格式的月现金流
        self.parsed_cashflow = self._parse_cashflow()
    
    def _parse_cashflow(self):
        """解析月现金流（处理特殊格式）"""
        if isinstance(self.monthly_cashflow, str):
            # 处理类似 "+1,500 / 月（最多 10 台）" 的格式
            if "最多" in self.monthly_cashflow:
                # 提取数字
                numbers = re.findall(r'(\d+)', self.monthly_cashflow.replace(',', ''))
                if len(numbers) >= 2:
                    per_unit = int(numbers[0])  # 每台收益
                    max_units = int(numbers[1]) # 最多台数
                    return {
                        "type": "multiple_units",
                        "per_unit": per_unit,
                        "max_units": max_units,
                        "total_max": per_unit * max_units
                    }
            else:
                # 普通数字格式
                numbers = re.findall(r'(\d+)', str(self.monthly_cashflow).replace(',', ''))
                if numbers:
                    return {
                        "type": "fixed",
                        "amount": int(numbers[0])
                    }
        else:
            # 直接是数字
            return {
                "type": "fixed", 
                "amount": int(self.monthly_cashflow)
            }
        
        return {"type": "fixed", "amount": 0}
    
    def __str__(self):
        cashflow_str = self.get_cashflow_description()
        return (f"企业卡片: {self.enterprise_name} ({self.enterprise_id})\n"
                f"首付: {self.down_payment:,}元\n"
                f"市值: {self.market_value:,}元\n"
                f"月现金流: {cashflow_str}\n"
                f"精力消耗: {self.energy_cost}")
    
    def get_cashflow_description(self):
        """获取现金流描述"""
        if self.parsed_cashflow["type"] == "multiple_units":
            return f"{self.parsed_cashflow['per_unit']:,}元/台 (最多{self.parsed_cashflow['max_units']}台)"
        else:
            return f"{self.parsed_cashflow['amount']:,}元/月"
    
    def get_actual_cashflow(self, units=1):
        """获取实际现金流（考虑台数）"""
        if self.parsed_cashflow["type"] == "multiple_units":
            max_units = self.parsed_cashflow['max_units']
            actual_units = min(units, max_units)
            return actual_units * self.parsed_cashflow['per_unit']
        else:
            return self.parsed_cashflow['amount']
    
    def can_afford(self, player):
        """检查玩家是否有足够现金支付首付"""
        return player.cash >= self.down_payment
    
    def execute_purchase(self, player):
        """执行购买"""
        if self.can_afford(player):
            player.cash -= self.down_payment
            # 如果需要贷款，增加负债
            if self.cost > self.down_payment:
                loan_amount = self.cost - self.down_payment
                player.cash += loan_amount
                # 可以在这里添加负债到玩家的负债表
            return True
        return False
    
    def get_required_cash(self):
        """获取所需现金（首付金额）"""
        return self.down_payment
    
    def has_enough_energy(self, player_energy):
        """检查玩家是否有足够精力经营企业"""
        return player_energy >= abs(self.energy_cost)
    
    def get_investment_data(self, units=1):
        """获取用于损益表的投资数据"""
        actual_cashflow = self.get_actual_cashflow(units)
        return {
            "代码": self.enterprise_name,
            "首付": self.down_payment,
            "现金流": actual_cashflow
        }
    
    def get_asset_data(self):
        """获取用于资产负债表的资产数据"""
        return {
            "权益": self.market_value
        }
    
    def calculate_roi(self, units=1):
        """计算年化收益率"""
        if self.down_payment == 0:
            return float('inf')
        actual_cashflow = self.get_actual_cashflow(units)
        return (actual_cashflow * 12) / self.down_payment * 100
    
    def calculate_energy_efficiency(self, units=1):
        """计算精力效率（月现金流/精力消耗）"""
        if self.energy_cost == 0:
            return float('inf')  # 无精力消耗
        actual_cashflow = self.get_actual_cashflow(units)
        return actual_cashflow / abs(self.energy_cost)

class EnterpriseCardManager:
    """企业卡片管理器"""
    
    def __init__(self, csv_file_path=None):
        self.cards = []
        if csv_file_path:
            self.load_cards_from_csv(csv_file_path)
    
    def load_cards_from_csv(self, csv_file_path):
        """从CSV文件加载企业卡片"""
        self.cards = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # 清理数据中的逗号和引号
                    down_payment = int(row['首付（元）'].replace(',', '').replace('"', ''))
                    market_value = int(row['市值（元）'].replace(',', '').replace('"', ''))
                    monthly_cashflow = row['月现金流（元）']  # 保持原格式用于解析
                    energy_cost = int(row['精力变化'])
                    
                    card = EnterpriseCard(
                        enterprise_id=row['企业编号'],
                        enterprise_name=row['企业名称'],
                        down_payment=down_payment,
                        market_value=market_value,
                        monthly_cashflow=monthly_cashflow,
                        energy_cost=energy_cost
                    )
                    
                    self.cards.append(card)
                    
        except FileNotFoundError:
            print(f"警告: 找不到文件 {csv_file_path}")
        except Exception as e:
            print(f"加载企业卡片时出错: {e}")
    
    def get_card_by_index(self, index):
        """根据索引获取卡片"""
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def get_card_by_id(self, enterprise_id):
        """根据ID获取卡片"""
        for card in self.cards:
            if card.enterprise_id == enterprise_id:
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
    
    def get_zero_energy_cards(self):
        """获取零精力消耗企业"""
        return [card for card in self.cards if card.energy_cost == 0]
    
    def get_high_roi_cards(self, min_roi=200):
        """获取高收益率企业"""
        high_roi_cards = []
        for card in self.cards:
            roi = card.calculate_roi()
            if roi >= min_roi:
                high_roi_cards.append((card, roi))
        return sorted(high_roi_cards, key=lambda x: x[1], reverse=True)
    
    def get_high_efficiency_cards(self):
        """获取高精力效率企业"""
        efficiency_cards = []
        for card in self.cards:
            efficiency = card.calculate_energy_efficiency()
            efficiency_cards.append((card, efficiency))
        return sorted(efficiency_cards, key=lambda x: x[1], reverse=True)
    
    def get_low_investment_cards(self, max_investment=100000):
        """获取低投资门槛企业"""
        return [card for card in self.cards if card.down_payment <= max_investment]
    
    def get_high_cashflow_cards(self, min_cashflow=50000):
        """获取高现金流企业"""
        high_cashflow_cards = []
        for card in self.cards:
            if card.parsed_cashflow["type"] == "multiple_units":
                max_cashflow = card.parsed_cashflow["total_max"]
            else:
                max_cashflow = card.parsed_cashflow["amount"]
            
            if max_cashflow >= min_cashflow:
                high_cashflow_cards.append(card)
        return high_cashflow_cards
    
    def print_all_cards(self):
        """打印所有卡片信息"""
        for i, card in enumerate(self.cards):
            print(f"\n=== 卡片 {i+1} ===")
            print(card)
            roi = card.calculate_roi()
            efficiency = card.calculate_energy_efficiency()
            
            if roi == float('inf'):
                print(f"年化收益率: 无限大（零投资）")
            else:
                print(f"年化收益率: {roi:.1f}%")
            
            if efficiency == float('inf'):
                print(f"精力效率: 无限大（零精力消耗）")
            else:
                print(f"精力效率: {efficiency:.0f}元/精力点")
    
    def print_investment_analysis(self):
        """打印投资分析报告"""
        print(f"\n=== 企业投资分析报告 ===")
        
        # 零精力消耗企业
        zero_energy = self.get_zero_energy_cards()
        print(f"\n【零精力消耗企业】({len(zero_energy)}个)")
        for card in zero_energy:
            roi = card.calculate_roi()
            print(f"{card.enterprise_name}: 首付{card.down_payment:,}元, 年化{roi:.1f}%")
        
        # 高收益率企业
        high_roi = self.get_high_roi_cards(300)
        print(f"\n【高收益率企业】(>300%, 前5名)")
        for card, roi in high_roi[:5]:
            print(f"{card.enterprise_name}: 年化{roi:.1f}%, 首付{card.down_payment:,}元")
        
        # 低投资门槛企业
        low_investment = self.get_low_investment_cards(60000)
        print(f"\n【低投资门槛企业】(≤60,000元, {len(low_investment)}个)")
        for card in low_investment[:5]:
            roi = card.calculate_roi()
            print(f"{card.enterprise_name}: 首付{card.down_payment:,}元, 年化{roi:.1f}%")

# 默认加载企业卡片
def load_default_enterprise_cards():
    """加载默认的企业卡片"""
    # 尝试从数据目录加载
    data_path = "data/cards/企业卡片.csv"
    if os.path.exists(data_path):
        return EnterpriseCardManager(data_path)
    
    # 如果找不到文件，创建一些示例卡片
    print("警告: 未找到企业卡片CSV文件，使用示例数据")
    manager = EnterpriseCardManager()
    
    # 添加一些示例卡片
    example_cards = [
        EnterpriseCard("C01", "自助娃娃机", 30000, 60000, "+1,500 / 月（最多 10 台）", -3),
        EnterpriseCard("C02", "自助咖啡机", 50000, 100000, "22,000", 0),
        EnterpriseCard("C08", "美容机构", 60000, 120000, "32,000", -3)
    ]
    
    manager.cards = example_cards
    return manager

if __name__ == "__main__":
    # 测试企业卡片系统
    print("=== 企业卡片系统测试 ===")
    
    # 加载卡片
    card_manager = load_default_enterprise_cards()
    print(f"成功加载 {card_manager.get_cards_count()} 张企业卡片")
    
    # 投资分析报告
    card_manager.print_investment_analysis()
    
    # 测试玩家负担能力
    print(f"\n=== 负担能力测试 ===")
    test_cash = 100000
    test_energy = 5
    
    affordable_cards = card_manager.filter_affordable_cards(test_cash, test_energy)
    print(f"玩家现金: {test_cash:,}元, 精力: {test_energy}")
    print(f"可负担的卡片数量: {len(affordable_cards)}")
    
    for index, card in affordable_cards[:3]:  # 显示前3个
        print(f"\n可投资企业 {index+1}:")
        print(f"{card.enterprise_name}: 首付{card.down_payment:,}元, {card.get_cashflow_description()}")
        print(f"年化收益率: {card.calculate_roi():.1f}%")
    
    # 测试多台设备企业
    print(f"\n=== 多台设备企业测试 ===")
    multi_unit_cards = [card for card in card_manager.cards if card.parsed_cashflow["type"] == "multiple_units"]
    for card in multi_unit_cards[:2]:
        print(f"\n{card.enterprise_name}:")
        for units in [1, 5, 10]:
            cashflow = card.get_actual_cashflow(units)
            roi = card.calculate_roi(units)
            print(f"  {units}台: 月现金流{cashflow:,}元, 年化收益率{roi:.1f}%")