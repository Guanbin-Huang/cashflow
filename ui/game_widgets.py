"""
财富流游戏UI组件库 - Game Widgets Library
包含各种游戏界面的可重用组件

文件功能概述：
==============
本文件定义了财富流游戏中使用的各种可重用UI组件，这些组件被主窗口
和其他界面模块调用，提供了模块化、可维护的界面开发方式。每个组件
都有特定的显示和交互功能。

主要组件：
----------
1. PlayerInfoWidget - 玩家信息显示组件
   - 显示玩家基本财务信息
   - 现金、被动收入、支出展示
   - 财务自由状态指示
   - 支持实时信息更新

2. CardInfoWidget - 卡片信息显示组件
   - 显示当前抽到的投资卡片
   - 卡片名称、描述、详细参数
   - 成本、首付、月现金流信息
   - 动态卡片内容切换

3. GameLogWidget - 游戏日志组件
   - 游戏事件日志记录显示
   - 滚动文本框实现
   - 自动滚动到最新消息
   - 日志清空功能

4. DiceWidget - 骰子显示组件
   - 直观的骰子图标显示
   - 投掷结果数字展示
   - 重置功能支持
   - 美观的视觉效果

核心功能：
----------
- 模块化的UI组件设计
- 统一的组件接口规范
- 灵活的布局集成能力
- 实时数据更新支持
- 用户友好的视觉效果

技术特点：
----------
- 基于Tkinter的组件封装
- 面向对象的设计模式
- 可重用的组件架构
- 清晰的组件职责分离
- 易于扩展的接口设计

设计原则：
----------
- 单一职责原则
- 高内聚低耦合
- 可重用性优先
- 用户体验友好
- 代码可维护性

组件特色：
----------
- PlayerInfoWidget: 实时财务状态监控
- CardInfoWidget: 投资机会详细展示
- GameLogWidget: 完整游戏过程记录
- DiceWidget: 生动的游戏互动体验

使用方式：
----------
- 在主窗口中实例化各组件
- 通过update()方法更新组件状态
- 使用set_*()方法设置组件数据
- 组件自动处理界面刷新

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
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