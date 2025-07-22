"""
卡片管理器
负责加载、管理和分发所有类型的卡片
"""

import json
import random
import os

from .base import CardType
from .enterprise import EnterpriseCard
from .opportunity import OpportunityCard
from .financial import FinancialCard
from .side_business import SideBusinessCard

class CardManager:
    """卡片管理器 - 管理所有卡片数据"""
    
    def __init__(self, card_data_file="data/cards.json"):
        self.cards = {}  # 所有卡片的字典 {card_id: card_object}
        self.card_decks = {
            CardType.ENTERPRISE: [],
            CardType.OPPORTUNITY: [],
            CardType.FINANCIAL: [],
            CardType.SIDE_BUSINESS: []
        }
        self.drawn_cards_history = []  # 已抽取的卡片历史
        self.load_cards(card_data_file)
    
    def load_cards(self, data_file):
        """从JSON文件加载卡片数据"""
        try:
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for card_data in data['cards']:
                    card = self._create_card_from_data(card_data)
                    if card:
                        self.cards[card.card_id] = card
                        self.card_decks[card.type].append(card)
                        
                print(f"成功加载 {len(self.cards)} 张卡片")
            else:
                print(f"卡片数据文件 {data_file} 未找到，创建默认卡片")
                self._create_default_cards()
                
        except Exception as e:
            print(f"加载卡片数据失败: {e}，使用默认卡片")
            self._create_default_cards()
    
    def _create_card_from_data(self, data):
        """根据数据创建卡片对象"""
        try:
            card_type = CardType(data['type'])
            
            if card_type == CardType.ENTERPRISE:
                return EnterpriseCard(
                    data['id'], data['name'], data['description'],
                    data['cost'], data['down_payment'], data['monthly_cash_flow'],
                    data.get('employee_count', 0), data.get('management_required', False)
                )
            elif card_type == CardType.OPPORTUNITY:
                return OpportunityCard(
                    data['id'], data['name'], data['description'],
                    data['cost'], data['down_payment'], data['monthly_cash_flow']
                )
            elif card_type == CardType.FINANCIAL:
                return FinancialCard(
                    data['id'], data['name'], data['description'],
                    data['price_per_share'], data['dividend_per_share'],
                    data.get('min_shares', 1), data.get('max_shares', 1000)
                )
            elif card_type == CardType.SIDE_BUSINESS:
                return SideBusinessCard(
                    data['id'], data['name'], data['description'],
                    data['cost'], data['monthly_cash_flow'],
                    data.get('time_required_hours', 0)
                )
        except Exception as e:
            print(f"创建卡片失败 {data.get('id', 'unknown')}: {e}")
            return None
    
    def _create_default_cards(self):
        """创建默认卡片用于测试"""
        default_cards = [
            # 企业卡
            EnterpriseCard("ENT001", "小型餐厅", "投资一家小型餐厅", 
                         50000, 10000, 1200, 3, True),
            EnterpriseCard("ENT002", "洗车店", "开设一家自助洗车店", 
                         30000, 6000, 800, 1, False),
            
            # 机会卡
            OpportunityCard("OPP001", "出租公寓", "购买一套公寓用于出租", 
                          80000, 16000, 800),
            OpportunityCard("OPP002", "商铺投资", "投资一间小商铺", 
                          120000, 24000, 1500),
            
            # 金融卡
            FinancialCard("FIN001", "科技股票基金", "投资科技行业股票基金", 
                        100, 2, 10, 1000),
            FinancialCard("FIN002", "蓝筹股票", "稳定的大公司股票", 
                        50, 1, 20, 2000),
            
            # 副业卡
            SideBusinessCard("SIDE001", "网络销售", "开设网络销售副业", 
                           2000, 400, 10),
            SideBusinessCard("SIDE002", "自媒体", "创建自媒体账号", 
                           1000, 300, 15),
        ]
        
        for card in default_cards:
            self.cards[card.card_id] = card
            self.card_decks[card.type].append(card)
        
        print(f"创建了 {len(default_cards)} 张默认卡片")
    
    def draw_card(self, card_type):
        """抽取指定类型的卡片"""
        deck = self.card_decks[card_type]
        if deck:
            card = random.choice(deck)
            self.drawn_cards_history.append((card.card_id, card_type))
            return card
        return None
    
    def draw_random_card(self):
        """随机抽取任意类型的卡片"""
        all_cards = []
        for deck in self.card_decks.values():
            all_cards.extend(deck)
        
        if all_cards:
            card = random.choice(all_cards)
            self.drawn_cards_history.append((card.card_id, card.type))
            return card
        return None
    
    def get_card_by_id(self, card_id):
        """根据ID获取卡片"""
        return self.cards.get(card_id)
    
    def get_cards_by_type(self, card_type):
        """获取指定类型的所有卡片"""
        return self.card_decks.get(card_type, [])
    
    def get_deck_size(self, card_type):
        """获取指定类型牌堆的大小"""
        return len(self.card_decks.get(card_type, []))
    
    def get_total_cards(self):
        """获取总卡片数量"""
        return len(self.cards)
    
    def get_cards_summary(self):
        """获取卡片摘要信息"""
        summary = {}
        for card_type, deck in self.card_decks.items():
            summary[card_type.value] = len(deck)
        return summary
    
    def reset_draw_history(self):
        """重置抽卡历史"""
        self.drawn_cards_history = []
    
    def get_draw_history(self):
        """获取抽卡历史"""
        return self.drawn_cards_history.copy()
    
    def __str__(self):
        summary = self.get_cards_summary()
        return f"卡片管理器: {summary}" 