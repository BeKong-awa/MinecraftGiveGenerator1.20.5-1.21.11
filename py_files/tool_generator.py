import tkinter as tk
from tkinter import ttk
import os

class ToolGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.rules = []
        self.generate_tool_var = tk.BooleanVar(value=False)
        self.create_widgets()
    
    def create_widgets(self):
        # 生成工具组件勾选框 - 使用更显眼的样式
        generate_frame = ttk.Frame(self.parent)
        generate_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 使用LabelFrame来突出显示
        generate_label_frame = ttk.LabelFrame(generate_frame, text="组件设置", padding="10")
        generate_label_frame.pack(fill=tk.X, padx=5)
        
        # 创建一个更显眼的勾选框
        generate_checkbutton = ttk.Checkbutton(generate_label_frame, text="生成工具组件", variable=self.generate_tool_var)
        generate_checkbutton.pack(side=tk.LEFT, padx=5)
        
        # 工具属性框架
        tool_frame = ttk.LabelFrame(self.parent, text="工具属性(tool)", padding="10")
        tool_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 默认挖掘速度
        ttk.Label(tool_frame, text="默认挖掘速度:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.default_mining_speed_var = tk.StringVar(value="1.0")
        self.default_mining_speed_entry = ttk.Entry(tool_frame, textvariable=self.default_mining_speed_var, width=15)
        self.default_mining_speed_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 每方块消耗耐久度
        ttk.Label(tool_frame, text="每方块消耗耐久度:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.damage_per_block_var = tk.StringVar(value="1")
        self.damage_per_block_entry = ttk.Entry(tool_frame, textvariable=self.damage_per_block_var, width=15)
        self.damage_per_block_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 挖掘规则框架
        rules_frame = ttk.LabelFrame(tool_frame, text="挖掘规则(rules)", padding="10")
        rules_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 方块列表
        ttk.Label(rules_frame, text="方块列表(blocks):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.blocks_var = tk.StringVar()
        self.blocks_entry = ttk.Entry(rules_frame, textvariable=self.blocks_var, width=30)
        self.blocks_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(rules_frame, text="(用逗号分隔，如:minecraft:stone,minecraft:dirt)").grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # 挖掘速度
        ttk.Label(rules_frame, text="挖掘速度(speed):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.speed_var = tk.StringVar(value="1.0f")
        self.speed_entry = ttk.Entry(rules_frame, textvariable=self.speed_var, width=15)
        self.speed_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 精准采集
        self.correct_for_drops_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(rules_frame, text="精准采集(correct_for_drops)", variable=self.correct_for_drops_var).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # 添加规则按钮
        ttk.Button(rules_frame, text="添加规则", command=self.add_rule).grid(row=2, column=0, pady=5)
        
        # 规则列表显示
        ttk.Label(rules_frame, text="已添加的规则:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.rules_listbox = tk.Listbox(rules_frame, height=4)
        self.rules_listbox.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(rules_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空规则", command=self.clear_rules).pack(side=tk.LEFT, padx=5)
        
        # 配置权重
        tool_frame.columnconfigure(1, weight=1)
        tool_frame.columnconfigure(3, weight=1)
        rules_frame.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)
    
    def add_rule(self):
        """添加挖掘规则"""
        blocks = self.blocks_var.get().strip()
        speed_str = self.speed_var.get().strip()
        correct_for_drops = self.correct_for_drops_var.get()
        
        if not blocks:
            return
        
        # 处理速度值，移除f后缀并转换为浮点数
        speed = 1.0
        if speed_str:
            try:
                speed = float(speed_str.rstrip('f'))
            except ValueError:
                speed = 1.0
        
        rule = {
            "blocks": blocks,
            "speed": speed,
            "correct_for_drops": correct_for_drops
        }
        
        self.rules.append(rule)
        self.update_rules_listbox()
        
        # 清空输入
        self.blocks_var.set("")
        self.speed_var.set("1.0f")
        self.correct_for_drops_var.set(False)
    
    def remove_rule(self):
        """删除选中的规则"""
        selection = self.rules_listbox.curselection()
        if selection:
            index = selection[0]
            del self.rules[index]
            self.update_rules_listbox()
    
    def clear_rules(self):
        """清空所有规则"""
        self.rules = []
        self.update_rules_listbox()
    
    def update_rules_listbox(self):
        """更新规则列表显示"""
        self.rules_listbox.delete(0, tk.END)
        for i, rule in enumerate(self.rules):
            blocks = rule["blocks"]
            speed = rule["speed"]
            correct_for_drops = "是" if rule["correct_for_drops"] else "否"
            display_text = f"{i+1}. 方块: {blocks}, 速度: {speed}, 精准采集: {correct_for_drops}"
            self.rules_listbox.insert(tk.END, display_text)
    
    def generate_tool_component(self):
        """生成工具组件"""
        # 如果未勾选生成工具组件，返回None
        if not self.generate_tool_var.get():
            return None
        
        components = {}
        
        # 默认挖掘速度
        default_mining_speed = self.default_mining_speed_var.get().strip()
        if default_mining_speed:
            try:
                components["default_mining_speed"] = float(default_mining_speed)
            except ValueError:
                pass
        
        # 每方块消耗耐久度
        damage_per_block = self.damage_per_block_var.get().strip()
        if damage_per_block:
            try:
                components["damage_per_block"] = int(damage_per_block)
            except ValueError:
                pass
        
        # 挖掘规则
        rules_list = []
        for rule in self.rules:
            rule_dict = {}
            
            # 方块列表
            blocks = rule["blocks"].strip()
            if blocks:
                block_list = [block.strip() for block in blocks.split(',')]
                rule_dict["blocks"] = block_list
            
            # 挖掘速度 - 确保始终包含speed字段
            speed = rule.get("speed", 1.0)
            if isinstance(speed, str):
                try:
                    speed = float(speed.rstrip('f'))
                except ValueError:
                    speed = 1.0
            rule_dict["speed"] = speed
            
            # 精准采集 - 转换为1b或0b格式
            correct_for_drops = rule.get("correct_for_drops", False)
            rule_dict["correct_for_drops"] = 1 if correct_for_drops else 0
            
            if rule_dict:
                rules_list.append(rule_dict)
        
        components["rules"] = rules_list
        
        return components
