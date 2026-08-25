import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import base64

class SkullGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.skull_data = {}
        
        # 预设头颅映射
        self.preset_skulls = {
            "苦力怕头颅": "MHF_Creeper",
            "凋灵骷髅头颅": "MHF_WSkeleton",
            "僵尸头颅": "MHF_Zombie",
            "末影人头颅": "MHF_Enderman",
            "猪灵头颅": "MHF_Piglin",
            "村民头颅": "MHF_Villager",
            "史蒂夫头颅": "MHF_Steve",
            "艾利克斯头颅": "MHF_Alex",
            "牛头颅": "MHF_Cow",
            "猪头颅": "MHF_Pig",
            "羊头颅": "MHF_Sheep",
            "鸡头颅": "MHF_Chicken",
            "鱿鱼头颅": "MHF_Squid",
            "蘑菇牛头颅": "MHF_MushroomCow",
            "史莱姆头颅": "MHF_Slime",
            "岩浆怪头颅": "MHF_MagmaCube",
            "恶魂头颅": "MHF_Ghast",
            "烈焰人头颅": "MHF_Blaze",
            "骷髅头颅": "MHF_Skeleton",
            "蜘蛛头颅": "MHF_Spider",
            "洞穴蜘蛛头颅": "MHF_CaveSpider",
            "蠹虫头颅": "MHF_Silverfish",
            "末影螨头颅": "MHF_Endermite",
            "守卫者头颅": "MHF_Guardian",
            "远古守卫者头颅": "MHF_ElderGuardian",
            "海豚头颅": "MHF_Dolphin",
            "海龟头颅": "MHF_Turtle",
            "熊猫头颅": "MHF_Panda",
            "狐狸头颅": "MHF_Fox",
            "蜜蜂头颅": "MHF_Bee",
            "山羊头颅": "MHF_Goat",
            "青蛙头颅": "MHF_Frog",
            "监守者头颅": "MHF_Warden",
            "悦灵头颅": "MHF_Allay",
            "嗅探兽头颅": "MHF_Sniffer",
            "铁傀儡头颅": "MHF_IronGolem",
            "雪傀儡头颅": "MHF_SnowGolem",
            "凋灵头颅": "MHF_Wither",
            "末影龙头颅": "MHF_EnderDragon"
        }
        
        self.create_skull_tab()
    
    def create_skull_tab(self):
        # 创建两列布局
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        
        # 预设头颅框架 - 左列
        preset_frame = ttk.LabelFrame(self.parent, text="预设头颅", padding="10")
        preset_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        ttk.Label(preset_frame, text="选择预设头颅:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.preset_skull_var = tk.StringVar()
        self.preset_skull_combo = ttk.Combobox(preset_frame, textvariable=self.preset_skull_var, width=20)
        self.preset_skull_combo['values'] = list(self.preset_skulls.keys())
        self.preset_skull_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.preset_skull_combo.bind('<<ComboboxSelected>>', self.on_preset_skull_selected)
        
        # 自定义头颅框架 - 右列
        custom_frame = ttk.LabelFrame(self.parent, text="自定义头颅", padding="10")
        custom_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))
        
        # 玩家名输入
        ttk.Label(custom_frame, text="玩家名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.player_name = ttk.Entry(custom_frame, width=20)
        self.player_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 自定义纹理值
        ttk.Label(custom_frame, text="自定义纹理值:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.texture_value = tk.Text(custom_frame, height=4, width=30)
        self.texture_value.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 头颅显示名称
        ttk.Label(custom_frame, text="显示名称:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.skull_display_name = ttk.Entry(custom_frame, width=20)
        self.skull_display_name.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架 - 跨两列
        button_frame = ttk.Frame(self.parent)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="清空输入", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        
        # 配置权重
        preset_frame.columnconfigure(1, weight=1)
        custom_frame.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)
    
    def get_skull_data(self):
        """获取头颅数据"""
        player_name = self.player_name.get().strip()
        texture_value = self.texture_value.get("1.0", tk.END).strip()
        display_name = self.skull_display_name.get().strip()
        
        # 收集数据
        skull_data = {
            "player_name": player_name,
            "texture_value": texture_value,
            "display_name": display_name
        }
        
        return skull_data
    
    def on_preset_skull_selected(self, event):
        """当选择预设头颅时，自动填充玩家名"""
        selected_skull = self.preset_skull_var.get()
        if selected_skull in self.preset_skulls:
            self.player_name.delete(0, tk.END)
            self.player_name.insert(0, self.preset_skulls[selected_skull])
            
            # 自动设置显示名称
            self.skull_display_name.delete(0, tk.END)
            self.skull_display_name.insert(0, selected_skull)
    
    def generate_skull_command(self):
        """生成头颅命令（使用新的组件格式）"""
        player_name = self.player_name.get().strip()
        texture_value = self.texture_value.get("1.0", tk.END).strip()
        display_name = self.skull_display_name.get().strip()
        
        if not player_name and not texture_value:
            messagebox.showerror("错误", "请输入玩家名或纹理值")
            return
        
        # 收集组件数据
        components = {}
        
        # 自定义名称组件
        if display_name:
            name_json = {"text": display_name, "type": "text"}
            components["minecraft:custom_name"] = name_json
        
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
            import json
            components["minecraft:profile"] = json.dumps(profile_data)
        
        # 构建完整的give命令
        command = f"/give @p minecraft:player_head"
        
        if components:
            # 将组件转换为字符串格式
            component_str = self.components_to_string(components)
            command += component_str
        
        command += " 1"
        
        # 显示命令
        messagebox.showinfo("生成的头颅命令", f"命令已生成:\n\n{command}\n\n已复制到剪贴板")
        
        # 复制到剪贴板
        self.parent.clipboard_clear()
        self.parent.clipboard_append(command)
    
    def components_to_string(self, components):
        """将组件字典转换为字符串格式"""
        if not components:
            return ""
        
        parts = []
        for component_name, component_value in components.items():
            if isinstance(component_value, dict):
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
                parts.append(f"{component_name}={1 if component_value else 0}b")
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
            # 移除minecraft:前缀（如果存在）
            if key.startswith("minecraft:"):
                key = key[10:]
            
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
                parts.append(f"{key}:{1 if value else 0}b")
            elif isinstance(value, int):
                parts.append(f"{key}:{value}")
            elif isinstance(value, float):
                # 检查是否为整数浮点数（如 11.0）
                if value.is_integer():
                    # 整数浮点数使用整数格式
                    parts.append(f"{key}:{int(value)}")
                else:
                    # 非整数浮点数使用浮点数格式
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
                parts.append(f"{1 if item else 0}b")
            elif isinstance(item, int):
                parts.append(str(item))
            elif isinstance(item, float):
                parts.append(f"{item}d")
        
        return "[" + ",".join(parts) + "]"
    
    def clear_inputs(self):
        """清空所有输入"""
        self.preset_skull_var.set('')
        self.player_name.delete(0, tk.END)
        self.texture_value.delete(1.0, tk.END)
        self.skull_display_name.delete(0, tk.END)
    
    def dict_to_nbt(self, data, level=0):
        """将字典转换为Minecraft NBT格式的字符串"""
        if not data:
            return ""
        
        parts = []
        for key, value in data.items():
            if key == "Id" and isinstance(value, list):
                # 特殊处理UUID，格式为 [I;数字1,数字2,数字3,数字4]
                uuid_str = ",".join(str(x) for x in value)
                parts.append(f'"{key}":[I;{uuid_str}]')
            elif isinstance(value, dict):
                parts.append(f'"{key}":{self.dict_to_nbt(value, level+1)}')
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    # 列表中的字典
                    list_parts = [self.dict_to_nbt(item, level+1) for item in value]
                    parts.append(f'"{key}":[{",".join(list_parts)}]')
                else:
                    # 普通列表
                    escaped_list = []
                    for item in value:
                        if isinstance(item, str):
                            escaped_item = item.replace('\\', '\\\\').replace('"', '\\"')
                            escaped_list.append(f'"{escaped_item}"')
                        else:
                            escaped_list.append(str(item))
                    parts.append(f'"{key}":[{",".join(escaped_list)}]')
            elif isinstance(value, str):
                # 转义字符串中的特殊字符
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                parts.append(f'"{key}":"{escaped_value}"')
            elif isinstance(value, bool):
                parts.append(f'"{key}":{1 if value else 0}')
            elif isinstance(value, int):
                parts.append(f'"{key}":{value}')
            elif isinstance(value, float):
                parts.append(f'"{key}":{value}d')
            else:
                parts.append(f'"{key}":{value}')
        
        return "{" + ",".join(parts) + "}"