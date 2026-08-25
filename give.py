import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os
# 添加py_files到Python路径
import sys
import os

if not getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(__file__)
    py_files_path = os.path.join(base_dir, 'py_files')
    sys.path.append(py_files_path)
    sys.path.append(base_dir)

from banner_generator import BannerGeneratorTab
from fireworks_generator import FireworksTab
from skull_generator import SkullGeneratorTab
from food_generator import FoodGeneratorTab
from potion_effects import PotionEffectsTab
from tool_generator import ToolGeneratorTab
from equippable_generator import EquippableGeneratorTab
from written_book_generator import WrittenBookGeneratorTab
from component_mapper import (
    format_enchantments_component,
    format_custom_name_component,
    format_lore_component,
    format_attribute_modifiers_component,
    format_potion_contents_component,
    format_fireworks_component,
    format_food_component,
    format_consumable_component,
    format_other_components,
    format_banner_component,
    format_tool_component,
    format_written_book_component
)

class MinecraftGiveGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Give指令生成器")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.root.maxsize(1600, 1000)
        
        # 窗口居中显示
        self.root.after(100, self.center_window)
        
        # 存储动态添加的附魔和属性修饰符
        self.enchantments = []
        self.attributes = []
        
        # 物品ID映射表
        self.item_id_map = {}
        
        # 附魔ID映射表
        self.enchant_map = {}
        
        # 方块ID映射表
        self.block_id_map = {}
        
        # 实体ID映射表
        self.entity_id_map = {}
        
        # 加载物品ID列表和附魔ID列表
        self.load_item_ids()
        self.load_enchant_ids()
        self.load_block_ids()
        self.load_entity_ids()
        
        # 药水效果标签页实例
        self.potion_tab = None
        
        # 烟花火箭标签页实例
        self.fireworks_tab = None

        # 头颅生成器标签页实例
        self.skull_tab = None
        
        # 食物生成器标签页实例
        self.food_tab = None
        
        # 旗帜生成器标签页实例
        self.banner_tab = None
        
        # 工具属性标签页实例
        self.tool_tab = None
        
        # 装备属性标签页实例
        self.equippable_tab = None
        
        # 成书生成器标签页实例
        self.written_book_tab = None
        
        # 创建自定义样式 - 使用深色配色方案
        style = ttk.Style()
        
        # 主窗口背景 - 使用深灰色
        self.root.configure(bg="#e5e7eb")
        
        # 小字体按钮样式
        style.configure("Small.TButton", font=('SimHei', 8), padding=2)
        
        # 标题样式
        style.configure("Title.TLabel", font=('SimHei', 10, 'bold'), foreground="#1f2937")
        
        # 普通标签样式
        style.configure("TLabel", font=('SimHei', 9), foreground="#374151")
        
        # 框架样式
        style.configure("Custom.TFrame", padding=12, relief="flat", background="#e5e7eb")
        
        # 分组框架样式
        style.configure("TLabelframe", background="#f3f4f6", padding=12, relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", font=('SimHei', 10, 'bold'), foreground="#1f2937", padding=(8, 4, 8, 4))
        
        # 标签页样式
        style.configure("Custom.TNotebook", padding=3, background="#e5e7eb")
        style.configure("Custom.TNotebook.Tab", padding=(10, 5), font=('SimHei', 9), background="#d1d5db", foreground="#374151")
        style.map("Custom.TNotebook.Tab", 
                 background=[("selected", "#f3f4f6"), ("active", "#e5e7eb")],
                 foreground=[("selected", "#1f2937"), ("active", "#1f2937")])
        
        # 输入框样式
        style.configure("TEntry", padding=6, font=('SimHei', 9), fieldbackground="#ffffff")
        
        # 下拉框样式
        style.configure("TCombobox", padding=6, font=('SimHei', 9), fieldbackground="#ffffff")
        
        # 按钮样式 - 确保符合WCAG 2.1 AA级标准（对比度≥4.5:1）
        style.configure("TButton", padding=8, font=('SimHei', 9), background="#2563eb", foreground="#263238")
        style.map("TButton", 
                 background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])
        
        # 复选框样式
        style.configure("TCheckbutton", font=('SimHei', 9), foreground="#4a5568")
        
        # 单选按钮样式
        style.configure("TRadiobutton", font=('SimHei', 9), foreground="#4a5568")
        
        # 分隔线样式
        style.configure("TSeparator", background="#e2e8f0")
        
        self.create_widgets()
    
    def center_window(self):
        """将窗口居中显示在屏幕上"""
        self.root.update_idletasks()
        
        # 获取窗口的宽度和高度
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 获取屏幕的宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算窗口居中的位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def check_window_position(self):
        """检查窗口位置，确保窗口不在任务栏下面"""
        self.root.update_idletasks()
        
        # 获取屏幕的宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口的宽度
        window_width = self.root.winfo_width()
        
        # 计算窗口居中的位置
        x = (screen_width - window_width) // 2
        
        # 窗口紧贴屏幕顶部
        y = 0  # 窗口顶部紧贴屏幕顶部
        
        # 设置窗口位置和大小
        self.root.geometry(f"+{x}+{y}")
    
    def create_main_content_widgets(self):
        """在主内容区域创建物品配置和命令生成控件"""
        # 顶部配置区域 - 紧凑布局
        config_frame = ttk.LabelFrame(self.main_content, text="物品配置", padding=8)
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 物品选择 - 减少间距
        ttk.Label(config_frame, text="物品:", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=3, padx=3)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(config_frame, textvariable=self.item_var, width=55)
        self.item_combo['values'] = list(self.item_id_map.keys())
        self.item_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=3, padx=3)
        self.item_combo.bind('<<ComboboxSelected>>', self.on_item_selected)
        self.item_combo.bind('<KeyRelease>', self.on_item_search)
        
        # 物品ID输入框 - 减少间距
        ttk.Label(config_frame, text="物品ID:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=3, padx=3)
        self.item_id_var = tk.StringVar()
        self.item_id = ttk.Entry(config_frame, textvariable=self.item_id_var, width=55)
        self.item_id.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=3, padx=3)
        self.item_id.bind('<KeyRelease>', self.on_item_id_changed)
        
        # 数量输入 - 减少间距
        ttk.Label(config_frame, text="数量:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=3, padx=3)
        self.count_var = tk.StringVar(value="1")
        count_entry = ttk.Entry(config_frame, textvariable=self.count_var, width=15)
        count_entry.grid(row=2, column=1, sticky=tk.W, pady=3, padx=3)
        
        # 命令生成区域 - 紧凑布局
        command_frame = ttk.LabelFrame(self.main_content, text="命令生成", padding=8)
        command_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 生成命令按钮 - 减少间距
        generate_button = ttk.Button(command_frame, text="生成Give命令", command=self.generate_command)
        generate_button.grid(row=0, column=0, pady=5, padx=3, sticky=tk.W)
        
        # 命令显示框和复制按钮 - 减少高度
        ttk.Label(command_frame, text="生成的命令:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=3, padx=3)
        command_display_frame = ttk.Frame(command_frame, borderwidth=1, relief="solid", style="Custom.TFrame")
        command_display_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3, padx=3)
        
        self.command_text = tk.Text(command_display_frame, height=4, width=75, font=('Courier New', 9), bg="#f7fafc", borderwidth=0, highlightthickness=0)
        self.command_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # 复制按钮 - 小字显示在旁边
        copy_button = ttk.Button(command_display_frame, text="复制", command=self.copy_command, style="Small.TButton")
        copy_button.pack(side=tk.RIGHT, padx=5, pady=3, fill=tk.Y)
        
        # 配置权重
        config_frame.columnconfigure(1, weight=1)
        command_frame.columnconfigure(1, weight=1)
        self.main_content.columnconfigure(0, weight=1)
    
    def create_tabs(self):
        """创建标签页内容"""
        # 显示属性标签页
        display_container, display_frame = self.create_scrollable_frame()
        self.notebook.add(display_container, text="显示属性")
        self.create_display_tab(display_frame)
        
        # 附魔标签页
        enchant_container, enchant_frame = self.create_scrollable_frame()
        self.notebook.add(enchant_container, text="附魔")
        self.create_enchant_tab(enchant_frame)
        
        # 属性修饰符标签页
        attribute_container, attribute_frame = self.create_scrollable_frame()
        self.notebook.add(attribute_container, text="属性修饰符")
        self.create_attribute_tab(attribute_frame)
        
        # 药水效果标签页
        potion_container, potion_frame = self.create_scrollable_frame()
        self.notebook.add(potion_container, text="药水效果")
        self.potion_tab = PotionEffectsTab(potion_frame)
        
        # 烟花火箭标签页
        fireworks_container, fireworks_frame = self.create_scrollable_frame()
        self.notebook.add(fireworks_container, text="烟花火箭")
        self.fireworks_tab = FireworksTab(fireworks_frame)
        
        # 头颅生成器标签页
        skull_container, skull_frame = self.create_scrollable_frame()
        self.notebook.add(skull_container, text="头颅生成器")
        self.skull_tab = SkullGeneratorTab(skull_frame)
        
        # 食物生成器标签页
        food_container, food_frame = self.create_scrollable_frame()
        self.notebook.add(food_container, text="食物属性")
        self.food_tab = FoodGeneratorTab(food_frame)
        
        # 旗帜生成器标签页
        banner_container, banner_frame = self.create_scrollable_frame()
        self.notebook.add(banner_container, text="旗帜属性")
        self.banner_tab = BannerGeneratorTab(banner_frame)
        
        # 工具属性标签页
        tool_container, tool_frame = self.create_scrollable_frame()
        self.notebook.add(tool_container, text="工具属性")
        self.tool_tab = ToolGeneratorTab(tool_frame)
        
        # 装备属性标签页
        equippable_container, equippable_frame = self.create_scrollable_frame()
        self.notebook.add(equippable_container, text="装备属性")
        self.equippable_tab = EquippableGeneratorTab(equippable_frame)
        
        # 成书生成器标签页
        written_book_container, written_book_frame = self.create_scrollable_frame()
        self.notebook.add(written_book_container, text="成书生成器")
        self.written_book_tab = WrittenBookGeneratorTab(written_book_frame)
        
        # 其他属性标签页
        other_container, other_frame = self.create_scrollable_frame()
        self.notebook.add(other_container, text="其他属性")
        self.create_other_tab(other_frame)
    
    def toggle_tabs(self, full_expand=False):
        """展开/收起标签页"""
        if self.tab_container.winfo_ismapped():
            # 收起标签页
            self.tab_container.pack_forget()
            self.toggle_button.config(text="展开标签页")
            
            # 取消窗口置顶
            self.root.attributes('-topmost', False)
            
            # 恢复原来的窗口大小
            if hasattr(self, 'original_width') and hasattr(self, 'original_height'):
                self.root.geometry(f"{self.original_width}x{self.original_height}")
            else:
                # 如果没有保存原始大小，使用默认大小
                self.root.geometry("1000x600")
            
            # 窗口移到屏幕中央
            self.center_window()
            
            # 恢复原来的布局
            main_frame = self.root.winfo_children()[0]
            if main_frame:
                # 重新排列组件
                # 标题栏保持在顶部 (row=0)
                # 主内容区域移回中间 (row=1)
                # 标签页区域移回底部 (row=2)
                children = main_frame.winfo_children()
                for child in children:
                    if child == self.title_frame:
                        # 显示标题栏
                        child.grid()
                    elif child == self.main_content:
                        # 显示主内容区域并移回中间
                        child.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
                    elif child == self.bottom_tab_area:
                        # 标签页区域移回底部
                        child.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
                
                # 重新配置权重
                main_frame.rowconfigure(0, weight=0)  # 标题栏
                main_frame.rowconfigure(1, weight=1)  # 主内容区域
                main_frame.rowconfigure(2, weight=0)  # 标签页区域
        else:
            # 展开标签页
            self.tab_container.pack(fill=tk.BOTH, expand=True, pady=5)
            self.toggle_button.config(text="收起标签页")
            
            # 检查窗口位置，确保窗口紧贴屏幕顶部
            self.check_window_position()
            
            # 如果是完全展开模式
            if full_expand:
                # 保存当前窗口大小，以便稍后恢复
                self.original_width = self.root.winfo_width()
                self.original_height = self.root.winfo_height()
                
                # 调整窗口大小，确保标签页有足够的空间
                new_height = 700  # 设置固定高度为700
                self.root.geometry(f"{self.original_width}x{new_height}")
                
                # 确保主框架的权重配置正确，使标签页区域能够扩展
                main_frame = self.root.winfo_children()[0]
                if main_frame:
                    # 重新布局，将标签页区域移到上方并隐藏主内容区域
                    # 先获取所有子组件
                    children = main_frame.winfo_children()
                    
                    # 重新排列组件
                    # 隐藏标题栏
                    # 标签页区域移到中间 (row=1)
                    # 隐藏主内容区域
                    for child in children:
                        if child == self.title_frame:
                            # 隐藏标题栏
                            child.grid_remove()
                        elif child == self.main_content:
                            # 隐藏主内容区域
                            child.grid_remove()
                        elif child == self.bottom_tab_area:
                            # 标签页区域移到中间
                            child.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
                    
                    # 重新配置权重
                    main_frame.rowconfigure(0, weight=0)  # 标题栏
                    main_frame.rowconfigure(1, weight=1)  # 标签页区域（给予全部权重）


    def get_txt_files_path(self):
        """获取txt_files目录的正确路径"""
        import sys
        # 检查是否是打包后的环境
        if getattr(sys, 'frozen', False):
            # 打包后的环境，使用当前工作目录
            return os.path.join(os.getcwd(), "txt_files")
        else:
            # 开发环境，使用文件所在目录
            return os.path.join(os.path.dirname(__file__), "txt_files")

    def load_item_ids(self):
        """从item_id.txt文件加载物品ID映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "item_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, item_id = line.split(',', 1)
                        self.item_id_map[chinese_name] = item_id
        except FileNotFoundError:
            # 如果文件不存在，创建一些默认物品
            self.item_id_map = {
                "下界合金剑": "minecraft:netherite_sword",
                "钻石剑": "minecraft:diamond_sword",
                "金剑": "minecraft:golden_sword",
                "铁剑": "minecraft:iron_sword",
                "石剑": "minecraft:stone_sword",
                "木剑": "minecraft:wooden_sword",
                "下界合金斧": "minecraft:netherite_axe",
                "钻石斧": "minecraft:diamond_axe",
                "弓": "minecraft:bow",
                "三叉戟": "minecraft:trident",
                "下界合金胸甲": "minecraft:netherite_chestplate",
                "钻石胸甲": "minecraft:diamond_chestplate",
                "下界合金头盔": "minecraft:netherite_helmet",
                "钻石头盔": "minecraft:diamond_helmet",
                "下界合金护腿": "minecraft:netherite_leggings",
                "钻石护腿": "minecraft:diamond_leggings",
                "下界合金靴子": "minecraft:netherite_boots",
                "钻石靴子": "minecraft:diamond_boots",
                "盾牌": "minecraft:shield",
                "不死图腾": "minecraft:totem_of_undying",
                "绿宝石": "minecraft:emerald",
                "钻石": "minecraft:diamond",
                "下界合金锭": "minecraft:netherite_ingot",
                "金锭": "minecraft:gold_ingot",
                "铁锭": "minecraft:iron_ingot",
                "石头": "minecraft:stone",
                "药水": "minecraft:potion",
                "喷溅药水": "minecraft:splash_potion",
                "滞留药水": "minecraft:lingering_potion",
                "烟花火箭": "minecraft:firework_rocket"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                # 确保txt_files目录存在
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "item_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, item_id in self.item_id_map.items():
                        f.write(f"{chinese_name},{item_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def load_enchant_ids(self):
        """从enchant_id.txt文件加载附魔ID映射"""
        try:
            file_path = os.path.join(self.get_txt_files_path(), "enchant_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, enchant_id = line.split(',', 1)
                        self.enchant_map[chinese_name] = enchant_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认附魔
            self.enchant_map = {
                "锋利": "minecraft:sharpness",
                "亡灵杀手": "minecraft:smite",
                "节肢杀手": "minecraft:bane_of_arthropods",
                "击退": "minecraft:knockback",
                "火焰附加": "minecraft:fire_aspect",
                "抢夺": "minecraft:looting",
                "横扫之刃": "minecraft:sweeping",
                "效率": "minecraft:efficiency",
                "精准采集": "minecraft:silk_touch",
                "耐久": "minecraft:unbreaking",
                "时运": "minecraft:fortune",
                "力量": "minecraft:power",
                "冲击": "minecraft:punch",
                "火矢": "minecraft:flame",
                "无限": "minecraft:infinity",
                "海之眷顾": "minecraft:luck_of_the_sea",
                "饵钓": "minecraft:lure",
                "忠诚": "minecraft:loyalty",
                "穿刺": "minecraft:impaling",
                "激流": "minecraft:riptide",
                "引雷": "minecraft:channeling",
                "多重射击": "minecraft:multishot",
                "快速装填": "minecraft:quick_charge",
                "穿透": "minecraft:piercing",
                "经验修补": "minecraft:mending",
                "消失诅咒": "minecraft:vanishing_curse",
                "绑定诅咒": "minecraft:binding_curse",
                "深海探索者": "minecraft:depth_strider",
                "冰霜行者": "minecraft:frost_walker",
                "摔落保护": "minecraft:feather_falling",
                "保护": "minecraft:protection",
                "爆炸保护": "minecraft:blast_protection",
                "火焰保护": "minecraft:fire_protection",
                "弹射物保护": "minecraft:projectile_protection",
                "水下呼吸": "minecraft:respiration",
                "水下速掘": "minecraft:aqua_affinity",
                "荆棘": "minecraft:thorns",
                "灵魂疾行": "minecraft:soul_speed",
                "迅捷潜行": "minecraft:swift_sneak"
            }
            # 尝试创建默认文件
        try:
            file_path = os.path.join(os.path.dirname(__file__), "txt_files", "enchant_id.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                for chinese_name, enchant_id in self.enchant_map.items():
                    f.write(f"{chinese_name},{enchant_id}\n")
        except:
            pass  # 如果无法创建文件，忽略错误
    
    def load_block_ids(self):
        """从block_id.txt文件加载方块ID映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "block_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, block_id = line.split(',', 1)
                        self.block_id_map[chinese_name] = block_id
        except FileNotFoundError:
            # 如果文件不存在，创建一些默认方块
            self.block_id_map = {
                "石头": "minecraft:stone",
                "草方块": "minecraft:grass_block",
                "泥土": "minecraft:dirt",
                "沙子": "minecraft:sand",
                "木头": "minecraft:oak_log",
                "木板": "minecraft:oak_planks"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "block_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, block_id in self.block_id_map.items():
                        f.write(f"{chinese_name},{block_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def load_entity_ids(self):
        """从entity_id.txt文件加载实体ID映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "entity_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, entity_id = line.split(',', 1)
                        self.entity_id_map[chinese_name] = entity_id
        except FileNotFoundError:
            # 如果文件不存在，创建一些默认实体
            self.entity_id_map = {
                "村民": "minecraft:villager",
                "僵尸": "minecraft:zombie",
                "骷髅": "minecraft:skeleton",
                "苦力怕": "minecraft:creeper",
                "末影人": "minecraft:enderman",
                "猪": "minecraft:pig",
                "牛": "minecraft:cow",
                "羊": "minecraft:sheep",
                "鸡": "minecraft:chicken",
                "狼": "minecraft:wolf"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "entity_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, entity_id in self.entity_id_map.items():
                        f.write(f"{chinese_name},{entity_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10", style="Custom.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 顶部标题 - 简化布局
        self.title_frame = tk.Frame(main_frame, bg="#f0f2f5")
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 8))
        title_label = tk.Label(self.title_frame, text="Minecraft Give指令生成器", font=('SimHei', 12, 'bold'), fg="#2c3e50", bg="#f0f2f5")
        title_label.pack(side=tk.LEFT)
        
        # 版本信息
        version_label = tk.Label(self.title_frame, text="v1.21.11+", font=('SimHei', 8), fg="#718096", bg="#f0f2f5")
        version_label.pack(side=tk.RIGHT, padx=5)
        
        # 主内容区域（可展开/收起的部分）
        self.main_content = ttk.Frame(main_frame)
        self.main_content.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 在主内容区域创建控件
        self.create_main_content_widgets()
        
        # 底部标签页区域 - 初始为收起状态
        self.bottom_tab_area = ttk.Frame(main_frame, padding="5")
        self.bottom_tab_area.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 创建展开/收起按钮 - 改为完全展开模式
        self.toggle_button = ttk.Button(self.bottom_tab_area, text="完全展开标签页", command=lambda: self.toggle_tabs(full_expand=True))
        self.toggle_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 标签页容器
        self.tab_container = ttk.Frame(self.bottom_tab_area)
        # 初始隐藏
        self.tab_container.pack_forget()
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.tab_container, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建标签页内容
        self.create_tabs()
        
        # 配置权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # 主内容区域可扩展
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 默认选择第一个物品
        if self.item_id_map:
            first_item = list(self.item_id_map.keys())[0]
            self.item_var.set(first_item)
            self.on_item_selected()
    
    def create_top_area_widgets(self):
        """在上方区域创建物品配置和命令生成控件"""
        # 顶部配置区域 - 紧凑布局
        config_frame = ttk.LabelFrame(self.top_area, text="物品配置", padding=8)
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 物品选择 - 减少间距
        ttk.Label(config_frame, text="物品:", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=3, padx=3)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(config_frame, textvariable=self.item_var, width=55)
        self.item_combo['values'] = list(self.item_id_map.keys())
        self.item_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=3, padx=3)
        self.item_combo.bind('<<ComboboxSelected>>', self.on_item_selected)
        self.item_combo.bind('<KeyRelease>', self.on_item_search)
        
        # 物品ID输入框 - 减少间距
        ttk.Label(config_frame, text="物品ID:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=3, padx=3)
        self.item_id_var = tk.StringVar()
        self.item_id = ttk.Entry(config_frame, textvariable=self.item_id_var, width=55)
        self.item_id.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=3, padx=3)
        self.item_id.bind('<KeyRelease>', self.on_item_id_changed)
        
        # 数量输入 - 减少间距
        ttk.Label(config_frame, text="数量:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=3, padx=3)
        self.count_var = tk.StringVar(value="1")
        count_entry = ttk.Entry(config_frame, textvariable=self.count_var, width=15)
        count_entry.grid(row=2, column=1, sticky=tk.W, pady=3, padx=3)
        
        # 命令生成区域 - 紧凑布局
        command_frame = ttk.LabelFrame(self.top_area, text="命令生成", padding=8)
        command_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 生成命令按钮 - 减少间距
        generate_button = ttk.Button(command_frame, text="生成Give命令", command=self.generate_command)
        generate_button.grid(row=0, column=0, pady=5, padx=3, sticky=tk.W)
        
        # 命令显示框和复制按钮 - 减少高度
        ttk.Label(command_frame, text="生成的命令:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=3, padx=3)
        command_display_frame = ttk.Frame(command_frame, borderwidth=1, relief="solid", style="Custom.TFrame")
        command_display_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3, padx=3)
        
        self.command_text = tk.Text(command_display_frame, height=4, width=75, font=('Courier New', 9), bg="#f7fafc", borderwidth=0, highlightthickness=0)
        self.command_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # 复制按钮 - 小字显示在旁边
        copy_button = ttk.Button(command_display_frame, text="复制", command=self.copy_command, style="Small.TButton")
        copy_button.pack(side=tk.RIGHT, padx=5, pady=3, fill=tk.Y)
        
        # 配置权重
        config_frame.columnconfigure(1, weight=1)
        command_frame.columnconfigure(1, weight=1)
        self.top_area.columnconfigure(0, weight=1)
    
    def create_bottom_area_widgets(self):
        """在下方区域创建标签页"""
        # 标签页区域 - 主要内容
        notebook = ttk.Notebook(self.bottom_area, style="Custom.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 显示属性标签页
        display_frame = self.create_scrollable_frame()
        notebook.add(display_frame, text="显示属性")
        self.create_display_tab(display_frame.winfo_children()[0])
        
        # 附魔标签页
        enchant_frame = self.create_scrollable_frame()
        notebook.add(enchant_frame, text="附魔")
        self.create_enchant_tab(enchant_frame.winfo_children()[0])
        
        # 属性修饰符标签页
        attribute_frame = self.create_scrollable_frame()
        notebook.add(attribute_frame, text="属性修饰符")
        self.create_attribute_tab(attribute_frame.winfo_children()[0])
        
        # 药水效果标签页
        potion_frame = self.create_scrollable_frame()
        notebook.add(potion_frame, text="药水效果")
        self.potion_tab = PotionEffectsTab(potion_frame.winfo_children()[0])
        
        # 烟花火箭标签页
        fireworks_frame = self.create_scrollable_frame()
        notebook.add(fireworks_frame, text="烟花火箭")
        self.fireworks_tab = FireworksTab(fireworks_frame.winfo_children()[0])
        
        # 头颅生成器标签页
        skull_frame = self.create_scrollable_frame()
        notebook.add(skull_frame, text="头颅生成器")
        self.skull_tab = SkullGeneratorTab(skull_frame.winfo_children()[0])
        
        # 食物生成器标签页
        food_frame = self.create_scrollable_frame()
        notebook.add(food_frame, text="食物属性")
        self.food_tab = FoodGeneratorTab(food_frame.winfo_children()[0])

        # 其他属性标签页
        other_frame = self.create_scrollable_frame()
        notebook.add(other_frame, text="其他属性")
        self.create_other_tab(other_frame.winfo_children()[0])
        
        # 保存notebook引用
        self.notebook = notebook
    
    def create_scrollable_frame(self):
        """创建可滚动的框架"""
        # 创建主框架
        container = ttk.Frame()
        container.pack_propagate(False)
        
        # 创建Canvas和Scrollbar - 移除固定高度，让界面可以灵活调整
        canvas = tk.Canvas(container, bg="#f3f4f6", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # 创建可滚动的内部框架
        scrollable_frame = ttk.Frame(canvas)
        
        # 在Canvas中创建窗口
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scrollable_frame(event):
            """配置内部框架和滚动区域"""
            # 设置内部框架的宽度为Canvas的宽度减去滚动条的宽度
            canvas_width = canvas.winfo_width()
            scrollbar_width = scrollbar.winfo_width()
            canvas.itemconfig(window_id, width=canvas_width - scrollbar_width)
            
            # 更新滚动区域
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas(event):
            """配置Canvas的大小"""
            canvas_width = event.width
            canvas_height = event.height
            canvas.configure(width=canvas_width, height=canvas_height)
            
            # 更新内部框架宽度
            scrollbar_width = scrollbar.winfo_width()
            canvas.itemconfig(window_id, width=canvas_width - scrollbar_width)
            
            # 更新滚动区域
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_mousewheel(event):
            """鼠标滚轮事件处理"""
            # Windows和Linux使用delta，Mac可能需要调整
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
        
        def on_canvas_mousewheel(event):
            """Canvas上的鼠标滚轮事件处理"""
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def bind_mousewheel_recursive(widget):
            """递归绑定鼠标滚轮事件到所有子组件"""
            widget.bind("<MouseWheel>", on_canvas_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            
            # 递归绑定子组件
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)
        
        # 绑定事件
        scrollable_frame.bind("<Configure>", configure_scrollable_frame)
        canvas.bind("<Configure>", configure_canvas)
        container.bind("<Configure>", configure_canvas)
        
        # 绑定鼠标滚轮事件到Canvas
        canvas.bind("<MouseWheel>", on_canvas_mousewheel)
        canvas.bind("<Button-4>", on_mousewheel)  # Linux向上滚动
        canvas.bind("<Button-5>", on_mousewheel)  # Linux向下滚动
        
        # 绑定鼠标滚轮事件到内部框架及其所有子组件
        bind_mousewheel_recursive(scrollable_frame)
        
        # 配置Canvas和Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 打包组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return container, scrollable_frame
    
    def on_item_search(self, event):
        """当在物品搜索框中输入时，自动过滤物品列表"""
        # 获取当前输入
        value = event.widget.get()
        
        # 如果输入为空，显示所有物品
        if value == '':
            self.item_combo['values'] = list(self.item_id_map.keys())
        else:
            # 过滤包含输入文本的物品名称
            data = []
            for item in self.item_id_map.keys():
                if value.lower() in item.lower():
                    data.append(item)
            self.item_combo['values'] = data
    
    def on_item_selected(self, event=None):
        """当选择物品时更新物品ID"""
        selected_item = self.item_var.get()
        if selected_item in self.item_id_map:
            self.item_id_var.set(self.item_id_map[selected_item])
    
    def on_item_id_changed(self, event):
        """当物品ID改变时反向查找物品名称"""
        item_id_value = self.item_id_var.get().strip()
        
        # 查找匹配的物品ID
        for chinese_name, item_id in self.item_id_map.items():
            if item_id.lower() == item_id_value.lower():
                self.item_var.set(chinese_name)
                return
        
        # 如果没有完全匹配，尝试部分匹配
        if item_id_value:
            matches = []
            for chinese_name, item_id in self.item_id_map.items():
                if item_id_value.lower() in item_id.lower():
                    matches.append(chinese_name)
            
            if len(matches) == 1:
                self.item_var.set(matches[0])
    
    def create_display_tab(self, parent):
        # 名称
        ttk.Label(parent, text="自定义名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.custom_name = ttk.Entry(parent, width=50)
        self.custom_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 颜色
        ttk.Label(parent, text="颜色:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar()
        color_combo = ttk.Combobox(parent, textvariable=self.color_var, width=20)
        color_combo['values'] = ('', 'black', 'dark_blue', 'dark_green', 'dark_aqua', 'dark_red', 
                                'dark_purple', 'gold', 'gray', 'dark_gray', 'blue', 'green', 
                                'aqua', 'red', 'light_purple', 'yellow', 'white')
        color_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 样式选项
        self.bold_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="粗体", variable=self.bold_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.italic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="斜体", variable=self.italic_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 描述
        ttk.Label(parent, text="描述(每行一个，用|分隔):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.lore_text = tk.Text(parent, height=4, width=50)
        self.lore_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        parent.columnconfigure(1, weight=1)
    
    def create_enchant_tab(self, parent):
        # 附魔列表框架
        enchant_list_frame = ttk.Frame(parent)
        enchant_list_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # 添加附魔的控件
        ttk.Label(enchant_list_frame, text="附魔:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.enchant_id = ttk.Combobox(enchant_list_frame, width=25)
        
        self.enchant_id['values'] = list(self.enchant_map.keys())
        self.enchant_id.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(enchant_list_frame, text="等级:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.enchant_level = ttk.Entry(enchant_list_frame, width=10)
        self.enchant_level.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        ttk.Button(enchant_list_frame, text="添加附魔", command=self.add_enchantment).grid(row=0, column=4, pady=5)
        
        # 附魔列表显示
        ttk.Label(parent, text="已添加的附魔:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.enchant_listbox = tk.Listbox(parent, height=6)
        self.enchant_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_enchantment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空列表", command=self.clear_enchantments).pack(side=tk.LEFT, padx=5)
        
        enchant_list_frame.columnconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def create_attribute_tab(self, parent):
        # 属性修饰符列表框架
        attribute_list_frame = ttk.Frame(parent)
        attribute_list_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # 添加属性修饰符的控件
        ttk.Label(attribute_list_frame, text="属性:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.attribute_name = ttk.Combobox(attribute_list_frame, width=20)
        
        # 属性与中文名称映射
        self.attribute_map = {
            "最大生命值": "generic.max_health",
            "追踪范围": "generic.follow_range",
            "击退抗性": "generic.knockback_resistance",
            "移动速度": "generic.movement_speed",
            "攻击伤害": "generic.attack_damage",
            "盔甲": "generic.armor",
            "盔甲韧性": "generic.armor_toughness",
            "攻击击退": "generic.attack_knockback",
            "攻击速度": "generic.attack_speed",
            "幸运": "generic.luck"
        }
        
        self.attribute_name['values'] = list(self.attribute_map.keys())
        self.attribute_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(attribute_list_frame, text="数值:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.attribute_amount = ttk.Entry(attribute_list_frame, width=10)
        self.attribute_amount.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(attribute_list_frame, text="操作:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.attribute_operation = ttk.Combobox(attribute_list_frame, width=15)
        self.attribute_operation['values'] = ('0 - 增加值', '1 - 倍增值', '2 - 最终值')
        self.attribute_operation.current(0)
        self.attribute_operation.grid(row=1, column=3, sticky=tk.W, pady=5)
        
        ttk.Label(attribute_list_frame, text="槽位:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.attribute_slot = ttk.Combobox(attribute_list_frame, width=15)
        self.attribute_slot['values'] = ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')
        self.attribute_slot.current(0)
        self.attribute_slot.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(attribute_list_frame, text="添加属性", command=self.add_attribute).grid(row=2, column=3, pady=5)
        
        # 属性列表显示
        ttk.Label(parent, text="已添加的属性:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.attribute_listbox = tk.Listbox(parent, height=6)
        self.attribute_listbox.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=4, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_attribute).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空列表", command=self.clear_attributes).pack(side=tk.LEFT, padx=5)
        
        attribute_list_frame.columnconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def create_other_tab(self, parent):
        # 标题和说明
        ttk.Label(parent, text="其他属性设置", font=('SimHei', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=8)
        ttk.Label(parent, text="以下是一些常用的物品属性设置，可根据需要选择配置。", font=('SimHei', 8), foreground="#718096").grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=3)
        
        # 不可破坏
        self.unbreakable_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="不可破坏", variable=self.unbreakable_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(物品不会损耗耐久度)", font=('SimHei', 8), foreground="#718096").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 损坏值
        ttk.Label(parent, text="损坏值:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.damage_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.damage_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(物品当前的耐久度损耗)", font=('SimHei', 8), foreground="#718096").grid(row=3, column=2, sticky=tk.W, pady=5)
        
        # 自定义模型数据
        ttk.Label(parent, text="自定义模型数据:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.model_data_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.model_data_var, width=10).grid(row=4, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(用于自定义资源包模型)", font=('SimHei', 8), foreground="#718096").grid(row=4, column=2, sticky=tk.W, pady=5)
        
        # 提示框显示控制（tooltip_display）
        ttk.Label(parent, text="提示框显示控制:", font=('SimHei', 10, 'bold')).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=8)
        
        # 隐藏提示框
        self.hide_tooltip_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="总是隐藏提示框", variable=self.hide_tooltip_var).grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(物品提示框是否总是隐藏)", font=('SimHei', 8), foreground="#718096").grid(row=6, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # 隐藏的组件
        ttk.Label(parent, text="隐藏的组件:").grid(row=7, column=0, sticky=tk.W, pady=5)
        
        # 组件ID映射（中文到英文）
        self.component_id_map = {
            '附魔': 'minecraft:enchantments',
            '属性修饰符': 'minecraft:attribute_modifiers',
            '不可破坏': 'minecraft:unbreakable',
            '可破坏方块': 'minecraft:can_break',
            '可放置方块': 'minecraft:can_place_on',
            '修复材料': 'minecraft:repairable',
            '返回物品': 'minecraft:use_remainder',
            '使用冷却': 'minecraft:use_cooldown',
            '实体数据': 'minecraft:entity_data',
            '方块实体数据': 'minecraft:block_entity_data',
            '药水效果': 'minecraft:potion_contents',
            '烟花效果': 'minecraft:fireworks',
            '自定义名称': 'minecraft:custom_name',
            '描述': 'minecraft:lore'
        }
        
        # 组件选择下拉列表（显示中文）
        self.hidden_component_var = tk.StringVar()
        hidden_component_combo = ttk.Combobox(parent, textvariable=self.hidden_component_var, width=30)
        hidden_component_combo['values'] = list(self.component_id_map.keys())
        hidden_component_combo.grid(row=7, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="添加", command=self.add_hidden_component).grid(row=7, column=2, sticky=tk.W, pady=5)
        
        # 隐藏组件列表框
        ttk.Label(parent, text="已选择的隐藏组件:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.hidden_components_listbox = tk.Listbox(parent, height=4, width=40)
        self.hidden_components_listbox.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 隐藏组件按钮
        hidden_components_button_frame = ttk.Frame(parent)
        hidden_components_button_frame.grid(row=9, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(hidden_components_button_frame, text="删除选中", command=self.remove_hidden_component).pack(side=tk.LEFT, padx=5)
        ttk.Button(hidden_components_button_frame, text="清空列表", command=self.clear_hidden_components).pack(side=tk.LEFT, padx=5)
        ttk.Label(parent, text=" ", font=('SimHei', 8), foreground="#718096").grid(row=9, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 可破坏方块（CanDestroy）
        ttk.Label(parent, text="可破坏方块:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.can_destroy_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.can_destroy_var, width=30).grid(row=10, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(parent, text="(格式: minecraft:stone,minecraft:wood 多个用逗号分隔)", font=('SimHei', 8), foreground="#718096").grid(row=11, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 可破坏方块列表框
        ttk.Label(parent, text="已选择的可破坏方块:").grid(row=12, column=0, sticky=tk.W, pady=5)
        self.can_destroy_listbox = tk.Listbox(parent, height=4, width=40)
        self.can_destroy_listbox.grid(row=12, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 可破坏方块按钮
        can_destroy_button_frame = ttk.Frame(parent)
        can_destroy_button_frame.grid(row=13, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(can_destroy_button_frame, text="删除选中", command=lambda: self.remove_block_from_list('can_destroy')).pack(side=tk.LEFT, padx=5)
        ttk.Button(can_destroy_button_frame, text="清空列表", command=lambda: self.clear_block_list('can_destroy')).pack(side=tk.LEFT, padx=5)
        
        # 可破坏方块下拉列表
        ttk.Label(parent, text="添加方块:").grid(row=14, column=0, sticky=tk.W, pady=5)
        self.can_destroy_block_var = tk.StringVar()
        can_destroy_combo = ttk.Combobox(parent, textvariable=self.can_destroy_block_var, width=30)
        can_destroy_combo['values'] = list(self.block_id_map.keys())
        can_destroy_combo.grid(row=14, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="添加", command=lambda: self.add_block_to_list('can_destroy')).grid(row=14, column=2, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(从下拉列表选择方块添加到可破坏方块列表)", font=('SimHei', 8), foreground="#718096").grid(row=15, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 可放置方块（CanPlaceOn）
        ttk.Label(parent, text="可放置方块:").grid(row=16, column=0, sticky=tk.W, pady=5)
        self.can_place_on_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.can_place_on_var, width=30).grid(row=16, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(parent, text="(格式: minecraft:stone,minecraft:wood 多个用逗号分隔)", font=('SimHei', 8), foreground="#718096").grid(row=17, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 可放置方块列表框
        ttk.Label(parent, text="已选择的可放置方块:").grid(row=18, column=0, sticky=tk.W, pady=5)
        self.can_place_on_listbox = tk.Listbox(parent, height=4, width=40)
        self.can_place_on_listbox.grid(row=18, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 可放置方块按钮
        can_place_on_button_frame = ttk.Frame(parent)
        can_place_on_button_frame.grid(row=19, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(can_place_on_button_frame, text="删除选中", command=lambda: self.remove_block_from_list('can_place_on')).pack(side=tk.LEFT, padx=5)
        ttk.Button(can_place_on_button_frame, text="清空列表", command=lambda: self.clear_block_list('can_place_on')).pack(side=tk.LEFT, padx=5)
        
        # 可放置方块下拉列表
        ttk.Label(parent, text="添加方块:").grid(row=20, column=0, sticky=tk.W, pady=5)
        self.can_place_on_block_var = tk.StringVar()
        can_place_on_combo = ttk.Combobox(parent, textvariable=self.can_place_on_block_var, width=30)
        can_place_on_combo['values'] = list(self.block_id_map.keys())
        can_place_on_combo.grid(row=20, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="添加", command=lambda: self.add_block_to_list('can_place_on')).grid(row=20, column=2, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(从下拉列表选择方块添加到可放置方块列表)", font=('SimHei', 8), foreground="#718096").grid(row=21, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 物品修复材料
        ttk.Label(parent, text="修复材料:").grid(row=22, column=0, sticky=tk.W, pady=5)
        self.repair_material_var = tk.StringVar()
        repair_material_combo = ttk.Combobox(parent, textvariable=self.repair_material_var, width=30)
        repair_material_combo['values'] = list(self.item_id_map.keys())
        repair_material_combo.grid(row=22, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(parent, text="(用于铁砧修复的材料ID，如 minecraft:iron_ingot)", font=('SimHei', 8), foreground="#718096").grid(row=23, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 父母信息（用于生物头颅）
        ttk.Label(parent, text="父母信息:").grid(row=24, column=0, sticky=tk.W, pady=5)
        self.parents_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.parents_var, width=30).grid(row=24, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(parent, text="(用于某些生物头颅的父母信息，格式为JSON)", font=('SimHei', 8), foreground="#718096").grid(row=25, column=1, columnspan=2, sticky=tk.W, pady=3)
        
        # 新属性设置
        ttk.Label(parent, text="新属性设置", font=('SimHei', 10, 'bold')).grid(row=26, column=0, columnspan=3, sticky=tk.W, pady=8)
        
        # max_stack_size=：正整数，指物品的最大堆叠数
        ttk.Label(parent, text="最大堆叠数:").grid(row=27, column=0, sticky=tk.W, pady=5)
        self.max_stack_size_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.max_stack_size_var, width=10).grid(row=27, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(正整数，指物品的最大堆叠数)", font=('SimHei', 8), foreground="#718096").grid(row=27, column=2, sticky=tk.W, pady=5)
        
        # repair_cost=：正整数，就是用铁砧修复时需要的经验等级惩罚
        ttk.Label(parent, text="修复惩罚等级:").grid(row=28, column=0, sticky=tk.W, pady=5)
        self.repair_cost_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.repair_cost_var, width=10).grid(row=28, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(正整数，铁砧修复时的经验等级惩罚)", font=('SimHei', 8), foreground="#718096").grid(row=28, column=2, sticky=tk.W, pady=5)
        
        # use_remainder={id:id,count:n}：拿着这种物品右键时能出现n个id所对应的物品
        ttk.Label(parent, text="返回物品ID:").grid(row=29, column=0, sticky=tk.W, pady=5)
        self.use_remainder_id_var = tk.StringVar()
        use_remainder_combo = ttk.Combobox(parent, textvariable=self.use_remainder_id_var, width=30)
        use_remainder_combo['values'] = list(self.item_id_map.keys())
        use_remainder_combo.grid(row=29, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(parent, text="返回物品数量:").grid(row=30, column=0, sticky=tk.W, pady=5)
        self.use_remainder_count_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.use_remainder_count_var, width=10).grid(row=30, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(使用完某消耗品返回的物品的数量)", font=('SimHei', 8), foreground="#718096").grid(row=30, column=2, sticky=tk.W, pady=5)
        
        # use_cooldown={seconds:正数}：物品使用的冷却时间
        ttk.Label(parent, text="使用冷却时间:").grid(row=31, column=0, sticky=tk.W, pady=5)
        self.use_cooldown_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.use_cooldown_var, width=10).grid(row=31, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(秒，仅用于原本有冷却时间的物品，不能为0)", font=('SimHei', 8), foreground="#718096").grid(row=31, column=2, sticky=tk.W, pady=5)
        
        # entity_data={id:id,Invisible:1b/0b}：实体类物品产生的实体名称和是否隐身
        ttk.Label(parent, text="实体ID:").grid(row=32, column=0, sticky=tk.W, pady=5)
        self.entity_id_var = tk.StringVar()
        entity_combo = ttk.Combobox(parent, textvariable=self.entity_id_var, width=30)
        entity_combo['values'] = list(self.entity_id_map.keys())
        entity_combo.grid(row=32, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.entity_invisible_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="实体隐身", variable=self.entity_invisible_var).grid(row=33, column=0, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(生成实体类物品（例如美西螈桶）产生的实体是否隐身)", font=('SimHei', 8), foreground="#718096").grid(row=33, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # hide_additional_tooltip={}：是否会显示nbt属性
        self.hide_additional_tooltip_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="隐藏额外提示", variable=self.hide_additional_tooltip_var).grid(row=30, column=0, sticky=tk.W, pady=5)
        ttk.Label(parent, text="(是否会显示nbt属性)", font=('SimHei', 8), foreground="#718096").grid(row=30, column=1, sticky=tk.W, pady=5)
    
    def add_enchantment(self):
        enchant_name = self.enchant_id.get().strip()
        level = self.enchant_level.get().strip()
        
        if not enchant_name or not level:
            messagebox.showerror("错误", "请选择附魔和填写等级")
            return
        
        if enchant_name not in self.enchant_map:
            messagebox.showerror("错误", "请选择有效的附魔")
            return
        
        try:
            level_int = int(level)
            if level_int < 1:
                raise ValueError("等级必须为正整数")
        except ValueError:
            messagebox.showerror("错误", "等级必须是正整数")
            return
        
        enchant_data = {
            "id": self.enchant_map[enchant_name],
            "lvl": level_int
        }
        
        self.enchantments.append(enchant_data)
        self.update_enchantment_listbox()
        
        # 清空输入框
        self.enchant_id.set('')
        self.enchant_level.delete(0, tk.END)
    
    def remove_enchantment(self):
        selected = self.enchant_listbox.curselection()
        if selected:
            index = selected[0]
            del self.enchantments[index]
            self.update_enchantment_listbox()
    
    def clear_enchantments(self):
        self.enchantments = []
        self.update_enchantment_listbox()
    
    def update_enchantment_listbox(self):
        self.enchant_listbox.delete(0, tk.END)
        for enchant in self.enchantments:
            # 查找中文名称
            chinese_name = "未知附魔"
            for name, id_val in self.enchant_map.items():
                if id_val == enchant["id"]:
                    chinese_name = name
                    break
            self.enchant_listbox.insert(tk.END, f"{chinese_name} (等级 {enchant['lvl']})")
    
    def add_attribute(self):
        attribute_name = self.attribute_name.get().strip()
        amount = self.attribute_amount.get().strip()
        operation = self.attribute_operation.get().strip()[0]  # 取第一个字符
        slot = self.attribute_slot.get().strip()
        
        if not attribute_name or not amount:
            messagebox.showerror("错误", "请选择属性和填写数值")
            return
        
        if attribute_name not in self.attribute_map:
            messagebox.showerror("错误", "请选择有效的属性")
            return
        
        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("错误", "数值必须是数字")
            return
        
        # 生成UUID - 格式为 [I;数字1,数字2,数字3,数字4]，每个数字4位
        uuid_parts = [random.randint(1000, 9999) for _ in range(4)]
        
        attribute_data = {
            "AttributeName": f"minecraft:{self.attribute_map[attribute_name]}",
            "Name": "noName",  # 固定为"noName"
            "Amount": amount_float,
            "Operation": int(operation),
            "UUID": uuid_parts,
            "Slot": slot
        }
        
        self.attributes.append(attribute_data)
        self.update_attribute_listbox()
        
        # 清空输入框
        self.attribute_amount.delete(0, tk.END)
    
    def remove_attribute(self):
        selected = self.attribute_listbox.curselection()
        if selected:
            index = selected[0]
            del self.attributes[index]
            self.update_attribute_listbox()
    
    def clear_attributes(self):
        self.attributes = []
        self.update_attribute_listbox()
    
    def update_attribute_listbox(self):
        self.attribute_listbox.delete(0, tk.END)
        for attr in self.attributes:
            # 查找中文名称
            chinese_name = "未知属性"
            attr_id = attr["AttributeName"].replace("minecraft:", "")
            for name, id_val in self.attribute_map.items():
                if id_val == attr_id:
                    chinese_name = name
                    break
            self.attribute_listbox.insert(tk.END, f"{chinese_name}: {attr['Amount']} ({attr['Slot']})")
    
    def add_block_to_list(self, list_type):
        """将选择的方块添加到可破坏或可放置列表"""
        if list_type == 'can_destroy':
            selected_block = self.can_destroy_block_var.get()
        else:
            selected_block = self.can_place_on_block_var.get()
            
        if selected_block in self.block_id_map:
            block_id = self.block_id_map[selected_block]
            block_display = f"{selected_block} ({block_id})"
            
            if list_type == 'can_destroy':
                current_value = self.can_destroy_var.get().strip()
                if current_value:
                    if block_id not in current_value:
                        self.can_destroy_var.set(current_value + ',' + block_id)
                        self.can_destroy_listbox.insert(tk.END, block_display)
                else:
                    self.can_destroy_var.set(block_id)
                    self.can_destroy_listbox.insert(tk.END, block_display)
            elif list_type == 'can_place_on':
                current_value = self.can_place_on_var.get().strip()
                if current_value:
                    if block_id not in current_value:
                        self.can_place_on_var.set(current_value + ',' + block_id)
                        self.can_place_on_listbox.insert(tk.END, block_display)
                else:
                    self.can_place_on_var.set(block_id)
                    self.can_place_on_listbox.insert(tk.END, block_display)
    
    def remove_block_from_list(self, list_type):
        """从可破坏或可放置列表中删除选中的方块"""
        if list_type == 'can_destroy':
            selected_indices = self.can_destroy_listbox.curselection()
            if selected_indices:
                # 从列表框中删除选中的项
                for index in reversed(selected_indices):
                    self.can_destroy_listbox.delete(index)
                
                # 更新输入框中的值
                # 重新构建方块ID列表
                block_ids = []
                for i in range(self.can_destroy_listbox.size()):
                    item = self.can_destroy_listbox.get(i)
                    # 从显示文本中提取方块ID
                    if '(' in item and ')' in item:
                        block_id = item.split('(')[1].strip(')')
                        block_ids.append(block_id)
                
                # 更新输入框
                self.can_destroy_var.set(','.join(block_ids))
        else:
            selected_indices = self.can_place_on_listbox.curselection()
            if selected_indices:
                # 从列表框中删除选中的项
                for index in reversed(selected_indices):
                    self.can_place_on_listbox.delete(index)
                
                # 更新输入框中的值
                # 重新构建方块ID列表
                block_ids = []
                for i in range(self.can_place_on_listbox.size()):
                    item = self.can_place_on_listbox.get(i)
                    # 从显示文本中提取方块ID
                    if '(' in item and ')' in item:
                        block_id = item.split('(')[1].strip(')')
                        block_ids.append(block_id)
                
                # 更新输入框
                self.can_place_on_var.set(','.join(block_ids))
    
    def clear_block_list(self, list_type):
        """清空可破坏或可放置列表中的所有方块"""
        if list_type == 'can_destroy':
            # 清空列表框
            self.can_destroy_listbox.delete(0, tk.END)
            # 清空输入框
            self.can_destroy_var.set('')
        else:
            # 清空列表框
            self.can_place_on_listbox.delete(0, tk.END)
            # 清空输入框
            self.can_place_on_var.set('')
    
    def add_hidden_component(self):
        """将选择的组件添加到隐藏组件列表"""
        selected_component = self.hidden_component_var.get().strip()
        if selected_component:
            # 将中文组件名称转换为英文组件ID
            if selected_component in self.component_id_map:
                component_id = self.component_id_map[selected_component]
            else:
                component_id = selected_component
            
            # 检查是否已存在
            exists = False
            for i in range(self.hidden_components_listbox.size()):
                if self.hidden_components_listbox.get(i) == component_id:
                    exists = True
                    break
            
            if not exists:
                self.hidden_components_listbox.insert(tk.END, component_id)
    
    def remove_hidden_component(self):
        """从隐藏组件列表中删除选中的组件"""
        selected_indices = self.hidden_components_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.hidden_components_listbox.delete(index)
    
    def clear_hidden_components(self):
        """清空隐藏组件列表中的所有组件"""
        self.hidden_components_listbox.delete(0, tk.END)
    
    def generate_command(self):
        item_id = self.item_id_var.get().strip()
        count = self.count_var.get().strip()
        
        if not item_id:
            messagebox.showerror("错误", "请选择物品")
            return
        
        # 特殊处理烟花火箭
        if item_id == "minecraft:firework_rocket" and hasattr(self, 'fireworks_tab'):
            try:
                fireworks_data, firework_count = self.fireworks_tab.get_fireworks_data()
                count_int = firework_count
            except ValueError as e:
                messagebox.showerror("错误", str(e))
                return
        else:
            try:
                count_int = int(count)
                if count_int < 1:
                    raise ValueError("数量必须为正整数")
            except ValueError:
                messagebox.showerror("错误", "数量必须是正整数")
                return
        
        # 收集所有组件数据
        components = {}
        
        # 自定义名称组件
        name = self.custom_name.get().strip()
        if name:
            name_json = {"text": name}
            
            color = self.color_var.get().strip()
            if color:
                name_json["color"] = color
            
            if self.bold_var.get():
                name_json["bold"] = True
            
            if self.italic_var.get():
                name_json["italic"] = True
            
            custom_name_component = format_custom_name_component(name_json)
            if custom_name_component:
                components["minecraft:custom_name"] = custom_name_component
        
        # 描述组件
        lore_text = self.lore_text.get("1.0", tk.END).strip()
        if lore_text:
            lore_lines = [line.strip() for line in lore_text.split('|') if line.strip()]
            lore_json = [json.dumps({"text": line}, ensure_ascii=False) for line in lore_lines]
            lore_component = format_lore_component(lore_json)
            if lore_component:
                components["minecraft:lore"] = lore_component
        
        # 附魔组件
        if self.enchantments:
            enchantments_component = format_enchantments_component(self.enchantments)
            if enchantments_component:
                components["minecraft:enchantments"] = enchantments_component
        
        # 属性修饰符组件
        if self.attributes:
            attribute_component = format_attribute_modifiers_component(self.attributes)
            if attribute_component:
                components["minecraft:attribute_modifiers"] = attribute_component
        
        # 药水效果组件
        if self.potion_tab:
            potion_effects = self.potion_tab.get_potion_effects()
            color_hex = self.potion_tab.get_potion_color()
            color_decimal = None
            if color_hex.startswith('#'):
                color_decimal = int(color_hex[1:], 16)
            
            potion_component = format_potion_contents_component(potion_effects, color_decimal)
            if potion_component:
                components["minecraft:potion_contents"] = potion_component
        
        # 烟花火箭组件
        if item_id == "minecraft:firework_rocket" and hasattr(self, 'fireworks_tab'):
            fireworks_data, _ = self.fireworks_tab.get_fireworks_data()
            fireworks_component = format_fireworks_component(fireworks_data)
            if fireworks_component:
                components["fireworks"] = fireworks_component
        
        # 头颅组件
        if item_id == "minecraft:player_head" and hasattr(self, 'skull_tab'):
            skull_data = self.skull_tab.get_skull_data()
            if skull_data:
                player_name = skull_data.get("player_name", "").strip()
                texture_value = skull_data.get("texture_value", "").strip()
                display_name = skull_data.get("display_name", "").strip()
                
                # 自定义名称组件
                if display_name:
                    name_json = {"text": display_name}
                    custom_name_component = format_custom_name_component(name_json)
                    if custom_name_component:
                        components["minecraft:custom_name"] = custom_name_component
                
                # 头颅配置文件组件
                if player_name:
                    # 对于预设头颅，直接使用玩家名作为profile值
                    components["minecraft:profile"] = player_name
                elif texture_value:
                    # 对于自定义纹理，需要构建完整的profile JSON字符串
                    import uuid
                    uuid_obj = uuid.uuid4()
                    profile_data = {
                        "id": str(uuid_obj),
                        "name": "Custom",
                        "properties": {
                            "textures": [
                                {
                                    "value": texture_value
                                }
                            ]
                        }
                    }
                    components["minecraft:profile"] = json.dumps(profile_data)
        
        # 食物组件
        if self.food_tab:
            try:
                food_data = self.food_tab.get_food_data()
                if food_data:
                    # Food组件
                    food_component = format_food_component(food_data.get("food"))
                    if food_component:
                        components["minecraft:food"] = food_component
                    
                    # Consumable组件
                    consumable_component = format_consumable_component(food_data.get("consumable"))
                    if consumable_component:
                        components["minecraft:consumable"] = consumable_component
            except ValueError as e:
                messagebox.showerror("错误", str(e))
                return
        
        # 旗帜组件
        if self.banner_tab:
            banner_data = self.banner_tab.get_banner_data()
            if banner_data:
                banner_component = format_banner_component(banner_data)
                if banner_component:
                    components["minecraft:banner_patterns"] = banner_component
        
        # 工具组件
        if self.tool_tab:
            try:
                tool_data = self.tool_tab.generate_tool_component()
                if tool_data:
                    tool_component = format_tool_component(tool_data)
                    if tool_component:
                        components["tool"] = tool_component
            except ValueError as e:
                messagebox.showerror("错误", str(e))
                return
        
        # 装备组件
        if self.equippable_tab:
            try:
                equippable_data = self.equippable_tab.generate_equippable_component()
                if equippable_data:
                    # equippable_data已经包含了多个组件（equippable、glider、death_protection）
                    # 直接将所有组件添加到components中
                    components.update(equippable_data)
            except ValueError as e:
                messagebox.showerror("错误", str(e))
                return
        
        # 成书组件
        if self.written_book_tab:
            try:
                written_book_data = self.written_book_tab.generate_written_book_component()
                if written_book_data:
                    written_book_component = format_written_book_component(written_book_data)
                    if written_book_component:
                        components["written_book_content"] = written_book_component
            except Exception as e:
                messagebox.showerror("错误", f"生成成书组件时出错: {str(e)}")
                return
        
        # 其他属性组件
        unbreakable = self.unbreakable_var.get()
        damage = self.damage_var.get().strip()
        model_data = self.model_data_var.get().strip()
        
        other_components = format_other_components(unbreakable, damage, model_data, None)
        if other_components:
            components.update(other_components)
        
        # 可破坏方块（CanDestroy）
        can_destroy = self.can_destroy_var.get().strip()
        if can_destroy:
            blocks = [block.strip() for block in can_destroy.split(',') if block.strip()]
            if blocks:
                components["minecraft:can_break"] = {"blocks": blocks}
        
        # 可放置方块（CanPlaceOn）
        can_place_on = self.can_place_on_var.get().strip()
        if can_place_on:
            blocks = [block.strip() for block in can_place_on.split(',') if block.strip()]
            if blocks:
                components["minecraft:can_place_on"] = {"blocks": blocks}
        
        # 修复材料
        repair_material = self.repair_material_var.get().strip()
        if repair_material:
            # 如果是显示名称，转换为对应的物品ID
            if repair_material in self.item_id_map:
                repair_material = self.item_id_map[repair_material]
            components["minecraft:repairable"] = {"items": [repair_material]}
        
        # 父母信息（用于生物头颅）
        parents = self.parents_var.get().strip()
        if parents:
            components["minecraft:parents"] = parents
        
        # 新属性设置
        # damage=：非负整数，指物品的初始消耗耐久点数
        damage_value = self.damage_var.get().strip()
        if damage_value:
            try:
                damage_int = int(damage_value)
                if damage_int >= 0:
                    components["minecraft:damage"] = damage_int
            except ValueError:
                pass
        
        # max_stack_size=：正整数，指物品的最大堆叠数
        max_stack_size = self.max_stack_size_var.get().strip()
        if max_stack_size:
            try:
                max_stack_int = int(max_stack_size)
                if max_stack_int > 0:
                    components["minecraft:max_stack_size"] = max_stack_int
            except ValueError:
                pass
        
        # repair_cost=：正整数，就是用铁砧修复时需要的经验等级惩罚
        repair_cost = self.repair_cost_var.get().strip()
        if repair_cost:
            try:
                repair_cost_int = int(repair_cost)
                if repair_cost_int > 0:
                    components["minecraft:repair_cost"] = repair_cost_int
            except ValueError:
                pass
        
        # use_remainder={id:id,count:n}：拿着这种物品右键时能出现n个id所对应的物品
        use_remainder_id = self.use_remainder_id_var.get().strip()
        use_remainder_count = self.use_remainder_count_var.get().strip()
        if use_remainder_id and use_remainder_count:
            # 如果是显示名称，转换为对应的物品ID
            if use_remainder_id in self.item_id_map:
                use_remainder_id = self.item_id_map[use_remainder_id]
                
            try:
                remainder_count = int(use_remainder_count)
                if remainder_count > 0:
                    components["minecraft:use_remainder"] = {
                        "id": use_remainder_id,
                        "count": remainder_count
                    }
            except ValueError:
                pass
        
        # use_cooldown={seconds:正数}：物品使用的冷却时间
        use_cooldown = self.use_cooldown_var.get().strip()
        if use_cooldown:
            try:
                cooldown_float = float(use_cooldown)
                if cooldown_float > 0:
                    components["minecraft:use_cooldown"] = {
                        "seconds": cooldown_float
                    }
            except ValueError:
                pass
        
        # entity_data={id:id,Invisible:1b/0b}：实体类物品产生的实体名称和是否隐身
        entity_id = self.entity_id_var.get().strip()
        entity_invisible = self.entity_invisible_var.get()
        if entity_id:
            # 如果是显示名称，转换为对应的实体ID
            if entity_id in self.entity_id_map:
                entity_id = self.entity_id_map[entity_id]
                
            components["minecraft:entity_data"] = {
                "id": entity_id,
                "Invisible": 1 if entity_invisible else 0
            }
        
        # hide_additional_tooltip={}：是否会显示nbt属性
        if self.hide_additional_tooltip_var.get():
            components["minecraft:hide_additional_tooltip"] = {}
        
        # tooltip_display组件
        tooltip_display = {}
        
        # hide_tooltip
        if self.hide_tooltip_var.get():
            tooltip_display["hide_tooltip"] = True
        
        # hidden_components
        hidden_components = []
        for i in range(self.hidden_components_listbox.size()):
            hidden_components.append(self.hidden_components_listbox.get(i))
        
        if hidden_components:
            tooltip_display["hidden_components"] = hidden_components
        
        # 如果tooltip_display有内容，添加到组件中
        if tooltip_display:
            components["minecraft:tooltip_display"] = tooltip_display
        
        # 构建命令 - 使用新的组件格式
        command = f"/give @p {item_id}"
        
        if components:
            # 将组件转换为字符串格式
            component_str = self.components_to_string(components)
            command += component_str
        
        command += f" {count_int}"
        
        # 显示命令 - 确保命令显示框可见
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, command)
        
        # 确保命令显示框可见
        self.command_text.see(1.0)
    
    def components_to_string(self, components):
        """将组件字典转换为字符串格式"""
        if not components:
            return ""
        
        parts = []
        for component_name, component_value in components.items():
            if isinstance(component_value, dict):
                if not component_value:
                    # 空字典，如 unbreakable={}
                    parts.append(f"{component_name}={{}}")
                else:
                    # 非空字典
                    value_str = self.dict_to_snbt(component_value)
                    parts.append(f"{component_name}={value_str}")
            elif isinstance(component_value, list):
                # 列表
                value_str = self.list_to_snbt(component_value)
                parts.append(f"{component_name}={value_str}")
            elif isinstance(component_value, str):
                # 字符串，需要转义
                escaped_value = component_value.replace('\\', '\\\\').replace('"', '\\"')
                parts.append(f'{component_name}="{escaped_value}"')
            elif isinstance(component_value, bool):
                # 布尔值
                parts.append(f"{component_name}:{'true' if component_value else 'false'}")
            elif isinstance(component_value, int):
                # 整数
                parts.append(f"{component_name}={component_value}")
            elif isinstance(component_value, float):
                # 浮点数
                parts.append(f"{component_name}={component_value}")
        
        return "[" + ",".join(parts) + "]"
    
    def dict_to_snbt(self, data):
        """将字典转换为SNBT格式字符串"""
        if not data:
            return ""
        
        parts = []
        for key, value in data.items():
            # 保留组件名称中的minecraft:前缀
            # 组件名称需要完整的命名空间前缀，例如 minecraft:attribute_modifiers
            
            if isinstance(value, dict):
                value_str = self.dict_to_snbt(value)
                parts.append(f"{key}:{value_str}")
            elif isinstance(value, list):
                value_str = self.list_to_snbt(value)
                parts.append(f"{key}:{value_str}")
            elif isinstance(value, str):
                # 检查是否已经是JSON字符串
                if value.startswith('{') or value.startswith('['):
                    # 已经是JSON格式，直接使用
                    parts.append(f'{key}:{value}')
                else:
                    # 普通字符串，需要转义
                    escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                    parts.append(f'{key}:"{escaped_value}"')
            elif isinstance(value, bool):
                parts.append(f"{key}:{'1b' if value else '0b'}")
            elif isinstance(value, int):
                parts.append(f"{key}:{value}")
            elif isinstance(value, float):
                # 检查是否为整数浮点数（如 11.0）
                if value.is_integer():
                    # 整数浮点数使用整数格式
                    parts.append(f"{key}:{int(value)}")
                else:
                    # 非整数浮点数使用浮点数格式，带f后缀
                    parts.append(f"{key}:{value}f")
        
        return "{" + ",".join(parts) + "}"
    
    def list_to_snbt(self, data):
        """将列表转换为SNBT格式字符串"""
        if not data:
            return "[]"
        
        parts = []
        for item in data:
            if isinstance(item, dict):
                parts.append(self.dict_to_snbt(item))
            elif isinstance(item, list):
                parts.append(self.list_to_snbt(item))
            elif isinstance(item, str):
                # 检查是否已经是JSON字符串
                if item.startswith('{') or item.startswith('['):
                    # 已经是JSON格式，直接使用
                    parts.append(item)
                else:
                    # 普通字符串，需要转义
                    escaped_item = item.replace('\\', '\\\\').replace('"', '\\"')
                    parts.append(f'"{escaped_item}"')
            elif isinstance(item, bool):
                parts.append(f"{'true' if item else 'false'}")
            elif isinstance(item, int):
                parts.append(str(item))
            elif isinstance(item, float):
                parts.append(f"{item}d")
        
        return "[" + ",".join(parts) + "]"
    
    def dict_to_nbt(self, data, level=0):
        """将字典转换为Minecraft NBT格式的字符串，确保正确的引号和转义"""
        if not data:
            return ""
        
        parts = []
        for key, value in data.items():
            if key == "UUID" and isinstance(value, list):
                # 特殊处理UUID，格式为 [I;数字1,数字2,数字3,数字4]
                uuid_str = ",".join(str(x) for x in value)
                parts.append(f'"{key}":[I;{uuid_str}]')
            elif key in ["Colors", "FadeColors"] and isinstance(value, list):
                # 特殊处理烟花颜色，格式为 [I;颜色值1,颜色值2,...]
                color_str = ",".join(str(x) for x in value)
                parts.append(f'"{key}":[I;{color_str}]')
            elif key == "CustomPotionEffects" and isinstance(value, list):
                # 特殊处理药水效果，确保Id使用正确的数字格式
                effect_parts = []
                for effect in value:
                    effect_str_parts = []
                    for effect_key, effect_value in effect.items():
                        if effect_key == "Id":
                            # 药水效果ID使用数字格式
                            effect_str_parts.append(f'"{effect_key}":{effect_value}')
                        elif isinstance(effect_value, bool):
                            effect_str_parts.append(f'"{effect_key}":{1 if effect_value else 0}')
                        else:
                            effect_str_parts.append(f'"{effect_key}":{effect_value}')
                    effect_parts.append("{" + ",".join(effect_str_parts) + "}")
                parts.append(f'"{key}":[{"|".join(effect_parts)}]')
            elif isinstance(value, dict):
                parts.append(f'"{key}":{self.dict_to_nbt(value, level+1)}')
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    # 列表中的字典（如附魔、属性修饰符）
                    list_parts = [self.dict_to_nbt(item, level+1) for item in value]
                    parts.append(f'"{key}":[{"|".join(list_parts)}]')
                else:
                    # 普通列表（如Lore）
                    # 确保列表中的字符串正确转义
                    escaped_list = []
                    for item in value:
                        if isinstance(item, str):
                            # 转义字符串中的特殊字符
                            escaped_item = item.replace('\\', '\\\\').replace('"', '\\"')
                            escaped_list.append(f'"{escaped_item}"')
                        else:
                            escaped_list.append(str(item))
                    parts.append(f'"{key}":[{"|".join(escaped_list)}]')
            elif isinstance(value, str):
                # 转义字符串中的特殊字符
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                parts.append(f'"{key}":"{escaped_value}"')
            elif isinstance(value, bool):
                parts.append(f'"{key}":{1 if value else 0}')
            elif isinstance(value, int):
                parts.append(f'"{key}":{value}')
            elif isinstance(value, float):
                # 注意：这里使用d而不是f，因为Minecraft使用双精度浮点数
                parts.append(f'"{key}":{value}d')
            else:
                parts.append(f'"{key}":{value}')
        
        return "{" + "|".join(parts) + "}"
    
    def copy_command(self):
        command = self.command_text.get(1.0, tk.END).strip()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
        else:
            messagebox.showerror("错误", "没有可复制的命令")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftGiveGenerator(root)
    root.mainloop()