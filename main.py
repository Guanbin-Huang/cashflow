#!/usr/bin/env python3
"""
财富流游戏主程序 - Cash Flow Game Main Entry
基于《富爸爸穷爸爸》理念的财务教育游戏

文件功能概述：
==============
本文件是整个财富流游戏的主入口点，负责游戏的启动、初始化和玩家设置。
提供了一个完整的图形化启动器界面，让用户可以方便地配置游戏参数并开始游戏。

主要组件：
----------
1. GameLauncher类 - 主启动器窗口
   - 提供友好的图形化界面
   - 玩家数量设置（2-6人）
   - 快速开始和详细设置选项
   - 游戏规则说明展示
   - 职业数据加载和管理

2. PlayerSetupDialog类 - 玩家设置对话框
   - 详细的玩家信息配置
   - 姓名和职业选择
   - 滚动界面支持多玩家设置

核心功能：
----------
- 游戏环境检查和依赖验证
- 数据目录初始化
- 职业数据加载（支持JSON文件和默认数据）
- 玩家数据配置和验证
- 游戏引擎启动和主窗口切换
- 错误处理和用户友好的错误提示

技术特点：
----------
- 基于Tkinter的跨平台GUI
- 支持命令行参数处理
- 完整的错误处理机制
- 可配置的职业数据系统
- 响应式界面设计

使用方式：
----------
直接运行: python main.py
命令行帮助: python main.py --help
测试模式: python main.py --test

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

import sys
import os
import json
import traceback
import tkinter as tk
from tkinter import ttk, messagebox

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 常量配置
WINDOW_CONFIG = {
    'title': '财富流游戏启动器',
    'geometry': '650x550',
    'min_size': (500, 400),
    'icon_title': '🎯 财富流游戏'
}

DEFAULT_PROFESSIONS = [
    {"id": "engineer", "name": "工程师", "salary": 5000, "initial_cash": 10000, "initial_expenses": 2500},
    {"id": "teacher", "name": "教师", "salary": 4000, "initial_cash": 8000, "initial_expenses": 2000},
    {"id": "doctor", "name": "医生", "salary": 8000, "initial_cash": 15000, "initial_expenses": 4000},
    {"id": "lawyer", "name": "律师", "salary": 7000, "initial_cash": 12000, "initial_expenses": 3500},
    {"id": "manager", "name": "经理", "salary": 6000, "initial_cash": 11000, "initial_expenses": 3000},
    {"id": "nurse", "name": "护士", "salary": 3500, "initial_cash": 7000, "initial_expenses": 1800}
]

GAME_INFO = """🎯 游戏目标：让你的被动收入超过月支出，实现财务自由！

🎮 游戏流程：投骰子移动 → 处理格子事件 → 决定投资 → 管理资产

💡 格子类型：发薪水、机会、意外支出、市场、特殊事件

🃏 卡片类型：企业卡、机会卡、金融卡、副业卡

