import tkinter as tk
from tkinter import ttk
import os
import webbrowser
import sys

class EquippableGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.generate_equippable_var = tk.BooleanVar(value=False)
        
        # 装备声音映射
        self.equip_sound_map = {}
        
        # 实体ID映射
        self.entity_map = {}
        
        # 已选择的实体集合
        self.selected_entities = []
        
        # 加载配置文件
        self.load_equip_sounds()
        self.load_entities()
        
        self.create_widgets()
    
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
    
    def load_equip_sounds(self):
        """从equip_sound_id.txt文件加载装备声音映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "equip_sound_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, sound_id = line.split(',', 1)
                        self.equip_sound_map[chinese_name] = sound_id
        except FileNotFoundError:
            pass
    
    def load_entities(self):
        """从entity_id.txt文件加载实体ID映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "entity_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, entity_id = line.split(',', 1)
                        self.entity_map[chinese_name] = entity_id
        except FileNotFoundError:
            pass
    
    def create_widgets(self):
        # 生成装备组件勾选框 - 使用更显眼的样式
        generate_frame = ttk.Frame(self.parent)
        generate_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 使用LabelFrame来突出显示
        generate_label_frame = ttk.LabelFrame(generate_frame, text="组件设置", padding="10")
        generate_label_frame.pack(fill=tk.X, padx=5)
        
        # 创建一个更显眼的勾选框
        generate_checkbutton = ttk.Checkbutton(generate_label_frame, text="生成装备组件", variable=self.generate_equippable_var)
        generate_checkbutton.pack(side=tk.LEFT, padx=5)
        
        # 装备属性框架
        equippable_frame = ttk.LabelFrame(self.parent, text="装备属性(equippable)", padding="10")
        equippable_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 装备槽位
        ttk.Label(equippable_frame, text="装备槽位(slot):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.slot_var = tk.StringVar(value="chest")
        slot_combobox = ttk.Combobox(equippable_frame, textvariable=self.slot_var, width=15, state="readonly")
        slot_combobox['values'] = ("head", "chest", "legs", "feet", "body", "mainhand", "offhand")
        slot_combobox.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(equippable_frame, text="(head:头部, chest:胸部, legs:腿部, feet:脚部, body:身体, mainhand:主手, offhand:副手)").grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # 装备模型
        ttk.Label(equippable_frame, text="装备模型(model):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar()
        self.model_entry = ttk.Entry(equippable_frame, textvariable=self.model_var, width=30)
        self.model_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(equippable_frame, text="(可选，留空则使用默认模型)").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # 装备声音
        ttk.Label(equippable_frame, text="装备声音(equip_sound):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.equip_sound_var = tk.StringVar()
        equip_sound_combobox = ttk.Combobox(equippable_frame, textvariable=self.equip_sound_var, width=25, state="readonly")
        equip_sound_combobox['values'] = list(self.equip_sound_map.keys())
        if self.equip_sound_map:
            self.equip_sound_var.set(list(self.equip_sound_map.keys())[0])
        equip_sound_combobox.grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Label(equippable_frame, text="(可选，选择装备声音)").grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # 相机遮罩
        ttk.Label(equippable_frame, text="相机遮罩(camera_overlay):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.camera_overlay_var = tk.StringVar()
        self.camera_overlay_entry = ttk.Entry(equippable_frame, textvariable=self.camera_overlay_var, width=30)
        self.camera_overlay_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(equippable_frame, text="(可选，命名空间ID，如:misc/pumpkin_blur)").grid(row=3, column=2, sticky=tk.W, pady=5)
        
        # 可被发射器装备
        self.dispensable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(equippable_frame, text="可被发射器装备(dispensable)", variable=self.dispensable_var).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # 可交换
        self.swappable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(equippable_frame, text="可交换(swappable)", variable=self.swappable_var).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # 受伤时受损
        self.damage_on_hurt_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(equippable_frame, text="受伤时受损(damage_on_hurt)", variable=self.damage_on_hurt_var).grid(row=4, column=2, sticky=tk.W, pady=5)
        
        # 允许的实体框架
        entity_frame = ttk.LabelFrame(equippable_frame, text="允许的实体(allowed_entities)", padding="5")
        entity_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 实体下拉列表
        ttk.Label(entity_frame, text="选择实体:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entity_var = tk.StringVar()
        entity_combobox = ttk.Combobox(entity_frame, textvariable=self.entity_var, width=20, state="readonly")
        entity_combobox['values'] = list(self.entity_map.keys())
        entity_combobox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 添加实体按钮
        ttk.Button(entity_frame, text="添加", command=self.add_entity).grid(row=0, column=2, padx=5)
        
        # 实体列表显示
        ttk.Label(entity_frame, text="已选择的实体:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entities_listbox = tk.Listbox(entity_frame, height=5, width=40)
        self.entities_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 删除实体按钮
        button_frame = ttk.Frame(entity_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)
        ttk.Button(button_frame, text="删除选中", command=self.remove_entity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空全部", command=self.clear_entities).pack(side=tk.LEFT, padx=5)
        
        # 特殊功能框架 - 放到允许的实体右边
        special_frame = ttk.LabelFrame(equippable_frame, text="特殊功能", padding="10")
        special_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 滑翔功能
        self.glider_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(special_frame, text="滑翔功能(glider) - 允许物品像鞘翅一样滑翔", variable=self.glider_var).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # 死亡保护
        self.death_protection_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(special_frame, text="死亡保护(death_protection) - 死亡时消耗此物品并保留物品栏", variable=self.death_protection_var).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # 配置权重
        equippable_frame.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)
    
    def add_entity(self):
        """添加实体到列表"""
        entity_name = self.entity_var.get().strip()
        if entity_name and entity_name in self.entity_map:
            entity_id = self.entity_map[entity_name]
            if entity_id not in self.selected_entities:
                self.selected_entities.append(entity_id)
                self.update_entities_listbox()
    
    def remove_entity(self):
        """删除选中的实体"""
        selection = self.entities_listbox.curselection()
        if selection:
            index = selection[0]
            del self.selected_entities[index]
            self.update_entities_listbox()
    
    def clear_entities(self):
        """清空所有实体"""
        self.selected_entities = []
        self.update_entities_listbox()
    
    def update_entities_listbox(self):
        """更新实体列表显示"""
        self.entities_listbox.delete(0, tk.END)
        for entity_id in self.selected_entities:
            # 查找对应的中文名称
            chinese_name = next((name for name, eid in self.entity_map.items() if eid == entity_id), entity_id)
            self.entities_listbox.insert(tk.END, f"{chinese_name} ({entity_id})")
    

    
    def generate_equippable_component(self):
        """生成装备组件"""
        # 如果未勾选生成装备组件，返回None
        if not self.generate_equippable_var.get():
            return None
        
        components = {}
        
        # 装备槽位
        slot = self.slot_var.get().strip()
        if slot:
            components["slot"] = slot
        
        # 装备模型
        model = self.model_var.get().strip()
        if model:
            components["model"] = model
        
        # 装备声音
        equip_sound_name = self.equip_sound_var.get().strip()
        if equip_sound_name and equip_sound_name in self.equip_sound_map:
            components["equip_sound"] = self.equip_sound_map[equip_sound_name]
        
        # 相机遮罩
        camera_overlay = self.camera_overlay_var.get().strip()
        if camera_overlay:
            components["camera_overlay"] = camera_overlay
        
        # 允许的实体
        if self.selected_entities:
            components["allowed_entities"] = self.selected_entities
        
        # 可被发射器装备
        dispensable = self.dispensable_var.get()
        components["dispensable"] = dispensable
        
        # 可交换
        swappable = self.swappable_var.get()
        components["swappable"] = swappable
        
        # 受伤时受损
        damage_on_hurt = self.damage_on_hurt_var.get()
        components["damage_on_hurt"] = damage_on_hurt
        
        # 返回equippable组件
        equippable_component = components
        
        # 构建最终结果，包含equippable、glider和death_protection组件
        result = {}
        
        # 添加equippable组件
        if equippable_component:
            result["equippable"] = equippable_component
        
        # 滑翔功能 - 独立组件
        glider = self.glider_var.get()
        if glider:
            result["glider"] = {}
        
        # 死亡保护 - 独立组件
        death_protection = self.death_protection_var.get()
        if death_protection:
            result["death_protection"] = {}
        
        return result
