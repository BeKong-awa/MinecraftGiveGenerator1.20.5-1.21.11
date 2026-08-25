import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import os

class PotionEffectsTab:
    def __init__(self, parent):
        self.parent = parent
        self.potion_effects = []
        
        # 药水效果ID与中文名称映射 - 使用数字ID
        self.potion_effect_map = {}
        
        # 加载药水效果列表
        self.load_potion_effects()
        
        self.create_potion_tab()
    
    def load_potion_effects(self):
        """从potion_effect_numeric_id.txt文件加载药水效果映射"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), "..", "txt_files", "potion_effect_numeric_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, effect_id = line.split(',', 1)
                        self.potion_effect_map[chinese_name] = int(effect_id)
        except FileNotFoundError:
            # 如果文件不存在，使用默认药水效果
            self.potion_effect_map = {
                "速度": 1,
                "缓慢": 2,
                "急迫": 3,
                "挖掘疲劳": 4,
                "力量": 5,
                "瞬间治疗": 6,
                "瞬间伤害": 7,
                "跳跃提升": 8,
                "反胃": 9,
                "生命恢复": 10,
                "抗性": 11,
                "防火": 12,
                "水下呼吸": 13,
                "隐身": 14,
                "失明": 15,
                "夜视": 16,
                "饥饿": 17,
                "虚弱": 18,
                "中毒": 19,
                "凋零": 20,
                "生命提升": 21,
                "吸收": 22,
                "饱和": 23,
                "幸运": 24,
                "缓降": 25,
                "潮涌能量": 26,
                "海豚的恩惠": 27,
                "不祥之兆": 28,
                "村庄英雄": 29,
                "黑暗": 30
            }
            # 尝试创建默认文件
            try:
                file_path = os.path.join(os.path.dirname(__file__), "..", "txt_files", "potion_effect_numeric_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, effect_id in self.potion_effect_map.items():
                        f.write(f"{chinese_name},{effect_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def create_potion_tab(self):
        # 药水效果列表框架
        potion_list_frame = ttk.Frame(self.parent)
        potion_list_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # 添加药水效果的控件
        ttk.Label(potion_list_frame, text="效果:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.potion_effect = ttk.Combobox(potion_list_frame, width=25)
        self.potion_effect['values'] = list(self.potion_effect_map.keys())
        self.potion_effect.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(potion_list_frame, text="等级:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.potion_amplifier = ttk.Entry(potion_list_frame, width=10)
        self.potion_amplifier.insert(0, "0")  # 默认等级0
        self.potion_amplifier.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        ttk.Label(potion_list_frame, text="持续时间(秒):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.potion_duration = ttk.Entry(potion_list_frame, width=10)
        self.potion_duration.insert(0, "30")  # 默认30秒
        self.potion_duration.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 显示粒子效果选项
        self.potion_particles = tk.BooleanVar(value=True)
        ttk.Checkbutton(potion_list_frame, text="显示粒子", variable=self.potion_particles).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # 环境效果选项
        self.potion_ambient = tk.BooleanVar(value=False)
        ttk.Checkbutton(potion_list_frame, text="环境效果", variable=self.potion_ambient).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        ttk.Button(potion_list_frame, text="添加效果", command=self.add_potion_effect).grid(row=1, column=4, pady=5)
        
        # 药水颜色选择
        ttk.Label(self.parent, text="药水颜色:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.potion_color_frame = ttk.Frame(self.parent)
        self.potion_color_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.potion_color_var = tk.StringVar(value="#FF0000")
        self.potion_color_entry = ttk.Entry(self.potion_color_frame, textvariable=self.potion_color_var, width=10)
        self.potion_color_entry.grid(row=0, column=0, padx=(0, 5))
        
        self.potion_color_button = ttk.Button(self.potion_color_frame, text="选择颜色", command=self.choose_potion_color)
        self.potion_color_button.grid(row=0, column=1)
        
        # 显示颜色预览
        self.potion_color_preview = tk.Label(self.potion_color_frame, text="    ", bg="#FF0000", relief="solid", bd=1)
        self.potion_color_preview.grid(row=0, column=2, padx=(5, 0))
        
        # 药水效果列表显示
        ttk.Label(self.parent, text="已添加的药水效果:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.potion_listbox = tk.Listbox(self.parent, height=6)
        self.potion_listbox.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.parent)
        button_frame.grid(row=5, column=0, columnspan=4, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_potion_effect).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空列表", command=self.clear_potion_effects).pack(side=tk.LEFT, padx=5)
        
        potion_list_frame.columnconfigure(1, weight=1)
        self.parent.columnconfigure(0, weight=1)
    
    def choose_potion_color(self):
        """选择药水颜色"""
        color_code = colorchooser.askcolor(title="选择药水颜色", initialcolor=self.potion_color_var.get())
        if color_code[1]:  # 用户选择了颜色
            self.potion_color_var.set(color_code[1])
            self.potion_color_preview.config(bg=color_code[1])
    
    def add_potion_effect(self):
        """添加药水效果"""
        effect_name = self.potion_effect.get().strip()
        amplifier = self.potion_amplifier.get().strip()
        duration = self.potion_duration.get().strip()
        
        if not effect_name or not amplifier or not duration:
            messagebox.showerror("错误", "请填写效果、等级和持续时间")
            return
        
        if effect_name not in self.potion_effect_map:
            messagebox.showerror("错误", "请选择有效的效果")
            return
        
        try:
            amplifier_int = int(amplifier)
            if amplifier_int < 0:
                raise ValueError("等级必须为非负整数")
        except ValueError:
            messagebox.showerror("错误", "等级必须为非负整数")
            return
        
        try:
            # 将秒转换为游戏刻 (1秒 = 20游戏刻)
            duration_ticks = int(float(duration) * 20)
            if duration_ticks < 0:
                raise ValueError("持续时间必须为非负数")
        except ValueError:
            messagebox.showerror("错误", "持续时间必须是数字")
            return
        
        effect_data = {
            "Id": self.potion_effect_map[effect_name],
            "Amplifier": amplifier_int,
            "Duration": duration_ticks,
            "ShowParticles": self.potion_particles.get(),
            "Ambient": self.potion_ambient.get()
        }
        
        self.potion_effects.append(effect_data)
        self.update_potion_listbox()
        
        # 清空输入框
        self.potion_effect.set('')
        self.potion_amplifier.delete(0, tk.END)
        self.potion_amplifier.insert(0, "0")
        self.potion_duration.delete(0, tk.END)
        self.potion_duration.insert(0, "30")
    
    def remove_potion_effect(self):
        """删除选中的药水效果"""
        selected = self.potion_listbox.curselection()
        if selected:
            index = selected[0]
            del self.potion_effects[index]
            self.update_potion_listbox()
    
    def clear_potion_effects(self):
        """清空所有药水效果"""
        self.potion_effects = []
        self.update_potion_listbox()
    
    def update_potion_listbox(self):
        """更新药水效果列表框"""
        self.potion_listbox.delete(0, tk.END)
        for effect in self.potion_effects:
            # 查找中文名称
            chinese_name = "未知效果"
            for name, id_val in self.potion_effect_map.items():
                if id_val == effect["Id"]:
                    chinese_name = name
                    break
            duration_seconds = effect["Duration"] / 20
            self.potion_listbox.insert(tk.END, f"{chinese_name} (等级 {effect['Amplifier']}, {duration_seconds}秒)")
    
    def get_potion_effects(self):
        """获取药水效果数据"""
        return self.potion_effects
    
    def get_potion_color(self):
        """获取药水颜色"""
        return self.potion_color_var.get()
    
    def set_potion_effects(self, effects):
        """设置药水效果数据（用于加载）"""
        self.potion_effects = effects
        self.update_potion_listbox()