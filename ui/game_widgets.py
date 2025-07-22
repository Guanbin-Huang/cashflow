"""
游戏相关的UI组件
包含各种游戏界面的小部件
"""

import tkinter as tk
from tkinter import ttk

class PlayerInfoWidget:
    """玩家信息显示组件"""
    
    def __init__(self, parent, player):
        self.player = player
        self.frame = ttk.LabelFrame(parent, text=player.name, padding="5")
        
        # 现金
        self.cash_label = ttk.Label(self.frame, text=f"现金: {player.cash}")
        self.cash_label.pack(anchor="w")
        
        # 被动收入
        self.income_label = ttk.Label(self.frame, text=f"被动收入: {player.passive_income}")
        self.income_label.pack(anchor="w")
        
        # 支出
        self.expense_label = ttk.Label(self.frame, text=f"支出: {player.expenses}")
        self.expense_label.pack(anchor="w")
        
        # 财务自由状态
        self.freedom_label = ttk.Label(self.frame, 
            text="财务自由" if player.is_financially_free() else "未财务自由",
            foreground="green" if player.is_financially_free() else "red")
        self.freedom_label.pack(anchor="w")
    
    def update(self):
        """更新显示"""
        self.cash_label.config(text=f"现金: {self.player.cash}")
        self.income_label.config(text=f"被动收入: {self.player.passive_income}")
        self.expense_label.config(text=f"支出: {self.player.expenses}")
        
        is_free = self.player.is_financially_free()
        self.freedom_label.config(
            text="财务自由" if is_free else "未财务自由",
            foreground="green" if is_free else "red"
        )

class CardInfoWidget:
    """卡片信息显示组件"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="当前卡片", padding="10")
        
        self.card_name = ttk.Label(self.frame, text="", font=("Arial", 12, "bold"))
        self.card_name.pack(anchor="w")
        
        self.card_desc = ttk.Label(self.frame, text="", wraplength=250)
        self.card_desc.pack(anchor="w", pady=5)
        
        self.card_details = ttk.Label(self.frame, text="")
        self.card_details.pack(anchor="w")
    
    def set_card(self, card):
        """设置显示的卡片"""
        if card:
            self.card_name.config(text=card.name)
            self.card_desc.config(text=card.description)
            
            details = []
            if hasattr(card, 'cost'):
                details.append(f"成本: {card.cost}")
            if hasattr(card, 'down_payment'):
                details.append(f"首付: {card.down_payment}")
            if hasattr(card, 'monthly_cash_flow'):
                details.append(f"月现金流: {card.monthly_cash_flow}")
            
            self.card_details.config(text="\n".join(details))
        else:
            self.card_name.config(text="无卡片")
            self.card_desc.config(text="")
            self.card_details.config(text="")

class GameLogWidget:
    """游戏日志组件"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="游戏日志", padding="5")
        
        # 文本框和滚动条
        self.text = tk.Text(self.frame, height=8, wrap=tk.WORD, state="disabled")
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
        
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_message(self, message):
        """添加日志消息"""
        self.text.config(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.config(state="disabled")
        self.text.see(tk.END)
    
    def clear(self):
        """清空日志"""
        self.text.config(state="normal")
        self.text.delete(1.0, tk.END)
        self.text.config(state="disabled")

class DiceWidget:
    """骰子显示组件"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        
        self.dice_label = ttk.Label(self.frame, text="🎲", font=("Arial", 24))
        self.dice_label.pack()
        
        self.value_label = ttk.Label(self.frame, text="", font=("Arial", 16, "bold"))
        self.value_label.pack()
    
    def set_value(self, value):
        """设置骰子值"""
        self.value_label.config(text=str(value) if value else "")
    
    def reset(self):
        """重置骰子"""
        self.value_label.config(text="") 