🏆 胜利条件：被动收入 >= 月支出时获得财务自由！"""

def check_dependencies():
    """检查必要的依赖"""
    try:
        import tkinter
        return True
    except ImportError:
        messagebox.showerror("错误", "缺少必要的依赖包：tkinter")
        return False

def ensure_data_dir():
    """确保数据目录存在"""
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

class GameLauncher:
    """游戏启动器 - 简化版本"""
    
    def __init__(self):
        self.root = self._setup_window()
        self.professions = self._load_professions()
        self._create_ui()
        
    def _setup_window(self):
        """设置主窗口"""
        root = tk.Tk()
        root.title(WINDOW_CONFIG['title'])
        root.geometry(WINDOW_CONFIG['geometry'])
        root.minsize(*WINDOW_CONFIG['min_size'])  # 设置最小尺寸，允许调整大小
        
        # 居中显示
        root.update_idletasks()
        x = (root.winfo_screenwidth() - 650) // 2
        y = (root.winfo_screenheight() - 550) // 2
        root.geometry(f"650x550+{x}+{y}")
        
        # 聚焦设置
        root.lift()
        root.focus_force()
        
        return root
    
    def _load_professions(self):
        """加载职业数据"""
        try:
            data_path = os.path.join(project_root, "data", "professions.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)['professions']
        except Exception:
            return DEFAULT_PROFESSIONS
    
    def _create_ui(self):
        """创建用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        self._create_header(main_frame)
        
        # 设置区域
        setup_frame = ttk.LabelFrame(main_frame, text="游戏设置", padding="15")
        setup_frame.pack(fill=tk.X, pady=(0, 15))
        self._create_settings(setup_frame)
        
        # 开始按钮
        ttk.Button(main_frame, text="🚀 开始游戏", 
                  command=self.start_game).pack(pady=10)
        
        # 游戏说明
        self._create_info_section(main_frame)
    
    def _create_header(self, parent):
        """创建标题区域"""
        ttk.Label(parent, text=WINDOW_CONFIG['icon_title'], 
                 font=("Arial", 20, "bold")).pack(pady=(0, 5))
        ttk.Label(parent, text="基于《富爸爸穷爸爸》理念的财务教育游戏",
                 font=("Arial", 11)).pack(pady=(0, 20))
    
    def _create_settings(self, parent):
        """创建设置区域"""
        # 玩家数量
        player_frame = ttk.Frame(parent)
        player_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(player_frame, text="玩家数量:").pack(side=tk.LEFT)
        self.player_count = tk.IntVar(value=2)
        ttk.Spinbox(player_frame, from_=2, to=6, textvariable=self.player_count, 
                   width=5).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(player_frame, text="(2-6人)", 
                 foreground="gray").pack(side=tk.LEFT)
        
        # 快速开始选项
        self.quick_start = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="快速开始（使用默认职业）", 
                       variable=self.quick_start).pack(anchor=tk.W)
    
    def _create_info_section(self, parent):
        """创建游戏说明区域"""
        info_frame = ttk.LabelFrame(parent, text="游戏说明", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建可滚动的文本区域
        text_widget = tk.Text(info_frame, wrap=tk.WORD, height=8, 
                             font=("Arial", 9), state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, 
                                 command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 插入文本
        text_widget.configure(state=tk.NORMAL)
        text_widget.insert(tk.END, GAME_INFO)
        text_widget.configure(state=tk.DISABLED)
        
        # 布局
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_game(self):
        """开始游戏"""
        try:
            player_count = self.player_count.get()
            
            if self.quick_start.get():
                players_data = self._create_quick_players(player_count)
            else:
                players_data = self._get_detailed_setup(player_count)
                if not players_data:
                    return
            
            self._launch_game(players_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败: {e}")
    
    def _create_quick_players(self, count):
        """创建快速开始的玩家"""
        return [{
            'name': f"玩家{i+1}",
            'profession': self.professions[i % len(self.professions)]['name'],
            'salary': self.professions[i % len(self.professions)]['salary'],
            'cash': self.professions[i % len(self.professions)]['initial_cash'],
            'expenses': self.professions[i % len(self.professions)]['initial_expenses']
        } for i in range(count)]
    
    def _get_detailed_setup(self, count):
        """获取详细玩家设置"""
        dialog = PlayerSetupDialog(self.root, self.professions, count)
        self.root.wait_window(dialog.dialog)
        return dialog.result
    
    def _launch_game(self, players_data):
        """启动主游戏"""
        try:
            from ui.main_window import MainWindow
            from game import GameEngine
            
            self.root.destroy()
            
            # 检查棋盘配置文件
            config_file = os.path.join(project_root, "data", "board_config.json")
            if not os.path.exists(config_file):
                config_file = None
                print("未找到棋盘配置文件，使用默认配置")
            
            app = MainWindow()
            app.game_engine = GameEngine(players_data, config_file)
            success, message = app.game_engine.start_game()
            
            if success:
                app.update_ui()
                app.log_message("🎮 游戏开始！")
                messagebox.showinfo("游戏开始", "游戏已成功启动！")
            else:
                messagebox.showerror("错误", f"游戏启动失败: {message}")
            
            app.run()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动主游戏失败: {e}")
            traceback.print_exc()
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()

class PlayerSetupDialog:
    """玩家设置对话框 - 简化版本"""
    
    def __init__(self, parent, professions, player_count):
        self.result = None
        self.professions = professions
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("玩家设置")
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._center_dialog()
        self._create_dialog_ui(player_count)
    
    def _center_dialog(self):
        """居中显示对话框"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - 450) // 2
        y = (self.dialog.winfo_screenheight() - 350) // 2
        self.dialog.geometry(f"450x350+{x}+{y}")
    
    def _create_dialog_ui(self, player_count):
        """创建对话框界面"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="玩家设置", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 15))
        
        # 创建滚动区域
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建玩家输入区域
        self.player_entries = []
        prof_names = [p['name'] for p in self.professions]
        
        for i in range(player_count):
            frame = ttk.LabelFrame(scrollable_frame, text=f"玩家 {i+1}", padding="8")
            frame.pack(fill=tk.X, pady=3)
            
            # 姓名输入
            name_frame = ttk.Frame(frame)
            name_frame.pack(fill=tk.X, pady=1)
            ttk.Label(name_frame, text="姓名:").pack(side=tk.LEFT)
            name_entry = ttk.Entry(name_frame)
            name_entry.insert(0, f"玩家{i+1}")
            name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
            
            # 职业选择
            prof_frame = ttk.Frame(frame)
            prof_frame.pack(fill=tk.X, pady=1)
            ttk.Label(prof_frame, text="职业:").pack(side=tk.LEFT)
            prof_combo = ttk.Combobox(prof_frame, values=prof_names, state="readonly")
            prof_combo.set(prof_names[i % len(prof_names)])
            prof_combo.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
            
            self.player_entries.append({'name': name_entry, 'profession': prof_combo})
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(btn_frame, text="取消", command=self._cancel).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="确定", command=self._confirm).pack(side=tk.RIGHT, padx=(0, 5))
    
    def _confirm(self):
        """确认设置"""
        self.result = []
        
        for entry in self.player_entries:
            name = entry['name'].get().strip()
            prof_name = entry['profession'].get()
            
            if not name:
                messagebox.showerror("错误", "请填写所有玩家的姓名")
                return
            
            profession = next((p for p in self.professions if p['name'] == prof_name), 
                            self.professions[0])
            
            self.result.append({
                'name': name,
                'profession': profession['name'],
                'salary': profession['salary'],
                'cash': profession['initial_cash'],
                'expenses': profession['initial_expenses']
            })
        
        self.dialog.destroy()
    
    def _cancel(self):
        """取消设置"""
        self.result = None
        self.dialog.destroy()

def main():
    """主函数 - 简化版本"""
    args = sys.argv[1:]
    
    if '-h' in args or '--help' in args:
        print("财富流游戏 - 基于《富爸爸穷爸爸》理念的财务教育游戏")
        print("用法: python main.py")
        return
    
    if '-t' in args or '--test' in args:
        print("测试模式暂未实现")
        return
    
    # 启动GUI启动器
    if not check_dependencies():
        return
    
    ensure_data_dir()
    
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        messagebox.showerror("错误", f"启动器错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 