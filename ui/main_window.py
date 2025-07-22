"""
财富流游戏主窗口
基于Tkinter的桌面应用界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

from game import GameEngine
from player import Player

class MainWindow:
    """主游戏窗口"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("财富流游戏 - Cash Flow Game")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # 游戏引擎
        self.game_engine = None
        
        # UI组件
        self.setup_ui()
        self.load_professions()
        
    def setup_ui(self):
        """设置UI界面"""
        # 主菜单栏
        self.create_menu()
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧面板 - 游戏控制
        self.create_control_panel(main_frame)
        
        # 中央面板 - 游戏棋盘
        self.create_game_board(main_frame)
        
        # 右侧面板 - 玩家信息
        self.create_player_panel(main_frame)
        
        # 底部面板 - 游戏日志
        self.create_log_panel(main_frame)
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="游戏", menu=game_menu)
        game_menu.add_command(label="新游戏", command=self.new_game)
        game_menu.add_command(label="保存游戏", command=self.save_game)
        game_menu.add_command(label="加载游戏", command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.root.quit)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="游戏规则", command=self.show_rules)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="游戏控制", padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # 投骰子按钮
        self.roll_dice_btn = ttk.Button(control_frame, text="投骰子", 
                                      command=self.roll_dice, state="disabled")
        self.roll_dice_btn.pack(fill=tk.X, pady=5)
        
        # 移动按钮
        self.move_btn = ttk.Button(control_frame, text="移动", 
                                 command=self.move_player, state="disabled")
        self.move_btn.pack(fill=tk.X, pady=5)
        
        # 结束回合按钮
        self.end_turn_btn = ttk.Button(control_frame, text="结束回合", 
                                     command=self.end_turn, state="disabled")
        self.end_turn_btn.pack(fill=tk.X, pady=5)
        
        # 分隔符
        ttk.Separator(control_frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
        # 当前状态显示
        self.status_label = ttk.Label(control_frame, text="请开始新游戏", 
                                    foreground="blue", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)
        
        # 骰子结果显示
        self.dice_label = ttk.Label(control_frame, text="", 
                                  font=("Arial", 16, "bold"))
        self.dice_label.pack(pady=5)
        
        # 当前卡片信息
        self.card_frame = ttk.LabelFrame(control_frame, text="当前卡片")
        self.card_frame.pack(fill=tk.X, pady=10)
        
        self.card_info_label = ttk.Label(self.card_frame, text="无", wraplength=200)
        self.card_info_label.pack(pady=5)
        
        self.buy_card_btn = ttk.Button(self.card_frame, text="购买", 
                                     command=self.buy_card, state="disabled")
        self.buy_card_btn.pack(side=tk.LEFT, padx=5)
        
        self.pass_card_btn = ttk.Button(self.card_frame, text="放弃", 
                                      command=self.pass_card, state="disabled")
        self.pass_card_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_game_board(self, parent):
        """创建游戏棋盘"""
        board_frame = ttk.LabelFrame(parent, text="游戏棋盘", padding="10")
        board_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        
        # 棋盘画布
        self.board_canvas = tk.Canvas(board_frame, width=600, height=500, bg="white")
        self.board_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 延迟绘制棋盘，确保canvas完全初始化
        self.board_canvas.after(100, self.draw_board)
        
    def create_player_panel(self, parent):
        """创建玩家信息面板"""
        player_frame = ttk.LabelFrame(parent, text="玩家信息", padding="10")
        player_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # 玩家列表
        self.player_tree = ttk.Treeview(player_frame, columns=("现金", "被动收入", "支出"), 
                                      show="tree headings", height=10)
        self.player_tree.heading("#0", text="玩家")
        self.player_tree.heading("现金", text="现金")
        self.player_tree.heading("被动收入", text="被动收入")
        self.player_tree.heading("支出", text="支出")
        
        self.player_tree.column("#0", width=100)
        self.player_tree.column("现金", width=80)
        self.player_tree.column("被动收入", width=80)
        self.player_tree.column("支出", width=80)
        
        self.player_tree.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        player_scrollbar = ttk.Scrollbar(player_frame, orient="vertical", 
                                       command=self.player_tree.yview)
        player_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.player_tree.configure(yscrollcommand=player_scrollbar.set)
        
    def create_log_panel(self, parent):
        """创建游戏日志面板"""
        log_frame = ttk.LabelFrame(parent, text="游戏日志", padding="10")
        log_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # 日志文本框
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", 
                                    command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # 配置网格权重
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_columnconfigure(0, weight=0)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=0)
    
    def load_professions(self):
        """加载职业数据"""
        try:
            with open("data/professions.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.professions = data['professions']
        except:
            # 如果文件不存在，使用默认职业
            self.professions = [
                {"id": "engineer", "name": "工程师", "salary": 5000, 
                 "initial_cash": 10000, "initial_expenses": 2500}
            ]
    
    def new_game(self):
        """开始新游戏"""
        # 玩家设置对话框
        players_data = self.get_players_setup()
        if not players_data:
            return
            
        # 创建游戏引擎
        self.game_engine = GameEngine(players_data)
        success, message = self.game_engine.start_game()
        
        if success:
            self.update_ui()
            self.log_message("游戏开始！")
            messagebox.showinfo("游戏开始", message)
        else:
            messagebox.showerror("错误", message)
    
    def get_players_setup(self):
        """获取玩家设置"""
        dialog = PlayerSetupDialog(self.root, self.professions)
        self.root.wait_window(dialog.dialog)
        return dialog.result
    
    def roll_dice(self):
        """投骰子"""
        if self.game_engine:
            success, message = self.game_engine.roll_dice()
            if success:
                self.dice_label.config(text=f"🎲 {self.game_engine.current_dice_roll}")
                self.log_message(message)
                self.update_ui()
    
    def move_player(self):
        """移动玩家"""
        if self.game_engine:
            success, message = self.game_engine.move_player()
            if success:
                self.log_message(message)
                self.update_ui()
                self.draw_board()  # 重绘棋盘显示玩家位置
    
    def buy_card(self):
        """购买卡片"""
        if self.game_engine and self.game_engine.current_opportunity_card:
            card = self.game_engine.current_opportunity_card
            
            # 如果是金融卡，询问购买股数
            if card.type.value == "金融卡":
                shares = simpledialog.askinteger("购买股数", 
                    f"请输入要购买的股数 (最少{card.min_shares}股，最多{card.max_shares}股):",
                    minvalue=card.min_shares, maxvalue=card.max_shares)
                if shares is None:
                    return
                additional_data = {'shares': shares}
            else:
                additional_data = None
            
            success, message = self.game_engine.handle_card_decision("buy", additional_data)
            if success:
                self.log_message(message)
                self.update_ui()
    
    def pass_card(self):
        """放弃卡片"""
        if self.game_engine:
            success, message = self.game_engine.handle_card_decision("pass")
            if success:
                self.log_message(message)
                self.update_ui()
    
    def end_turn(self):
        """结束回合"""
        if self.game_engine:
            # 如果在市场阶段，先退出市场
            if self.game_engine.turn_phase.value == "市场操作":
                self.game_engine.handle_market_action("exit_market")
                self.log_message("退出市场")
                self.update_ui()
            
            success, message = self.game_engine.end_turn()
            if success:
                self.log_message(message)
                self.update_ui()
                
                # 检查游戏是否结束
                if self.game_engine.game_phase.value == "游戏结束":
                    messagebox.showinfo("游戏结束", message)
    
    def update_ui(self):
        """更新UI状态"""
        if not self.game_engine:
            return
            
        # 更新状态标签
        current_player = self.game_engine.get_current_player()
        phase = self.game_engine.turn_phase.value
        player_name = current_player.name if current_player else "无玩家"
        self.status_label.config(text=f"{player_name} - {phase}")
        
        # 更新按钮状态
        self.update_buttons()
        
        # 更新卡片信息
        self.update_card_info()
        
        # 更新玩家信息
        self.update_player_info()
    
    def update_buttons(self):
        """更新按钮状态"""
        if not self.game_engine:
            return
            
        phase = self.game_engine.turn_phase.value
        
        # 根据游戏阶段启用/禁用按钮
        self.roll_dice_btn.config(state="normal" if phase == "投骰子" else "disabled")
        self.move_btn.config(state="normal" if phase == "移动" else "disabled")
        self.end_turn_btn.config(state="normal" if phase == "结束回合" else "disabled")
        
        # 卡片决策按钮
        card_decision = phase == "卡片决策"
        self.buy_card_btn.config(state="normal" if card_decision else "disabled")
        self.pass_card_btn.config(state="normal" if card_decision else "disabled")
        
        # 市场操作：如果在市场阶段，允许直接结束回合
        if phase == "市场操作":
            self.end_turn_btn.config(state="normal")
    
    def update_card_info(self):
        """更新卡片信息"""
        if self.game_engine and self.game_engine.current_opportunity_card:
            card = self.game_engine.current_opportunity_card
            info = f"{card.name}\n{card.description}"
            if hasattr(card, 'cost'):
                info += f"\n成本: {card.cost}"
            if hasattr(card, 'down_payment'):
                info += f"\n首付: {card.down_payment}"
            if hasattr(card, 'monthly_cash_flow'):
                info += f"\n月现金流: {card.monthly_cash_flow}"
        else:
            info = "无"
        
        self.card_info_label.config(text=info)
    
    def update_player_info(self):
        """更新玩家信息"""
        # 清空现有数据
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        
        if not self.game_engine:
            return
        
        # 添加玩家数据
        for i, player in enumerate(self.game_engine.players):
            name = player.name
            if i == self.game_engine.current_player_index:
                name += " (当前)"
            
            self.player_tree.insert("", "end", text=name, 
                                  values=(player.cash, player.passive_income, player.expenses))
    
    def draw_board(self):
        """绘制游戏棋盘"""
        self.board_canvas.delete("all")
        
        # 更新canvas使其获取实际尺寸
        self.board_canvas.update()
        
        # 获取canvas尺寸，使用固定值避免0尺寸问题
        canvas_width = max(self.board_canvas.winfo_width(), 600)
        canvas_height = max(self.board_canvas.winfo_height(), 500)
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        radius = min(canvas_width, canvas_height) // 3
        
        # 绘制基础棋盘（即使没有游戏引擎也绘制）
        board_size = 24 if not self.game_engine else self.game_engine.board.get_board_size()
        
        # 绘制棋盘格子
        for i in range(board_size):
            angle = 2 * 3.14159 * i / board_size
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            
            # 绘制格子
            self.board_canvas.create_oval(x-20, y-20, x+20, y+20, 
                                        fill="lightblue", outline="black")
            
            # 绘制格子编号
            self.board_canvas.create_text(x, y, text=str(i))
        
        # 如果有游戏引擎，绘制玩家位置
        if self.game_engine:
            for i, player in enumerate(self.game_engine.players):
                angle = 2 * 3.14159 * player.position / board_size
                x = center_x + radius * cos(angle)
                y = center_y + radius * sin(angle)
                
                # 玩家标记
                colors = ["red", "green", "blue", "yellow", "purple", "orange"]
                color = colors[i % len(colors)]
                
                self.board_canvas.create_oval(x-8, y-8, x+8, y+8, 
                                            fill=color, outline="black")
                self.board_canvas.create_text(x, y, text=str(i+1), fill="white")
    
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def save_game(self):
        """保存游戏"""
        messagebox.showinfo("保存游戏", "保存功能尚未实现")
    
    def load_game(self):
        """加载游戏"""
        messagebox.showinfo("加载游戏", "加载功能尚未实现")
    
    def show_rules(self):
        """显示游戏规则"""
        rules = """
财富流游戏规则:

1. 游戏目标：通过投资和理财达到财务自由（被动收入 >= 支出）

2. 游戏流程：
   - 投骰子移动
   - 执行格子事件
   - 根据情况购买投资机会
   - 管理资产和负债

3. 格子类型：
   - 发薪水：收取工资和被动收入，支付支出
   - 机会：抽取投资机会卡片
   - 意外支出：遇到突发费用
   - 市场：可以买卖资产
   - 慈善：根据孩子数量获得奖励
   - 裁员：暂时失去工资收入
   - 生孩子：增加支出但有慈善收益

4. 卡片类型：
   - 企业卡：高投入高回报的企业投资
   - 机会卡：各种房地产和商业投资
   - 金融卡：股票、基金等金融产品
   - 副业卡：小投入快回报的副业
        """
        messagebox.showinfo("游戏规则", rules)
    
    def show_about(self):
        """显示关于信息"""
        about = """
财富流游戏 v1.0

基于《富爸爸穷爸爸》理念的财务教育游戏
帮助玩家学习投资和理财知识

开发者：AI助手
框架：Python + Tkinter
        """
        messagebox.showinfo("关于", about)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()


class PlayerSetupDialog:
    """玩家设置对话框"""
    
    def __init__(self, parent, professions):
        self.result = None
        self.professions = professions
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("玩家设置")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """设置对话框"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 玩家数量
        ttk.Label(main_frame, text="玩家数量:").grid(row=0, column=0, sticky="w", pady=5)
        self.player_count = tk.IntVar(value=2)
        player_spinbox = ttk.Spinbox(main_frame, from_=2, to=6, textvariable=self.player_count)
        player_spinbox.grid(row=0, column=1, sticky="ew", pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="确定", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
    
    def ok_clicked(self):
        """确定按钮点击"""
        count = self.player_count.get()
        self.result = []
        
        for i in range(count):
            # 简单设置，使用默认职业
            profession = self.professions[i % len(self.professions)]
            player_data = {
                'name': f"玩家{i+1}",
                'profession': profession['name'],
                'salary': profession['salary'],
                'cash': profession['initial_cash'],
                'expenses': profession['initial_expenses']
            }
            self.result.append(player_data)
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """取消按钮点击"""
        self.result = None
        self.dialog.destroy()


# 数学函数
def cos(angle):
    """余弦函数"""
    import math
    return math.cos(angle)

def sin(angle):
    """正弦函数"""
    import math
    return math.sin(angle) 