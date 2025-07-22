"""
财富流游戏主窗口 - Main Game Window
基于Tkinter的桌面应用界面

文件功能概述：
==============
本文件实现了财富流游戏的主要图形用户界面，提供了完整的桌面应用
体验。包括游戏控制、棋盘显示、玩家信息展示和游戏日志等功能模块，
是玩家与游戏交互的主要入口。

主要组件：
----------
1. MainWindow类 - 主游戏窗口管理器
   - 整体窗口布局和组件协调
   - 游戏引擎集成和状态同步
   - 用户交互事件处理

2. 界面布局模块：
   - create_menu(): 创建菜单栏
   - create_control_panel(): 游戏控制面板
   - create_game_board(): 棋盘显示区域
   - create_player_panel(): 玩家信息面板
   - create_log_panel(): 游戏日志面板

3. PlayerSetupDialog类 - 玩家设置对话框
   - 游戏开始前的玩家配置
   - 支持多玩家设置
   - 职业选择和参数配置

核心功能：
----------
- 游戏控制界面
  * 投骰子、移动、结束回合按钮
  * 卡片决策处理（购买/放弃）
  * 市场操作控制
  * 层级转换显示

- 三层圈棋盘可视化
  * 内圈Z字形布局绘制
  * 中圈和外圈圆形布局
  * 玩家位置实时显示
  * 格子类型视觉区分
  * 层级转换连线显示

- 玩家信息管理
  * 实时财务状况显示
  * 现金、被动收入、支出跟踪
  * 当前玩家高亮显示
  * 层级信息展示

- 游戏日志系统
  * 实时游戏事件记录
  * 滚动显示最新消息
  * 操作结果反馈

技术特点：
----------
- 基于Tkinter的跨平台GUI
- 响应式布局设计
- 自定义Canvas绘图系统
- 事件驱动的界面更新
- 完整的用户交互处理

界面设计特色：
--------------
- 直观的三层圈棋盘可视化
- 友好的用户操作体验
- 实时的游戏状态反馈
- 清晰的信息层次结构
- 专业的游戏界面美观度

绘图算法：
----------
- 圆形布局数学计算
- Z字形路径坐标计算
- 动态Canvas尺寸适应
- 玩家标记位置算法
- 格子类型颜色映射

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
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
        
        # 调试模式框架
        debug_frame = ttk.LabelFrame(control_frame, text="调试模式")
        debug_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 调试模式开关
        self.debug_mode_var = tk.BooleanVar()
        self.debug_checkbox = ttk.Checkbutton(debug_frame, text="启用调试模式", 
                                            variable=self.debug_mode_var,
                                            command=self.toggle_debug_mode)
        self.debug_checkbox.pack(pady=5)
        
        # 调试控制框架（初始隐藏）
        self.debug_control_frame = ttk.Frame(debug_frame)
        
        # 玩家选择
        ttk.Label(self.debug_control_frame, text="控制玩家:").grid(row=0, column=0, sticky="w", padx=5)
        self.debug_player_var = tk.StringVar()
        self.debug_player_combo = ttk.Combobox(self.debug_control_frame, textvariable=self.debug_player_var,
                                             width=12, state="readonly")
        self.debug_player_combo.grid(row=0, column=1, padx=5)
        
        # 骰子点数输入
        ttk.Label(self.debug_control_frame, text="骰子点数:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.debug_dice_var = tk.IntVar(value=1)
        self.debug_dice_spin = ttk.Spinbox(self.debug_control_frame, from_=1, to=6, 
                                         textvariable=self.debug_dice_var, width=10)
        self.debug_dice_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # 分隔符
        ttk.Separator(control_frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
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
        
        # 层级转换框架
        self.layer_frame = ttk.LabelFrame(control_frame, text="层级信息")
        self.layer_frame.pack(fill=tk.X, pady=10)
        
        self.layer_info_label = ttk.Label(self.layer_frame, text="当前层级: 平流层(中圈)", wraplength=200)
        self.layer_info_label.pack(pady=5)
        
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
        self.player_tree = ttk.Treeview(player_frame, columns=("现金", "被动收入", "支出", "层级"), 
                                      show="tree headings", height=10)
        self.player_tree.heading("#0", text="玩家")
        self.player_tree.heading("现金", text="现金")
        self.player_tree.heading("被动收入", text="被动收入")
        self.player_tree.heading("支出", text="支出")
        self.player_tree.heading("层级", text="层级")
        
        self.player_tree.column("#0", width=100)
        self.player_tree.column("现金", width=80)
        self.player_tree.column("被动收入", width=80)
        self.player_tree.column("支出", width=80)
        self.player_tree.column("层级", width=60)
        
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
            # 更新调试模式玩家列表
            self.update_debug_player_list()
            messagebox.showinfo("游戏开始", message)
        else:
            messagebox.showerror("错误", message)
    
    def toggle_debug_mode(self):
        """切换调试模式"""
        if self.debug_mode_var.get():
            # 启用调试模式
            self.debug_control_frame.pack(fill=tk.X, pady=5)
            if self.game_engine:
                self.game_engine.debug_mode = True
                self.update_debug_player_list()
            self.log_message("调试模式已启用")
        else:
            # 禁用调试模式
            self.debug_control_frame.pack_forget()
            if self.game_engine:
                self.game_engine.debug_mode = False
            self.log_message("调试模式已禁用")
    
    def update_debug_player_list(self):
        """更新调试模式玩家列表"""
        if not self.game_engine:
            return
        
        player_names = [f"{i+1}. {player.name}" for i, player in enumerate(self.game_engine.players)]
        self.debug_player_combo['values'] = player_names
        if player_names:
            self.debug_player_combo.current(0)  # 默认选择第一个玩家
    
    def get_players_setup(self):
        """获取玩家设置"""
        dialog = PlayerSetupDialog(self.root, self.professions)
        self.root.wait_window(dialog.dialog)
        return dialog.result
    
    def roll_dice(self):
        """投骰子"""
        if self.game_engine:
            # 检查是否在调试模式且控制当前玩家
            if (self.debug_mode_var.get() and 
                self.game_engine.debug_mode and 
                self.debug_player_combo.get()):
                
                # 获取选中的玩家索引
                selected_text = self.debug_player_combo.get()
                if selected_text:
                    selected_index = int(selected_text.split('.')[0]) - 1
                    current_index = self.game_engine.current_player_index
                    
                    # 如果选中的玩家是当前玩家，使用调试模式骰子点数
                    if selected_index == current_index:
                        debug_dice = self.debug_dice_var.get()
                        success, message = self.game_engine.roll_dice_debug(debug_dice)
                        if success:
                            self.dice_label.config(text=f"🎲 {debug_dice} (调试)")
                            self.log_message(f"{message} (调试模式)")
                            self.update_ui()
                        return
            
            # 正常投骰子
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
    
    def change_layer(self, target_layer):
        """处理层级转换 - 现在为私有方法，由系统自动调用"""
        if not self.game_engine:
            return
            
        # 注意：此方法已不再由按钮调用，仅由系统内部使用
        success, message = self.game_engine.handle_layer_transition(target_layer)
        if success:
            self.log_message(message)
            self.update_ui()
            self.draw_board()  # 重绘棋盘显示玩家新位置
    
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
        
        # 层级转换现在是自动的，不需要按钮
        
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
            
            # 获取玩家所在层级
            layer_name = getattr(player, "active_layer", "middle")
            layer_display = {"inner": "内圈", "middle": "中圈", "outer": "外圈"}
            layer_text = layer_display.get(layer_name, "中圈")
            
            values = (player.cash, player.passive_income, player.expenses, layer_text)
            self.player_tree.insert("", "end", text=name, values=values)
            
        # 更新层级信息标签
        current_player = self.game_engine.get_current_player()
        if current_player:
            layer_name = getattr(current_player, "active_layer", "middle")
            layer_display = {"inner": "逆流层(内圈)", "middle": "平流层(中圈)", "outer": "顺流层(外圈)"}
            self.layer_info_label.config(text=f"当前层级: {layer_display.get(layer_name, '平流层(中圈)')}")
    
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
        
        # 三个圆的半径
        inner_radius = min(canvas_width, canvas_height) // 5  # 内圈 - 绿色
        middle_radius = min(canvas_width, canvas_height) // 3  # 中圈 - 红色
        outer_radius = min(canvas_width, canvas_height) // 2.2  # 外圈 - 蓝色
        
        # 绘制三个圆环背景
        # 外圈 - 顺流层 (蓝色)
        self.board_canvas.create_oval(
            center_x - outer_radius, center_y - outer_radius,
            center_x + outer_radius, center_y + outer_radius,
            outline="lightblue", width=2, fill="#e6f7ff"  # 淡蓝色背景
        )
        
        # 中圈 - 平流层 (红色)
        self.board_canvas.create_oval(
            center_x - middle_radius, center_y - middle_radius,
            center_x + middle_radius, center_y + middle_radius,
            outline="red", width=2, fill="#ffe6e6"  # 淡红色背景
        )
        
        # 内圈 - 逆流层 (绿色)
        self.board_canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            outline="green", width=2, fill="#e6ffe6"  # 淡绿色背景
        )
        
        # 添加圈层标签
        self.board_canvas.create_text(center_x, center_y - outer_radius - 15, 
                                  text="顺流层 (外圈)", font=("Arial", 10, "bold"), fill="blue")
        self.board_canvas.create_text(center_x, center_y - middle_radius - 15, 
                                  text="平流层 (中圈)", font=("Arial", 10, "bold"), fill="red")
        self.board_canvas.create_text(center_x, center_y - inner_radius - 15, 
                                  text="逆流层 (内圈)", font=("Arial", 10, "bold"), fill="green")
        
        if not self.game_engine:
            # 没有游戏引擎，只绘制基础圆形
            return
            
        # 获取各层格子数量
        inner_size = self.game_engine.board.get_circle_size("inner")
        middle_size = self.game_engine.board.get_circle_size("middle")
        outer_size = self.game_engine.board.get_circle_size("outer")
        
        # 绘制三个圈的格子
        layers = [
            {"name": "outer", "radius": outer_radius, "size": outer_size, "color": "lightblue"},
            {"name": "middle", "radius": middle_radius, "size": middle_size, "color": "red"},
            {"name": "inner", "radius": inner_radius, "size": inner_size, "color": "green"}
        ]
        
        # 绘制层级转换连线
        # 内圈位置1与中圈位置18绘制连线
        inner_pos_1 = self.get_inner_layer_position(center_x, center_y, inner_radius, 1)
        middle_pos_18_angle = 2 * 3.14159 * 18 / middle_size
        middle_pos_18_x = center_x + middle_radius * cos(middle_pos_18_angle)
        middle_pos_18_y = center_y + middle_radius * sin(middle_pos_18_angle)
        
        # 绘制内圈1与中圈18之间的连线
        self.board_canvas.create_line(inner_pos_1[0], inner_pos_1[1], middle_pos_18_x, middle_pos_18_y, 
                                  fill="purple", width=2, dash=(4, 4))
        
        # 内圈位置9与中圈位置6绘制连线
        inner_pos_9 = self.get_inner_layer_position(center_x, center_y, inner_radius, 9)
        middle_pos_6_angle = 2 * 3.14159 * 6 / middle_size
        middle_pos_6_x = center_x + middle_radius * cos(middle_pos_6_angle)
        middle_pos_6_y = center_y + middle_radius * sin(middle_pos_6_angle)
        
        # 绘制内圈9与中圈6之间的连线
        self.board_canvas.create_line(inner_pos_9[0], inner_pos_9[1], middle_pos_6_x, middle_pos_6_y, 
                                  fill="purple", width=2, dash=(4, 4))
        
        # 绘制各层格子
        for layer in layers:
            layer_name = layer["name"]
            radius = layer["radius"]
            size = layer["size"]
            color = layer["color"]
            
            if layer_name == "inner":
                # 内层使用Z字形布局
                self.draw_inner_layer_z_shape(center_x, center_y, inner_radius, size, color)
            else:
                # 其他层使用圆形布局
                for i in range(size):
                    angle = 2 * 3.14159 * i / size
                    x = center_x + radius * cos(angle)
                    y = center_y + radius * sin(angle)
                    
                    # 获取格子类型
                    square = self.game_engine.board.get_square(i, layer_name)
                    
                    # 根据格子类型选择颜色
                    fill_color = "white"
                    
                    # 绘制格子
                    self.board_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                              fill=fill_color, outline=color)
                    
                    # 绘制格子编号
                    self.board_canvas.create_text(x, y, text=str(i))
        
        # 绘制玩家位置
        for i, player in enumerate(self.game_engine.players):
            # 确定玩家所在圈层
            player_layer = getattr(player, "active_layer", "middle")
            
            if player_layer == "inner":
                # 内层使用Z字形坐标
                x, y = self.get_inner_layer_position(center_x, center_y, inner_radius, player.position)
            else:
                # 其他层使用圆形坐标
                # 根据圈层选择半径
                if player_layer == "outer":
                    radius = outer_radius
                    size = outer_size
                else:  # middle
                    radius = middle_radius
                    size = middle_size
                    
                # 计算角度和位置
                angle = 2 * 3.14159 * player.position / size
                x = center_x + radius * cos(angle)
                y = center_y + radius * sin(angle)
            
            # 玩家标记
            player_colors = ["red", "green", "blue", "yellow", "purple", "orange"]
            color = player_colors[i % len(player_colors)]
            
            self.board_canvas.create_oval(x-8, y-8, x+8, y+8, 
                                      fill=color, outline="black")
            self.board_canvas.create_text(x, y, text=str(i+1), fill="white")
    
    def get_inner_layer_position(self, center_x, center_y, inner_radius, position):
        """获取内层Z字形指定位置的坐标"""
        # Z字形路径的坐标点 (和draw_inner_layer_z_shape方法中的一致)
        z_positions = [
            # 空占位，因为我们从1开始编号
            (0, 0),  # 0: 不使用
            
            # 第一行：1-4 (从左到右)
            (-inner_radius * 0.6, -inner_radius * 0.4),  # 1: 左上
            (-inner_radius * 0.2, -inner_radius * 0.4),  # 2
            (inner_radius * 0.2, -inner_radius * 0.4),   # 3
            (inner_radius * 0.6, -inner_radius * 0.4),   # 4: 右上
            
            # 中间：5 (星号* - 转换点)
            (0, 0),                                     # 5: 中心点
            
            # 第二行：6-9 (从左到右)
            (-inner_radius * 0.6, inner_radius * 0.4),   # 6: 左下
            (-inner_radius * 0.2, inner_radius * 0.4),   # 7
            (inner_radius * 0.2, inner_radius * 0.4),    # 8
            (inner_radius * 0.6, inner_radius * 0.4),    # 9: 右下
        ]
        
        if 0 <= position < len(z_positions):
            x_offset, y_offset = z_positions[position]
            return center_x + x_offset, center_y + y_offset
        else:
            # 如果位置超出范围，返回中心点
            return center_x, center_y
    
    def draw_inner_layer_z_shape(self, center_x, center_y, inner_radius, size, color):
        """绘制内层Z字形格子布局"""
        # Z字形路径的坐标点 (相对于中心点的偏移)
        # 新布局: 
        # 第一行: 1 2 3 4
        # 中间: 5 (星号位置)
        # 第二行: 6 7 8 9
        z_positions = [
            # 空占位，因为我们从1开始编号
            (0, 0),  # 0: 不使用
            
            # 第一行：1-4 (从左到右)
            (-inner_radius * 0.6, -inner_radius * 0.4),  # 1: 左上
            (-inner_radius * 0.2, -inner_radius * 0.4),  # 2
            (inner_radius * 0.2, -inner_radius * 0.4),   # 3
            (inner_radius * 0.6, -inner_radius * 0.4),   # 4: 右上
            
            # 中间：5 (星号* - 转换点)
            (0, 0),                                     # 5: 中心点
            
            # 第二行：6-9 (从左到右)
            (-inner_radius * 0.6, inner_radius * 0.4),   # 6: 左下
            (-inner_radius * 0.2, inner_radius * 0.4),   # 7
            (inner_radius * 0.2, inner_radius * 0.4),    # 8
            (inner_radius * 0.6, inner_radius * 0.4),    # 9: 右下
        ]
        
        # 连接线 - 首先连接1-4
        for i in range(1, 4):
            x1_offset, y1_offset = z_positions[i]
            x2_offset, y2_offset = z_positions[i+1]
            x1, y1 = center_x + x1_offset, center_y + y1_offset
            x2, y2 = center_x + x2_offset, center_y + y2_offset
            
            self.board_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        # 连接线 - 连接4到5
        x1_offset, y1_offset = z_positions[4]
        x2_offset, y2_offset = z_positions[5]
        x1, y1 = center_x + x1_offset, center_y + y1_offset
        x2, y2 = center_x + x2_offset, center_y + y2_offset
        self.board_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        # 连接线 - 连接5到6
        x1_offset, y1_offset = z_positions[5]
        x2_offset, y2_offset = z_positions[6]
        x1, y1 = center_x + x1_offset, center_y + y1_offset
        x2, y2 = center_x + x2_offset, center_y + y2_offset
        self.board_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        # 连接线 - 连接6-9
        for i in range(6, 9):
            x1_offset, y1_offset = z_positions[i]
            x2_offset, y2_offset = z_positions[i+1]
            x1, y1 = center_x + x1_offset, center_y + y1_offset
            x2, y2 = center_x + x2_offset, center_y + y2_offset
            
            self.board_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        # 绘制格子 - 跳过索引0，从1开始
        for i in range(1, min(size + 1, len(z_positions))):
            x_offset, y_offset = z_positions[i]
            x = center_x + x_offset
            y = center_y + y_offset
            
            # 获取格子类型
            square = self.game_engine.board.get_square(i, "inner")
            
            # 根据格子类型选择颜色
            fill_color = "white"
            
            # 为星号格子(5)添加特殊标记
            if i == 5:
                fill_color = "gold"
                
            # 绘制格子
            self.board_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                      fill=fill_color, outline=color, width=2)
            
            # 绘制格子编号
            if i == 5:
                self.board_canvas.create_text(x, y, text="★", font=("Arial", 12, "bold"))
            else:
                self.board_canvas.create_text(x, y, text=str(i), font=("Arial", 10, "bold"))
    
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