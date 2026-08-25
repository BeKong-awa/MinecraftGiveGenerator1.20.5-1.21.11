import tkinter as tk
from tkinter import ttk
import os
import sys
# 添加父目录到Python路径，以便访问txt_files
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class BannerGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.banner_data = {
            "base_color": "white",
            "patterns": []
        }
        
        # 颜色映射
        self.color_map = {
            "白色": "white",
            "淡灰色": "light_gray",
            "灰色": "gray",
            "黑色": "black",
            "棕色": "brown",
            "红色": "red",
            "橙色": "orange",
            "黄色": "yellow",
            "黄绿色": "lime",
            "绿色": "green",
            "青色": "cyan",
            "淡蓝色": "light_blue",
            "蓝色": "blue",
            "紫色": "purple",
            "品红色": "magenta",
            "粉红色": "pink"
        }
        
        # 图案映射 - 从文件加载
        self.pattern_map = {}
        self.load_banner_patterns()
        
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

    def load_banner_patterns(self):
        """从banner_pattern_id.txt文件加载图案映射"""
        try:
            txt_files_path = self.get_txt_files_path()
            file_path = os.path.join(txt_files_path, "banner_pattern_id.txt")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        chinese_name, pattern_id = line.split(',', 1)
                        self.pattern_map[chinese_name] = pattern_id
        except FileNotFoundError:
            # 如果文件不存在，使用默认图案
            self.pattern_map = {
                "底Fully color Field": "base",
                "底横条Base": "stripe_bottom",
                "顶横条Chief": "stripe_top",
                "右竖条Pale Dexter": "stripe_left",
                "左竖条Pale Sinister": "stripe_right",
                "中竖条Pale": "stripe_center",
                "中横条Fess": "stripe_middle",
                "右斜条Bend": "stripe_downright",
                "左斜条Bend Sinister": "stripe_downleft",
                "竖条纹Paly": "small_stripes",
                "斜十字Saltire": "cross",
                "正十字Cross": "straight_cross",
                "右上三角Per Bend Sinister": "diagonal_left",
                "左上三角Per Bend": "diagonal_right",
                "右下三角Per Bend Inverted": "diagonal_up_left",
                "左下三角Per Bend Sinister Inverted": "diagonal_up_right",
                "右半方形Per Pale": "half_vertical",
                "左半方形Per Pale Inverted": "half_vertical_right",
                "上半方形Per Fess": "half_horizontal",
                "下半方形Per Fess Inverted": "half_horizontal_bottom",
                "右底方Base Dexter Canton": "square_bottom_left",
                "左底方Base Sinister Canton": "square_bottom_right",
                "右顶方Chief Dexter Canton": "square_top_left",
                "左顶方Chief Sinister Canton": "square_top_right",
                "底三角Chevron": "triangle_bottom",
                "顶三角Inverted Chevron": "triangle_top",
                "底波纹Base Indented": "triangles_bottom",
                "顶波纹Chief Indented": "triangles_top",
                "圆形Roundel": "circle",
                "菱形Lozenge": "rhombus",
                "方框边Bordure": "border",
                "波纹边Bordure Indented": "curly_border",
                "砖纹Field Masoned": "bricks",
                "自上渐淡Gradient": "gradient",
                "自下渐淡Base Gradient": "gradient_up",
                "苦力怕盾徽Creeper Charge": "creeper",
                "头颅盾徽Skull Charge": "skull",
                "花朵盾徽Flower Charge": "flower",
                "Mojang徽标Thing": "mojang",
                "地球Globe": "globe",
                "猪鼻Snout": "piglin",
                "涡流Flow": "flow",
                "旋风Guster": "guster"
            }
            # 尝试创建默认文件
            try:
                file_path = os.path.join(os.path.dirname(__file__), "..", "txt_files", "banner_pattern_id.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for chinese_name, pattern_id in self.pattern_map.items():
                        f.write(f"{chinese_name},{pattern_id}\n")
            except:
                pass  # 如果无法创建文件，忽略错误
    
    def create_widgets(self):
        # 底色选择
        color_frame = ttk.LabelFrame(self.parent, text="旗帜底色")
        color_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(color_frame, text="选择底色:").pack(anchor=tk.W, pady=3)
        self.color_var = tk.StringVar(value="白色")
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_var, values=list(self.color_map.keys()))
        color_combo.pack(fill=tk.X, pady=3)
        color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        
        # 图案选择
        pattern_frame = ttk.LabelFrame(self.parent, text="图案设置")
        pattern_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 图案类型
        ttk.Label(pattern_frame, text="图案类型:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.pattern_var = tk.StringVar()
        pattern_combo = ttk.Combobox(pattern_frame, textvariable=self.pattern_var, values=list(self.pattern_map.keys()), width=20)
        pattern_combo.grid(row=0, column=1, sticky=tk.W, pady=3)
        
        # 图案颜色
        ttk.Label(pattern_frame, text="图案颜色:").grid(row=0, column=2, sticky=tk.W, pady=3)
        self.pattern_color_var = tk.StringVar(value="黑色")
        pattern_color_combo = ttk.Combobox(pattern_frame, textvariable=self.pattern_color_var, values=list(self.color_map.keys()), width=15)
        pattern_color_combo.grid(row=0, column=3, sticky=tk.W, pady=3)
        
        # 添加图案按钮
        add_pattern_button = ttk.Button(pattern_frame, text="添加图案", command=self.add_pattern)
        add_pattern_button.grid(row=0, column=4, sticky=tk.W, pady=3, padx=5)
        
        # 已添加的图案列表
        ttk.Label(pattern_frame, text="已添加的图案:").grid(row=1, column=0, columnspan=5, sticky=tk.W, pady=3)
        self.pattern_listbox = tk.Listbox(pattern_frame, height=6)
        self.pattern_listbox.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=3)
        
        # 删除图案按钮
        delete_pattern_button = ttk.Button(pattern_frame, text="删除选中图案", command=self.delete_pattern)
        delete_pattern_button.grid(row=2, column=4, sticky=tk.W, pady=3, padx=5)
        
        # 清空图案按钮
        clear_patterns_button = ttk.Button(pattern_frame, text="清空所有图案", command=self.clear_patterns)
        clear_patterns_button.grid(row=3, column=4, sticky=tk.W, pady=3, padx=5)
        
        # 提示信息
        hint_frame = ttk.LabelFrame(self.parent, text="提示")
        hint_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        hint_frame.columnconfigure(0, weight=1)
        
        hint_text = "1. 旗帜最多可以添加6层不同的图案（指令无限制）\n"
        hint_text += "2. 图案添加顺序会影响显示效果\n"
        hint_text += "3. 对装有水的炼药锅使用旗帜可以洗去最上层图案"
        ttk.Label(hint_frame, text=hint_text, justify=tk.LEFT).pack(fill=tk.BOTH, expand=True, pady=3)
        
        pattern_frame.columnconfigure(1, weight=1)
    
    def on_color_change(self, event=None):
        self.banner_data["base_color"] = self.color_map[self.color_var.get()]
    
    def add_pattern(self):
        pattern_name = self.pattern_var.get()
        color_name = self.pattern_color_var.get()
        
        if not pattern_name:
            return
        
        if len(self.banner_data["patterns"]) >= 6:
            return
        
        pattern_id = self.pattern_map[pattern_name]
        color_id = self.color_map[color_name]
        
        pattern_data = {
            "pattern": pattern_id,
            "color": color_id
        }
        
        self.banner_data["patterns"].append(pattern_data)
        self.update_pattern_listbox()
    
    def delete_pattern(self):
        selected = self.pattern_listbox.curselection()
        if selected:
            index = selected[0]
            del self.banner_data["patterns"][index]
            self.update_pattern_listbox()
    
    def clear_patterns(self):
        self.banner_data["patterns"] = []
        self.update_pattern_listbox()
    
    def update_pattern_listbox(self):
        self.pattern_listbox.delete(0, tk.END)
        for i, pattern in enumerate(self.banner_data["patterns"]):
            # 查找图案和颜色的中文名称
            pattern_name = "未知图案"
            color_name = "未知颜色"
            
            for name, id_val in self.pattern_map.items():
                if id_val == pattern["pattern"]:
                    pattern_name = name
                    break
            
            for name, id_val in self.color_map.items():
                if id_val == pattern["color"]:
                    color_name = name
                    break
            
            self.pattern_listbox.insert(tk.END, f"{i+1}. {pattern_name} ({color_name})")
    
    def get_banner_data(self):
        return self.banner_data