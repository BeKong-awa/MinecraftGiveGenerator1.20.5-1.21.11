import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import random

class FireworksTab:
    def __init__(self, parent):
        self.parent = parent
        self.explosions = []
        
        # 烟花类型映射 - 使用字符串格式
        self.firework_types = {
            "小型球状": "small_ball",
            "大型球状": "large_ball",
            "星形": "star",
            "爬行者形状": "creeper",
            "爆裂": "burst"
        }
        
        self.create_fireworks_tab()
    
    def create_fireworks_tab(self):
        # 创建两列布局
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        
        # 基本设置框架 - 放在左列
        basic_frame = ttk.LabelFrame(self.parent, text="基本设置", padding="10")
        basic_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        # 飞行时间
        ttk.Label(basic_frame, text="飞行时间(1-3):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flight_time = ttk.Entry(basic_frame, width=10)
        self.flight_time.insert(0, "1")
        self.flight_time.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 数量
        ttk.Label(basic_frame, text="数量:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.firework_count = ttk.Entry(basic_frame, width=10)
        self.firework_count.insert(0, "1")
        self.firework_count.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 爆炸效果设置框架 - 放在右列
        explosion_frame = ttk.LabelFrame(self.parent, text="爆炸效果", padding="10")
        explosion_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))
        
        # 爆炸类型
        ttk.Label(explosion_frame, text="爆炸类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.explosion_type = ttk.Combobox(explosion_frame, width=15)
        self.explosion_type['values'] = list(self.firework_types.keys())
        self.explosion_type.current(0)
        self.explosion_type.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 主要颜色
        ttk.Label(explosion_frame, text="主要颜色:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.primary_color_frame = ttk.Frame(explosion_frame)
        self.primary_color_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        self.primary_color_var = tk.StringVar(value="#FF0000")
        self.primary_color_entry = ttk.Entry(self.primary_color_frame, textvariable=self.primary_color_var, width=10)
        self.primary_color_entry.grid(row=0, column=0, padx=(0, 5))
        
        self.primary_color_button = ttk.Button(self.primary_color_frame, text="选择颜色", 
                                             command=lambda: self.choose_color(self.primary_color_var, self.primary_color_preview))
        self.primary_color_button.grid(row=0, column=1)
        
        self.primary_color_preview = tk.Label(self.primary_color_frame, text="    ", bg="#FF0000", relief="solid", bd=1)
        self.primary_color_preview.grid(row=0, column=2, padx=(5, 0))
        
        # 淡出颜色
        ttk.Label(explosion_frame, text="淡出颜色:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fade_color_frame = ttk.Frame(explosion_frame)
        self.fade_color_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.fade_color_var = tk.StringVar(value="#0000FF")
        self.fade_color_entry = ttk.Entry(self.fade_color_frame, textvariable=self.fade_color_var, width=10)
        self.fade_color_entry.grid(row=0, column=0, padx=(0, 5))
        
        self.fade_color_button = ttk.Button(self.fade_color_frame, text="选择颜色", 
                                          command=lambda: self.choose_color(self.fade_color_var, self.fade_color_preview))
        self.fade_color_button.grid(row=0, column=1)
        
        self.fade_color_preview = tk.Label(self.fade_color_frame, text="    ", bg="#0000FF", relief="solid", bd=1)
        self.fade_color_preview.grid(row=0, column=2, padx=(5, 0))
        
        # 效果选项
        self.trail_var = tk.BooleanVar()
        ttk.Checkbutton(explosion_frame, text="拖尾效果", variable=self.trail_var).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.flicker_var = tk.BooleanVar()
        ttk.Checkbutton(explosion_frame, text="闪烁效果", variable=self.flicker_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # 添加爆炸效果按钮
        ttk.Button(explosion_frame, text="添加爆炸效果", command=self.add_explosion).grid(row=4, column=0, columnspan=2, pady=10)
        
        # 爆炸效果列表 - 跨两列
        ttk.Label(self.parent, text="已添加的爆炸效果:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.explosion_listbox = tk.Listbox(self.parent, height=6)
        self.explosion_listbox.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架 - 跨两列
        button_frame = ttk.Frame(self.parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_explosion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空列表", command=self.clear_explosions).pack(side=tk.LEFT, padx=5)
        
        # 配置权重
        basic_frame.columnconfigure(1, weight=1)
        explosion_frame.columnconfigure(1, weight=1)
        self.parent.rowconfigure(2, weight=1)  # 列表行可扩展
    
    def choose_color(self, color_var, preview_label):
        """选择颜色"""
        color_code = colorchooser.askcolor(title="选择颜色", initialcolor=color_var.get())
        if color_code[1]:  # 用户选择了颜色
            color_var.set(color_code[1])
            preview_label.config(bg=color_code[1])
    
    def hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_minecraft_color(self, rgb):
        """将RGB颜色转换为Minecraft颜色值"""
        r, g, b = rgb
        return r * 65536 + g * 256 + b
    
    def add_explosion(self):
        """添加爆炸效果"""
        explosion_type = self.explosion_type.get()
        primary_color = self.primary_color_var.get()
        fade_color = self.fade_color_var.get()
        
        if not explosion_type:
            messagebox.showerror("错误", "请选择爆炸类型")
            return
        
        try:
            # 转换颜色
            primary_rgb = self.hex_to_rgb(primary_color)
            primary_mc = self.rgb_to_minecraft_color(primary_rgb)
            
            fade_rgb = self.hex_to_rgb(fade_color)
            fade_mc = self.rgb_to_minecraft_color(fade_rgb)
        except ValueError:
            messagebox.showerror("错误", "颜色格式不正确，请使用十六进制格式（如#FF0000）")
            return
        
        # 使用新的组件格式
        explosion_data = {
            "shape": self.firework_types[explosion_type],
            "colors": [primary_mc],
            "fade_colors": [fade_mc],
            "has_trail": self.trail_var.get(),
            "has_twinkle": self.flicker_var.get()
        }
        
        self.explosions.append(explosion_data)
        self.update_explosion_listbox()
    
    def remove_explosion(self):
        """删除选中的爆炸效果"""
        selected = self.explosion_listbox.curselection()
        if selected:
            index = selected[0]
            del self.explosions[index]
            self.update_explosion_listbox()
    
    def clear_explosions(self):
        """清空所有爆炸效果"""
        self.explosions = []
        self.update_explosion_listbox()
    
    def update_explosion_listbox(self):
        """更新爆炸效果列表框"""
        self.explosion_listbox.delete(0, tk.END)
        for i, explosion in enumerate(self.explosions):
            # 查找类型名称
            type_name = "未知类型"
            for name, type_id in self.firework_types.items():
                if type_id == explosion["shape"]:
                    type_name = name
                    break
            
            trail_text = "有拖尾" if explosion["has_trail"] else "无拖尾"
            flicker_text = "有闪烁" if explosion["has_twinkle"] else "无闪烁"
            
            self.explosion_listbox.insert(tk.END, f"效果 {i+1}: {type_name}, {trail_text}, {flicker_text}")
    
    def get_fireworks_data(self):
        """获取烟花数据（使用新的组件格式）"""
        try:
            flight_time = int(self.flight_time.get())
            if flight_time < 1 or flight_time > 3:
                raise ValueError("飞行时间必须在1-3之间")
        except ValueError:
            raise ValueError("飞行时间必须是1-3之间的整数")
        
        try:
            count = int(self.firework_count.get())
            if count < 1:
                raise ValueError("数量必须为正整数")
        except ValueError:
            raise ValueError("数量必须是正整数")
        
        # 使用新的组件格式
        fireworks_data = {
            "flight_duration": flight_time
        }
        
        if self.explosions:
            fireworks_data["explosions"] = self.explosions
        
        return fireworks_data, count
    
    def set_fireworks_data(self, data):
        """设置烟花数据（用于加载）"""
        # 兼容新旧格式
        flight_key = "flight_duration" if "flight_duration" in data else "Flight"
        if flight_key in data:
            self.flight_time.delete(0, tk.END)
            self.flight_time.insert(0, str(data[flight_key]))
        
        explosions_key = "explosions" if "explosions" in data else "Explosions"
        if explosions_key in data:
            self.explosions = data[explosions_key]
            self.update_explosion_listbox()