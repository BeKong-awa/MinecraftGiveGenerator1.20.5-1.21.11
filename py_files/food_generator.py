import tkinter as tk
from tkinter import ttk, messagebox
import os

class FoodGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        
        # 动画映射
        self.animation_map = {}
        
        # 音效映射
        self.sound_map = {}
        
        # 效果类型映射
        self.effect_type_map = {}
        
        # 药水效果映射
        self.potion_effect_map = {}
        
        # 存储添加的效果
        self.consume_effects = []
        
        # 是否生成食物组件的标志
        self.generate_food_var = tk.BooleanVar(value=False)
        
        # 加载配置文件
        self.load_animations()
        self.load_sounds()
        self.load_effect_types()
        self.load_potion_effects()
        
        self.create_food_tab()
    
    def get_txt_files_path(self):
        """获取txt_files目录的正确路径"""
        import sys
        import os
        # 检查是否是打包后的环境
        if getattr(sys, 'frozen', False):
            # 打包后的环境，获取exe文件所在目录
            base_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境，使用文件所在目录的上级目录
            base_dir = os.path.dirname(os.path.dirname(__file__))
        
        # 构建txt_files目录路径
        return os.path.join(base_dir, 'txt_files')
    
    def load_animations(self):
        """从food_animation_id.txt文件加载进食动画映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "food_animation_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, animation_id = line.split(',', 1)
                        self.animation_map[chinese_name] = animation_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认动画
            self.animation_map = {
                "吃东西（默认）": "eat",
                "喝东西": "drink",
                "无动画": "none",
                "阻挡": "block",
                "拉弓": "bow",
                "开望远镜": "spyglass",
                "拉弩": "crossbow",
                "扔三叉戟": "spear",
                "吹羊角": "toot_horn",
                "用刷子刷方块": "brush"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                # 确保txt_files目录存在
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "food_animation_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, animation_id in self.animation_map.items():
                        f.write(f"{chinese_name},{animation_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def load_potion_effects(self):
        """从potion_effect_id.txt文件加载药水效果映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "potion_effect_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, effect_id = line.split(',', 1)
                        self.potion_effect_map[chinese_name] = effect_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认药水效果
            self.potion_effect_map = {
                "迅捷": "speed",
                "缓慢": "slowness",
                "急迫": "haste",
                "挖掘疲劳": "mining_fatigue",
                "力量": "strength",
                "瞬间治疗": "instant_health",
                "瞬间伤害": "instant_damage",
                "跳跃提升": "jump_boost",
                "反胃": "nausea",
                "生命恢复": "regeneration",
                "抗性提升": "resistance",
                "抗火": "fire_resistance",
                "水下呼吸": "water_breathing",
                "隐身": "invisibility",
                "失明": "blindness",
                "夜视": "night_vision",
                "饥饿": "hunger",
                "虚弱": "weakness",
                "中毒": "poison",
                "凋零": "wither",
                "发光": "glowing",
                "漂浮": "levitation",
                "幸运": "luck",
                "不幸": "unluck"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "potion_effect_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, effect_id in self.potion_effect_map.items():
                        f.write(f"{chinese_name},{effect_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def load_sounds(self):
        """加载进食音效映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "food_sound_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, sound_id = line.split(',', 1)
                        self.sound_map[chinese_name] = sound_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认音效
            self.sound_map = {
                "吃东西（默认）": "entity.generic.eat",
                "喝东西": "entity.generic.drink",
                "吃苹果": "entity.player.burp",
                "吃蛋糕": "block.cake.add_candle",
                "吃面包": "entity.generic.eat",
                "吃肉": "entity.generic.eat",
                "吃鱼": "entity.generic.eat",
                "吃水果": "entity.generic.eat",
                "吃蘑菇": "entity.generic.eat",
                "吃胡萝卜": "entity.generic.eat",
                "吃马铃薯": "entity.generic.eat",
                "吃甜菜根": "entity.generic.eat",
                "吃南瓜派": "entity.generic.eat",
                "吃曲奇": "entity.generic.eat",
                "吃浆果": "entity.generic.eat",
                "吃蜂蜜瓶": "entity.player.burp",
                "喝药水": "entity.generic.drink",
                "喝牛奶": "entity.generic.drink",
                "喝蜂蜜": "entity.player.burp",
                "吃干海带": "entity.generic.eat",
                "吃甜浆果丛": "entity.generic.eat",
                "吃发光浆果": "entity.generic.eat",
                "吃海泡菜": "entity.generic.eat",
                "吃金苹果": "entity.generic.eat",
                "吃附魔金苹果": "entity.generic.eat",
                "吃兔肉": "entity.generic.eat",
                "吃鸡肉": "entity.generic.eat",
                "吃生牛肉": "entity.generic.eat",
                "吃牛排": "entity.generic.eat",
                "吃猪肉": "entity.generic.eat",
                "吃熟猪肉": "entity.generic.eat",
                "吃羊肉": "entity.generic.eat",
                "吃熟羊肉": "entity.generic.eat",
                "吃生鸡肉": "entity.generic.eat",
                "吃熟鸡肉": "entity.generic.eat",
                "吃生兔肉": "entity.generic.eat",
                "吃熟兔肉": "entity.generic.eat",
                "吃生鱼": "entity.generic.eat",
                "吃熟鱼": "entity.generic.eat",
                "吃生鳕鱼": "entity.generic.eat",
                "吃熟鳕鱼": "entity.generic.eat",
                "吃生鲑鱼": "entity.generic.eat",
                "吃熟鲑鱼": "entity.generic.eat",
                "吃河豚": "entity.generic.eat",
                "吃热带鱼": "entity.generic.eat",
                "吃蜘蛛眼": "entity.generic.eat",
                "吃腐肉": "entity.generic.eat",
                "吃河豚": "entity.generic.eat",
                "吃热带鱼": "entity.generic.eat",
                "吃紫颂果": "entity.generic.eat",
                "吃甜浆果": "entity.generic.eat",
                "吃发光浆果": "entity.generic.eat",
                "吃海泡菜": "entity.generic.eat",
                "吃干海带": "entity.generic.eat",
                "吃甜浆果丛": "entity.generic.eat"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "food_sound_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, sound_id in self.sound_map.items():
                        f.write(f"{chinese_name},{sound_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def load_effect_types(self):
        """加载效果类型映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "food_effect_type_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, effect_type_id = line.split(',', 1)
                        self.effect_type_map[chinese_name] = effect_type_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认效果类型
            self.effect_type_map = {
                "添加效果": "add",
                "清除效果": "clear",
                "清除所有效果": "clear_all"
            }
            # 尝试创建默认文件
            try:
                txt_files_path = self.get_txt_files_path()
                os.makedirs(txt_files_path, exist_ok=True)
                file_path = os.path.join(txt_files_path, "food_effect_type_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, effect_type_id in self.effect_type_map.items():
                        f.write(f"{chinese_name},{effect_type_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def create_food_tab(self):
        # 创建两列布局
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        
        # 生成食物组件勾选框 - 使用更显眼的样式
        generate_frame = ttk.Frame(self.parent)
        generate_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 使用LabelFrame来突出显示
        generate_label_frame = ttk.LabelFrame(generate_frame, text="组件设置", padding="10")
        generate_label_frame.pack(fill=tk.X, padx=5)
        
        # 创建一个更显眼的勾选框
        generate_checkbutton = ttk.Checkbutton(generate_label_frame, text="生成食物组件", variable=self.generate_food_var)
        generate_checkbutton.pack(side=tk.LEFT, padx=5)
        
        # Food组件框架 - 左列
        food_frame = ttk.LabelFrame(self.parent, text="Food组件", padding="10")
        food_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        # 饥饿值
        ttk.Label(food_frame, text="饥饿值(nutrition):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nutrition_var = tk.StringVar(value="8")
        ttk.Entry(food_frame, textvariable=self.nutrition_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 饱和度
        ttk.Label(food_frame, text="饱和度(saturation):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.saturation_var = tk.StringVar(value="12.8")
        ttk.Entry(food_frame, textvariable=self.saturation_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 是否随时可吃
        self.can_always_eat_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(food_frame, text="随时可吃(can_always_eat)", variable=self.can_always_eat_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Consumable组件框架 - 右列
        consumable_frame = ttk.LabelFrame(self.parent, text="Consumable组件", padding="10")
        consumable_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))
        
        # 进食时间
        ttk.Label(consumable_frame, text="进食时间(秒):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.consume_seconds_var = tk.StringVar(value="1.6")
        ttk.Entry(consumable_frame, textvariable=self.consume_seconds_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 进食动画
        ttk.Label(consumable_frame, text="进食动画:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.animation_var = tk.StringVar()
        animation_combo = ttk.Combobox(consumable_frame, textvariable=self.animation_var, width=12)
        animation_combo['values'] = list(self.animation_map.keys())
        animation_combo.current(0)
        animation_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 进食音效
        ttk.Label(consumable_frame, text="进食音效:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sound_var = tk.StringVar()
        sound_combo = ttk.Combobox(consumable_frame, textvariable=self.sound_var, width=30)
        sound_combo['values'] = list(self.sound_map.keys())
        sound_combo.current(0)
        sound_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        sound_combo.bind('<KeyRelease>', self.on_sound_search)
        
        # 是否有粒子效果
        self.has_consume_particles_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(consumable_frame, text="有粒子效果", variable=self.has_consume_particles_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 进食效果框架 - 跨两列
        effects_frame = ttk.LabelFrame(self.parent, text="进食效果(on_consume_effects)", padding="10")
        effects_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 效果类型
        ttk.Label(effects_frame, text="效果类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.effect_type_var = tk.StringVar()
        effect_type_combo = ttk.Combobox(effects_frame, textvariable=self.effect_type_var, width=12)
        effect_type_combo['values'] = list(self.effect_type_map.keys())
        effect_type_combo.current(0)
        effect_type_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        effect_type_combo.bind('<<ComboboxSelected>>', self.on_effect_type_changed)
        
        # 获得概率
        ttk.Label(effects_frame, text="获得概率(0-1):").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.probability_var = tk.StringVar(value="1.0")
        self.probability_entry = ttk.Entry(effects_frame, textvariable=self.probability_var, width=10)
        self.probability_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 药水效果选择
        ttk.Label(effects_frame, text="药水效果:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.potion_effect_var = tk.StringVar()
        self.potion_effect_combo = ttk.Combobox(effects_frame, textvariable=self.potion_effect_var, width=15)
        self.potion_effect_combo['values'] = list(self.potion_effect_map.keys())
        self.potion_effect_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 持续时间
        ttk.Label(effects_frame, text="持续时间(秒):").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.effect_duration_var = tk.StringVar(value="60")
        self.effect_duration_entry = ttk.Entry(effects_frame, textvariable=self.effect_duration_var, width=10)
        self.effect_duration_entry.grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 效果等级
        ttk.Label(effects_frame, text="效果等级:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.effect_amplifier_var = tk.StringVar(value="0")
        self.effect_amplifier_entry = ttk.Entry(effects_frame, textvariable=self.effect_amplifier_var, width=15)
        self.effect_amplifier_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 是否为环境效果
        self.effect_ambient_var = tk.BooleanVar(value=False)
        self.effect_ambient_checkbutton = ttk.Checkbutton(effects_frame, text="环境效果", variable=self.effect_ambient_var)
        self.effect_ambient_checkbutton.grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # 是否显示粒子
        self.effect_show_particles_var = tk.BooleanVar(value=True)
        self.effect_show_particles_checkbutton = ttk.Checkbutton(effects_frame, text="显示粒子", variable=self.effect_show_particles_var)
        self.effect_show_particles_checkbutton.grid(row=2, column=3, sticky=tk.W, pady=5)
        
        # 是否显示图标
        self.effect_show_icon_var = tk.BooleanVar(value=True)
        self.effect_show_icon_checkbutton = ttk.Checkbutton(effects_frame, text="显示图标", variable=self.effect_show_icon_var)
        self.effect_show_icon_checkbutton.grid(row=3, column=2, sticky=tk.W, pady=5)
        
        # 添加效果按钮
        ttk.Button(effects_frame, text="添加效果", command=self.add_effect).grid(row=3, column=0, pady=5)
        
        # 效果列表显示
        ttk.Label(effects_frame, text="已添加的效果:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.effect_listbox = tk.Listbox(effects_frame, height=4)
        self.effect_listbox.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架 - 放到右边
        button_frame = ttk.Frame(effects_frame)
        button_frame.grid(row=5, column=2, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.remove_effect).pack(side=tk.TOP, pady=2, fill=tk.X)
        ttk.Button(button_frame, text="清空效果", command=self.clear_effects).pack(side=tk.TOP, pady=2, fill=tk.X)
        
        # 配置权重
        food_frame.columnconfigure(1, weight=1)
        consumable_frame.columnconfigure(1, weight=1)
        effects_frame.columnconfigure(1, weight=1)
        effects_frame.columnconfigure(3, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)
    
    def add_effect(self):
        effect_name = self.potion_effect_var.get().strip()
        duration = self.effect_duration_var.get().strip()
        amplifier = self.effect_amplifier_var.get().strip()
        probability = self.probability_var.get().strip()
        effect_type_name = self.effect_type_var.get().strip()
        
        # 获取效果类型ID
        effect_type_id = self.effect_type_map.get(effect_type_name, "apply_effects")
        
        # 检查是否需要药水效果
        needs_potion_effect = effect_type_id not in ["clear_all_effects", "teleport_randomly"]
        
        if needs_potion_effect:
            if not effect_name:
                messagebox.showerror("错误", "请选择药水效果")
                return
            
            if effect_name not in self.potion_effect_map:
                messagebox.showerror("错误", "请选择有效的药水效果")
                return
        
        try:
            probability_float = float(probability)
            if probability_float < 0 or probability_float > 1:
                raise ValueError("概率必须在0-1之间")
        except ValueError:
            messagebox.showerror("错误", "概率必须在0-1之间")
            return
        
        if effect_type_id == "remove_effects":
            # 移除效果：effects字段是字符串数组，包含要移除的效果ID
            effect_id = self.potion_effect_map[effect_name]
            self.consume_effects.append({
                "type": effect_type_id,
                "probability": probability_float,
                "effects": [effect_id]
            })
        elif effect_type_id in ["clear_all_effects", "teleport_randomly"]:
            # 清除所有效果或随机传送：effects字段为空数组
            self.consume_effects.append({
                "type": effect_type_id,
                "probability": probability_float,
                "effects": []
            })
        else:
            # 添加效果：effects字段是完整的效果对象数组
            try:
                duration_int = int(duration)
                if duration_int < 0:
                    raise ValueError("持续时间必须为非负整数")
            except ValueError:
                messagebox.showerror("错误", "持续时间必须为非负整数")
                return
            
            try:
                amplifier_int = int(amplifier)
                if amplifier_int < 0:
                    raise ValueError("效果等级必须为非负整数")
            except ValueError:
                messagebox.showerror("错误", "效果等级必须为非负整数")
                return
            
            effect_data = {
                "id": self.potion_effect_map[effect_name],
                "duration": duration_int * 20,  # 转换为tick（1秒=20tick）
                "amplifier": amplifier_int,
                "ambient": self.effect_ambient_var.get(),
                "show_particles": self.effect_show_particles_var.get(),
                "show_icon": self.effect_show_icon_var.get()
            }
            
            self.consume_effects.append({
                "type": effect_type_id,
                "probability": probability_float,
                "effects": [effect_data]
            })
        
        self.update_effect_listbox()
        
        # 清空输入框
        self.potion_effect_var.set('')
        self.effect_duration_var.set('60')
        self.effect_amplifier_var.set('0')
    
    def remove_effect(self):
        selected = self.effect_listbox.curselection()
        if selected:
            index = selected[0]
            del self.consume_effects[index]
            self.update_effect_listbox()
    
    def clear_effects(self):
        self.consume_effects = []
        self.update_effect_listbox()
    
    def update_effect_listbox(self):
        self.effect_listbox.delete(0, tk.END)
        for idx, consume_effect in enumerate(self.consume_effects):
            effect_type = consume_effect["type"]
            probability_percent = int(consume_effect["probability"] * 100)
            
            # 根据效果类型显示不同的文本
            if effect_type == "clear_all_effects":
                self.effect_listbox.insert(tk.END, f"{idx+1}. 清除所有效果 (概率:{probability_percent}%)")
            elif effect_type == "teleport_randomly":
                self.effect_listbox.insert(tk.END, f"{idx+1}. 随机传送 (概率:{probability_percent}%)")
            elif effect_type == "remove_effects":
                # 移除效果：effects字段是字符串数组
                effects = consume_effect.get("effects", [])
                if effects and isinstance(effects[0], str):
                    # 查找中文名称
                    chinese_name = "未知效果"
                    effect_id = effects[0]
                    for name, id_val in self.potion_effect_map.items():
                        if id_val == effect_id:
                            chinese_name = name
                            break
                    
                    self.effect_listbox.insert(tk.END, f"{idx+1}. 移除效果: {chinese_name} (概率:{probability_percent}%)")
                else:
                    self.effect_listbox.insert(tk.END, f"{idx+1}. 移除效果 (概率:{probability_percent}%)")
            else:
                # 处理需要药水效果的类型
                effects = consume_effect.get("effects", [])
                if effects and isinstance(effects[0], dict):
                    effect = effects[0]
                    # 查找中文名称
                    chinese_name = "未知效果"
                    for name, id_val in self.potion_effect_map.items():
                        if id_val == effect.get("id", ""):
                            chinese_name = name
                            break
                    
                    duration_seconds = effect.get("duration", 0) // 20
                    self.effect_listbox.insert(tk.END, f"{idx+1}. {chinese_name} (持续时间:{duration_seconds}秒, 概率:{probability_percent}%)")
                else:
                    self.effect_listbox.insert(tk.END, f"{idx+1}. 未知效果 (概率:{probability_percent}%)")
    
    def get_food_data(self):
        """获取食物数据"""
        # 如果未勾选生成食物组件，返回None
        if not self.generate_food_var.get():
            return None
        
        try:
            nutrition = int(self.nutrition_var.get().strip())
        except ValueError:
            raise ValueError("饥饿值必须是整数")
        
        try:
            saturation = float(self.saturation_var.get().strip())
        except ValueError:
            raise ValueError("饱和度必须是数字")
        
        try:
            consume_seconds = float(self.consume_seconds_var.get().strip())
        except ValueError:
            raise ValueError("进食时间必须是数字")
        
        animation_name = self.animation_var.get().strip()
        animation_id = self.animation_map.get(animation_name, "eat")
        
        sound_name = self.sound_var.get().strip()
        sound_id = self.sound_map.get(sound_name, "entity.generic.eat")
        
        # 构建food组件
        food_component = {
            "nutrition": nutrition,
            "saturation": saturation,
            "can_always_eat": self.can_always_eat_var.get()
        }
        
        # 构建consumable组件
        consumable_component = {
            "consume_seconds": consume_seconds,
            "animation": animation_id,
            "sound": sound_id,
            "has_consume_particles": self.has_consume_particles_var.get(),
            "on_consume_effects": self.consume_effects
        }
        
        return {
            "food": food_component,
            "consumable": consumable_component
        }
    
    def clear_inputs(self):
        """清空所有输入"""
        self.nutrition_var.set("8")
        self.saturation_var.set("12.8")
        self.can_always_eat_var.set(False)
        self.consume_seconds_var.set("1.6")
        self.animation_var.set("吃东西（默认）")
        self.sound_var.set("吃东西（默认）")
        self.has_consume_particles_var.set(True)
        self.effect_type_var.set("添加效果")
        self.probability_var.set("1.0")
        self.potion_effect_var.set('')
        self.effect_duration_var.set('60')
        self.effect_amplifier_var.set('0')
        self.effect_ambient_var.set(False)
        self.effect_show_particles_var.set(True)
        self.effect_show_icon_var.set(True)
        self.clear_effects()
    
    def on_sound_search(self, event):
        """当在音效搜索框中输入时，自动过滤音效列表"""
        # 获取当前输入
        value = event.widget.get()
        
        # 如果输入为空，显示所有音效
        if value == '':
            event.widget['values'] = list(self.sound_map.keys())
        else:
            # 过滤包含输入文本的音效名称
            data = []
            for sound in self.sound_map.keys():
                if value.lower() in sound.lower():
                    data.append(sound)
            event.widget['values'] = data
    
    def on_effect_type_changed(self, event):
        """当效果类型改变时，禁用/启用相应的输入框"""
        effect_type_name = event.widget.get()
        effect_type_id = self.effect_type_map.get(effect_type_name, "apply_effects")
        
        # 根据效果类型禁用/启用输入框
        if effect_type_id in ["clear_all_effects", "teleport_randomly"]:
            # 清除所有效果或随机传送：禁用所有药水效果相关的输入框
            self.potion_effect_combo.state(['disabled'])
            self.effect_duration_entry.state(['disabled'])
            self.effect_amplifier_entry.state(['disabled'])
            self.effect_ambient_checkbutton.state(['disabled'])
            self.effect_show_particles_checkbutton.state(['disabled'])
            self.effect_show_icon_checkbutton.state(['disabled'])
        elif effect_type_id == "remove_effects":
            # 移除效果：只启用药水效果选择，禁用其他
            self.potion_effect_combo.state(['!disabled'])
            self.effect_duration_entry.state(['disabled'])
            self.effect_amplifier_entry.state(['disabled'])
            self.effect_ambient_checkbutton.state(['disabled'])
            self.effect_show_particles_checkbutton.state(['disabled'])
            self.effect_show_icon_checkbutton.state(['disabled'])
        else:
            # 添加效果：启用所有输入框
            self.potion_effect_combo.state(['!disabled'])
            self.effect_duration_entry.state(['!disabled'])
            self.effect_amplifier_entry.state(['!disabled'])
            self.effect_ambient_checkbutton.state(['!disabled'])
            self.effect_show_particles_checkbutton.state(['!disabled'])
            self.effect_show_icon_checkbutton.state(['!disabled'])
