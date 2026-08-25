import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import re

class WrittenBookGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.pages = []  # 存储所有页面
        self.current_page = 0  # 当前编辑的页面
        self.generate_written_book_var = tk.BooleanVar(value=False)  # 生成成书组件开关

        # 颜色映射
        self.color_map = {
            "黑色": "black",
            "深蓝色": "dark_blue",
            "深绿色": "dark_green",
            "深青色": "dark_aqua",
            "深红色": "dark_red",
            "深紫色": "dark_purple",
            "金色": "gold",
            "灰色": "gray",
            "深灰色": "dark_gray",
            "蓝色": "blue",
            "绿色": "green",
            "青色": "aqua",
            "红色": "red",
            "浅紫色": "light_purple",
            "黄色": "yellow",
            "白色": "white"
        }

        # 鼠标动作类型
        self.click_actions = {
            "无": "none",
            "打开链接": "open_url",
            "运行命令": "run_command",
            "建议命令": "suggest_command",
            "改变页面": "change_page",
            "复制到剪贴板": "copy_to_clipboard"
        }

        self.hover_actions = {
            "无": "none",
            "显示文本": "show_text",
            "显示物品": "show_item",
            "显示实体": "show_entity"
        }

        # 文本样式
        self.text_styles = {
            "正常": "normal",
            "粗体": "bold",
            "斜体": "italic",
            "下划线": "underlined",
            "删除线": "strikethrough",
            "随机": "obfuscated"
        }

        self.create_written_book_tab()

        # 初始化第一页
        self.add_new_page()

    def create_written_book_tab(self):
        # 配置父容器（滚动框架）使其能够扩展
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        # 生成成书组件开关
        self.create_generate_switch_section()

        # 页面管理区域
        self.create_page_management_section()

        # 内容编辑区域
        self.create_content_editing_section()

        # 输出预览区域
        self.create_output_preview_section()

    def create_generate_switch_section(self):
        """创建生成成书组件开关"""
        switch_frame = ttk.LabelFrame(self.parent, text="组件设置", padding="5")
        switch_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=8, pady=3)

        generate_checkbutton = ttk.Checkbutton(switch_frame, text="生成成书组件",
                                              variable=self.generate_written_book_var)
        generate_checkbutton.pack(side=tk.LEFT, padx=3)

        help_label = ttk.Label(switch_frame, text="勾选此项将在生成的give命令中包含成书组件",
                              font=('SimHei', 7), foreground="#666666")
        help_label.pack(side=tk.LEFT, padx=5)

        switch_frame.columnconfigure(0, weight=1)

    def create_page_management_section(self):
        page_frame = ttk.LabelFrame(self.parent, text="页面管理", padding="6")
        page_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=8, pady=3)

        # 当前页面选择
        ttk.Label(page_frame, text="当前页面:", font=('SimHei', 8)).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.page_var = tk.StringVar()
        self.page_combo = ttk.Combobox(page_frame, textvariable=self.page_var, width=12, state="readonly")
        self.page_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=3)
        self.page_combo.bind('<<ComboboxSelected>>', self.on_page_selected)

        # 按钮
        button_frame = ttk.Frame(page_frame)
        button_frame.grid(row=0, column=2, sticky=tk.W, pady=2, padx=5)

        ttk.Button(button_frame, text="添加", command=self.add_new_page, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_frame, text="删除", command=self.delete_current_page, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_frame, text="上移", command=self.move_page_up, width=4).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_frame, text="下移", command=self.move_page_down, width=4).pack(side=tk.LEFT, padx=1)

        # 页面标题
        ttk.Label(page_frame, text="页面标题:", font=('SimHei', 8)).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.page_title_var = tk.StringVar()
        self.page_title_entry = ttk.Entry(page_frame, textvariable=self.page_title_var, width=40)
        self.page_title_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2, padx=3)
        self.page_title_entry.bind('<KeyRelease>', self.on_page_title_changed)

        # 页面编辑提示标签（新增）
        self.page_hint_label = ttk.Label(page_frame, text="", font=('SimHei', 7), foreground="#666666")
        self.page_hint_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=2)

        page_frame.columnconfigure(1, weight=1)

    def create_content_editing_section(self):
        content_frame = ttk.LabelFrame(self.parent, text="内容编辑", padding="6")
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=8, pady=3)

        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        paragraph_frame = ttk.LabelFrame(content_frame, text="段落管理", padding="3")
        paragraph_frame.pack(fill="x", pady=3)

        button_container = ttk.Frame(paragraph_frame)
        button_container.pack(fill=tk.X)

        ttk.Button(button_container, text="段落", command=self.add_paragraph, width=6).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(button_container, text="选择器", command=self.add_selector, width=6).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(button_container, text="记分板", command=self.add_scoreboard, width=6).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(button_container, text="热键", command=self.add_keybind, width=6).pack(side=tk.LEFT, padx=2, pady=2)

        help_label = ttk.Label(paragraph_frame, text="点击段落列表中的'编辑'按钮来详细配置每个段落",
                              font=('SimHei', 7), foreground="#666666")
        help_label.pack(side=tk.BOTTOM, anchor=tk.W, pady=1)

        self.paragraph_list_frame = ttk.Frame(content_frame)
        self.paragraph_list_frame.pack(fill="x", pady=3)

    def create_output_preview_section(self):
        output_frame = ttk.LabelFrame(self.parent, text="输出预览", padding="6")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=8, pady=3)

        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.preview_text = tk.Text(output_frame, height=6, width=80, font=('Courier New', 8))
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=3)

        ttk.Button(output_frame, text="更新预览", command=self.update_preview, width=10).grid(row=1, column=0, pady=3)

        self.parent.rowconfigure(3, weight=1)

    # ---------- 页面管理方法 ----------
    def add_new_page(self):
        page_num = len(self.pages) + 1
        page_data = {
            "title": f"第{page_num}页",
            "paragraphs": []
        }
        self.pages.append(page_data)
        self.update_page_combo()
        self.page_combo.set(f"第{page_num}页")
        self.current_page = len(self.pages) - 1
        self.update_page_editor()
        self.update_preview()  # 自动更新预览

    def delete_current_page(self):
        if len(self.pages) <= 1:
            messagebox.showwarning("警告", "至少需要保留一个页面")
            return

        if messagebox.askyesno("确认", f"确定要删除{self.pages[self.current_page]['title']}吗？"):
            self.pages.pop(self.current_page)
            if self.current_page >= len(self.pages):
                self.current_page = len(self.pages) - 1
            self.update_page_combo()
            self.update_page_editor()
            self.update_preview()

    def move_page_up(self):
        if self.current_page > 0:
            self.pages[self.current_page], self.pages[self.current_page - 1] = \
                self.pages[self.current_page - 1], self.pages[self.current_page]
            self.current_page -= 1
            self.update_page_combo()
            self.update_page_editor()
            self.update_preview()

    def move_page_down(self):
        if self.current_page < len(self.pages) - 1:
            self.pages[self.current_page], self.pages[self.current_page + 1] = \
                self.pages[self.current_page + 1], self.pages[self.current_page]
            self.current_page += 1
            self.update_page_combo()
            self.update_page_editor()
            self.update_preview()

    def update_page_combo(self):
        page_names = [page["title"] for page in self.pages]
        self.page_combo['values'] = page_names
        if page_names:
            self.page_combo.set(page_names[self.current_page])

    def on_page_selected(self, event):
        selected_title = self.page_var.get()
        for i, page in enumerate(self.pages):
            if page["title"] == selected_title:
                self.current_page = i
                self.update_page_editor()
                break

    def on_page_title_changed(self, event):
        if 0 <= self.current_page < len(self.pages):
            self.pages[self.current_page]["title"] = self.page_title_var.get()
            self.update_page_combo()
            self.update_preview()

    def update_page_editor(self):
        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]
            self.page_title_var.set(page_data["title"])
            # 更新提示标签
            total = len(self.pages)
            self.page_hint_label.config(text=f"当前编辑：第{self.current_page+1}页，共{total}页")
            self.update_paragraph_list()
            self.update_preview()  # 页面切换时自动更新预览

    # ---------- 段落管理方法 ----------
    def add_paragraph(self):
        if 0 <= self.current_page < len(self.pages):
            paragraph_data = {
                "type": "text",
                "content": "",
                "color": "black",
                "style": "normal",
                "click_action": "none",
                "click_value": "",
                "hover_action": "none",
                "hover_value": ""
            }
            self.pages[self.current_page]["paragraphs"].append(paragraph_data)
            self.update_paragraph_list()
            self.update_preview()

    def add_selector(self):
        if 0 <= self.current_page < len(self.pages):
            paragraph_data = {
                "type": "selector",
                "selector": "@p",
                "color": "white",
                "style": "normal",
                "click_action": "none",
                "click_value": "",
                "hover_action": "none",
                "hover_value": ""
            }
            self.pages[self.current_page]["paragraphs"].append(paragraph_data)
            self.update_paragraph_list()
            self.update_preview()

    def add_scoreboard(self):
        if 0 <= self.current_page < len(self.pages):
            paragraph_data = {
                "type": "scoreboard",
                "objective": "score",
                "target": "@p",
                "color": "white",
                "style": "normal",
                "click_action": "none",
                "click_value": "",
                "hover_action": "none",
                "hover_value": ""
            }
            self.pages[self.current_page]["paragraphs"].append(paragraph_data)
            self.update_paragraph_list()
            self.update_preview()

    def add_keybind(self):
        if 0 <= self.current_page < len(self.pages):
            paragraph_data = {
                "type": "keybind",
                "key": "key.forward",
                "color": "white",
                "style": "normal",
                "click_action": "none",
                "click_value": "",
                "hover_action": "none",
                "hover_value": ""
            }
            self.pages[self.current_page]["paragraphs"].append(paragraph_data)
            self.update_paragraph_list()
            self.update_preview()

    def update_paragraph_list(self):
        for widget in self.paragraph_list_frame.winfo_children():
            widget.destroy()

        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]

            if not page_data["paragraphs"]:
                empty_label = ttk.Label(self.paragraph_list_frame, text="当前页面没有段落，点击上方按钮添加段落",
                                      font=('SimHei', 9), foreground="#999999")
                empty_label.pack(pady=20)
                return

            for i, paragraph in enumerate(page_data["paragraphs"]):
                paragraph_frame = ttk.Frame(self.paragraph_list_frame, relief="solid", borderwidth=1)
                paragraph_frame.pack(fill="x", pady=2, padx=5)

                info_frame = ttk.Frame(paragraph_frame)
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=3)

                type_label = ttk.Label(info_frame, text=f"段落 {i+1} - {self.get_paragraph_type_name(paragraph['type'])}",
                                     font=('SimHei', 9, 'bold'))
                type_label.pack(anchor=tk.W)

                preview_text = self.get_paragraph_preview(paragraph)
                preview_label = ttk.Label(info_frame, text=preview_text, font=('SimHei', 8),
                                        foreground="#666666")
                preview_label.pack(anchor=tk.W)

                button_frame = ttk.Frame(paragraph_frame)
                button_frame.pack(side=tk.RIGHT, padx=5, pady=3)

                up_button = ttk.Button(button_frame, text="↑", width=2,
                                     command=lambda idx=i: self.move_paragraph_up(idx))
                up_button.pack(side=tk.LEFT, padx=1)

                down_button = ttk.Button(button_frame, text="↓", width=2,
                                       command=lambda idx=i: self.move_paragraph_down(idx))
                down_button.pack(side=tk.LEFT, padx=1)

                edit_button = ttk.Button(button_frame, text="编辑",
                                       command=lambda idx=i: self.edit_paragraph(idx))
                edit_button.pack(side=tk.LEFT, padx=2)

                delete_button = ttk.Button(button_frame, text="删除",
                                         command=lambda idx=i: self.delete_paragraph(idx))
                delete_button.pack(side=tk.LEFT, padx=2)

    def get_paragraph_type_name(self, paragraph_type):
        type_names = {
            "text": "文本段落",
            "selector": "目标选择器",
            "scoreboard": "记分板数据",
            "keybind": "绑定热键"
        }
        return type_names.get(paragraph_type, paragraph_type)

    def get_paragraph_preview(self, paragraph):
        if paragraph["type"] == "text":
            content = paragraph.get("content", "")
            if len(content) > 30:
                return content[:30] + "..."
            return content if content else "[空文本]"
        elif paragraph["type"] == "selector":
            return f"选择器: {paragraph.get('selector', '@p')}"
        elif paragraph["type"] == "scoreboard":
            return f"记分板: {paragraph.get('target', '@p')} -> {paragraph.get('objective', 'score')}"
        elif paragraph["type"] == "keybind":
            return f"热键: {paragraph.get('key', 'key.forward')}"
        return "未知段落类型"

    def edit_paragraph(self, index):
        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]
            if 0 <= index < len(page_data["paragraphs"]):
                paragraph = page_data["paragraphs"][index]
                self.show_paragraph_editor(paragraph, index)

    def delete_paragraph(self, index):
        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]
            if 0 <= index < len(page_data["paragraphs"]):
                page_data["paragraphs"].pop(index)
                self.update_paragraph_list()
                self.update_preview()

    def move_paragraph_up(self, index):
        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]
            if index > 0 and index < len(page_data["paragraphs"]):
                page_data["paragraphs"][index], page_data["paragraphs"][index-1] = \
                    page_data["paragraphs"][index-1], page_data["paragraphs"][index]
                self.update_paragraph_list()
                self.update_preview()

    def move_paragraph_down(self, index):
        if 0 <= self.current_page < len(self.pages):
            page_data = self.pages[self.current_page]
            if index < len(page_data["paragraphs"]) - 1:
                page_data["paragraphs"][index], page_data["paragraphs"][index+1] = \
                    page_data["paragraphs"][index+1], page_data["paragraphs"][index]
                self.update_paragraph_list()
                self.update_preview()

    # ---------- 段落编辑对话框 ----------
    def show_paragraph_editor(self, paragraph, index):
        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"编辑段落 {index+1}")
        edit_window.geometry("600x400")
        edit_window.transient(self.parent)
        edit_window.grab_set()

        self.editing_paragraph_index = index
        self.create_paragraph_edit_interface(edit_window, paragraph)

        button_frame = ttk.Frame(edit_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="确定", command=lambda: self.save_paragraph_edit(edit_window)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.RIGHT, padx=5)

    def create_paragraph_edit_interface(self, parent, paragraph):
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=f"段落类型: {self.get_paragraph_type_name(paragraph['type'])}",
                  font=('SimHei', 10, 'bold')).pack(anchor=tk.W, pady=5)

        if paragraph["type"] == "text":
            self.create_text_paragraph_editor(main_frame, paragraph)
        elif paragraph["type"] == "selector":
            self.create_selector_paragraph_editor(main_frame, paragraph)
        elif paragraph["type"] == "scoreboard":
            self.create_scoreboard_paragraph_editor(main_frame, paragraph)
        elif paragraph["type"] == "keybind":
            self.create_keybind_paragraph_editor(main_frame, paragraph)

        self.create_common_style_editor(main_frame, paragraph)
        self.create_mouse_actions_editor(main_frame, paragraph)

    def create_text_paragraph_editor(self, parent, paragraph):
        text_frame = ttk.LabelFrame(parent, text="文本内容", padding="5")
        text_frame.pack(fill=tk.X, pady=5)

        ttk.Label(text_frame, text="文本内容:").pack(anchor=tk.W, pady=2)
        self.edit_text_content = tk.Text(text_frame, height=4, width=50)
        self.edit_text_content.pack(fill=tk.X, pady=5)
        self.edit_text_content.insert(1.0, paragraph.get("content", ""))

    def create_selector_paragraph_editor(self, parent, paragraph):
        selector_frame = ttk.LabelFrame(parent, text="目标选择器", padding="5")
        selector_frame.pack(fill=tk.X, pady=5)

        ttk.Label(selector_frame, text="选择器:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.edit_selector_var = tk.StringVar(value=paragraph.get("selector", "@p"))
        self.edit_selector_entry = ttk.Entry(selector_frame, textvariable=self.edit_selector_var, width=40)
        self.edit_selector_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        common_selectors_frame = ttk.Frame(selector_frame)
        common_selectors_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        common_selectors = [
            ("最近的玩家", "@p"),
            ("所有玩家", "@a"),
            ("随机玩家", "@r"),
            ("所有实体", "@e"),
            ("执行者", "@s")
        ]

        for text, selector in common_selectors:
            ttk.Button(common_selectors_frame, text=text,
                      command=lambda s=selector: self.edit_selector_var.set(s)).pack(side=tk.LEFT, padx=2)

        selector_frame.columnconfigure(1, weight=1)

    def create_scoreboard_paragraph_editor(self, parent, paragraph):
        score_frame = ttk.LabelFrame(parent, text="记分板数据", padding="5")
        score_frame.pack(fill=tk.X, pady=5)

        ttk.Label(score_frame, text="目标:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.edit_score_target_var = tk.StringVar(value=paragraph.get("target", "@p"))
        self.edit_score_target_entry = ttk.Entry(score_frame, textvariable=self.edit_score_target_var, width=30)
        self.edit_score_target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        ttk.Label(score_frame, text="记分项:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edit_score_objective_var = tk.StringVar(value=paragraph.get("objective", "score"))
        self.edit_score_objective_entry = ttk.Entry(score_frame, textvariable=self.edit_score_objective_var, width=30)
        self.edit_score_objective_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        score_frame.columnconfigure(1, weight=1)

    def create_keybind_paragraph_editor(self, parent, paragraph):
        keybind_frame = ttk.LabelFrame(parent, text="绑定热键", padding="5")
        keybind_frame.pack(fill=tk.X, pady=5)

        ttk.Label(keybind_frame, text="热键ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.edit_keybind_var = tk.StringVar(value=paragraph.get("key", "key.forward"))
        self.edit_keybind_entry = ttk.Entry(keybind_frame, textvariable=self.edit_keybind_var, width=40)
        self.edit_keybind_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        common_keys_frame = ttk.Frame(keybind_frame)
        common_keys_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        common_keys = [
            ("前进", "key.forward"),
            ("后退", "key.back"),
            ("左移", "key.left"),
            ("右移", "key.right"),
            ("跳跃", "key.jump"),
            ("潜行", "key.sneak"),
            ("攻击", "key.attack"),
            ("使用", "key.use")
        ]

        for text, key in common_keys:
            ttk.Button(common_keys_frame, text=text,
                      command=lambda k=key: self.edit_keybind_var.set(k)).pack(side=tk.LEFT, padx=2)

        keybind_frame.columnconfigure(1, weight=1)

    def create_common_style_editor(self, parent, paragraph):
        style_frame = ttk.LabelFrame(parent, text="文本样式", padding="5")
        style_frame.pack(fill=tk.X, pady=5)

        ttk.Label(style_frame, text="颜色:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.edit_color_var = tk.StringVar(value=paragraph.get("color", "black"))
        self.edit_color_combo = ttk.Combobox(style_frame, textvariable=self.edit_color_var,
                                           values=list(self.color_map.keys()), width=12)
        self.edit_color_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)

        ttk.Label(style_frame, text="样式:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.edit_style_var = tk.StringVar(value=paragraph.get("style", "normal"))
        self.edit_style_combo = ttk.Combobox(style_frame, textvariable=self.edit_style_var,
                                           values=list(self.text_styles.keys()), width=12)
        self.edit_style_combo.grid(row=0, column=3, sticky=tk.W, pady=2, padx=5)

        style_frame.columnconfigure(1, weight=1)
        style_frame.columnconfigure(3, weight=1)

    def create_mouse_actions_editor(self, parent, paragraph):
        mouse_frame = ttk.LabelFrame(parent, text="鼠标动作", padding="5")
        mouse_frame.pack(fill=tk.X, pady=5)

        # 点击动作
        ttk.Label(mouse_frame, text="点击动作:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.edit_click_action_var = tk.StringVar(value=paragraph.get("click_action", "none"))
        self.edit_click_combo = ttk.Combobox(mouse_frame, textvariable=self.edit_click_action_var,
                                           values=list(self.click_actions.keys()), width=12)
        self.edit_click_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        self.edit_click_combo.bind('<<ComboboxSelected>>', self.on_edit_click_action_changed)

        ttk.Label(mouse_frame, text="参数:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.edit_click_param_var = tk.StringVar(value=paragraph.get("click_value", ""))
        self.edit_click_param_entry = ttk.Entry(mouse_frame, textvariable=self.edit_click_param_var, width=30)
        self.edit_click_param_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2, padx=5)

        # 悬停动作
        ttk.Label(mouse_frame, text="悬停动作:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edit_hover_action_var = tk.StringVar(value=paragraph.get("hover_action", "none"))
        self.edit_hover_combo = ttk.Combobox(mouse_frame, textvariable=self.edit_hover_action_var,
                                           values=list(self.hover_actions.keys()), width=12)
        self.edit_hover_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        self.edit_hover_combo.bind('<<ComboboxSelected>>', self.on_edit_hover_action_changed)

        ttk.Label(mouse_frame, text="参数:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.edit_hover_param_var = tk.StringVar(value=paragraph.get("hover_value", ""))
        self.edit_hover_param_entry = ttk.Entry(mouse_frame, textvariable=self.edit_hover_param_var, width=30)
        self.edit_hover_param_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=2, padx=5)

        mouse_frame.columnconfigure(3, weight=1)

        # 初始化参数框状态
        self.on_edit_click_action_changed()
        self.on_edit_hover_action_changed()

    def on_edit_click_action_changed(self, event=None):
        action = self.edit_click_action_var.get()
        hints = {
            "无": "",
            "打开链接": "请输入网址（例如 https://example.com）",
            "运行命令": "请输入命令（不含 /）",
            "建议命令": "请输入建议的命令",
            "改变页面": "请输入页码（从1开始）",
            "复制到剪贴板": "请输入要复制的文本"
        }
        if action == "无":
            self.edit_click_param_entry.config(state="disabled")
            self.edit_click_param_var.set("")
        else:
            self.edit_click_param_entry.config(state="normal")
            # 仅在参数为空时设置提示，避免覆盖用户输入
            if not self.edit_click_param_var.get():
                self.edit_click_param_var.set(hints.get(action, ""))

    def on_edit_hover_action_changed(self, event=None):
        action = self.edit_hover_action_var.get()
        hints = {
            "无": "",
            "显示文本": "请输入要显示的文本",
            "显示物品": "请输入物品ID（例如 minecraft:stone）",
            "显示实体": "请输入实体ID（例如 minecraft:creeper）"
        }
        if action == "无":
            self.edit_hover_param_entry.config(state="disabled")
            self.edit_hover_param_var.set("")
        else:
            self.edit_hover_param_entry.config(state="normal")
            if not self.edit_hover_param_var.get():
                self.edit_hover_param_var.set(hints.get(action, ""))

    def save_paragraph_edit(self, edit_window):
        if 0 <= self.current_page < len(self.pages) and hasattr(self, 'editing_paragraph_index'):
            page_data = self.pages[self.current_page]
            index = self.editing_paragraph_index

            if 0 <= index < len(page_data["paragraphs"]):
                paragraph = page_data["paragraphs"][index]

                if paragraph["type"] == "text":
                    paragraph["content"] = self.edit_text_content.get(1.0, tk.END).strip()
                elif paragraph["type"] == "selector":
                    paragraph["selector"] = self.edit_selector_var.get()
                elif paragraph["type"] == "scoreboard":
                    paragraph["target"] = self.edit_score_target_var.get()
                    paragraph["objective"] = self.edit_score_objective_var.get()
                elif paragraph["type"] == "keybind":
                    paragraph["key"] = self.edit_keybind_var.get()

                paragraph["color"] = self.color_map.get(self.edit_color_var.get(), "black")
                paragraph["style"] = self.text_styles.get(self.edit_style_var.get(), "normal")
                paragraph["click_action"] = self.click_actions.get(self.edit_click_action_var.get(), "none")
                paragraph["click_value"] = self.edit_click_param_var.get()
                paragraph["hover_action"] = self.hover_actions.get(self.edit_hover_action_var.get(), "none")
                paragraph["hover_value"] = self.edit_hover_param_var.get()

                self.update_paragraph_list()
                self.update_preview()
                edit_window.destroy()

    # ---------- 预览与数据生成 ----------
    def update_preview(self):
        try:
            book_data = self.generate_book_data()
            preview_text = json.dumps(book_data, ensure_ascii=False, indent=2)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
        except Exception as e:
            # 预览更新失败不阻塞操作
            print(f"预览更新失败: {e}")

    def generate_book_data(self):
        book_data = {"pages": []}
        for page in self.pages:
            page_components = []
            for paragraph in page["paragraphs"]:
                component = self.generate_component(paragraph)
                if component:
                    page_components.append(component)

            if page_components:
                # 如果只有一个组件，直接使用该组件；否则使用数组
                if len(page_components) == 1:
                    page_json = json.dumps(page_components[0], ensure_ascii=False)
                else:
                    page_json = json.dumps(page_components, ensure_ascii=False)
                book_data["pages"].append(page_json)

        return book_data

    def generate_component(self, paragraph):
        component = {}

        ptype = paragraph.get("type", "text")
        if ptype == "text":
            component["text"] = paragraph.get("content", "")
        elif ptype == "selector":
            component["selector"] = paragraph.get("selector", "@p")
        elif ptype == "scoreboard":
            component["score"] = {
                "name": paragraph.get("target", "@p"),
                "objective": paragraph.get("objective", "score")
            }
        elif ptype == "keybind":
            component["keybind"] = paragraph.get("key", "key.forward")

        color = paragraph.get("color", "black")
        if color and color != "black":
            component["color"] = color

        style = paragraph.get("style", "normal")
        if style and style != "normal":
            component["style"] = style

        click_action = paragraph.get("click_action", "none")
        if click_action != "none":
            component["clickEvent"] = {
                "action": click_action,
                "value": paragraph.get("click_value", "")
            }

        hover_action = paragraph.get("hover_action", "none")
        if hover_action != "none":
            component["hoverEvent"] = {
                "action": hover_action,
                "value": paragraph.get("hover_value", "")
            }

        return component

    def get_component_data(self):
        return self.generate_book_data()

    def generate_written_book_component(self):
        if not self.generate_written_book_var.get():
            return None

        try:
            book_data = self.generate_book_data()
            if not book_data.get("pages"):
                return None

            # 标题取第一页标题，作者暂固定为“作者”
            return {
                "pages": book_data["pages"],
                "title": self.pages[0]["title"] if self.pages else "自定义成书",
                "author": "作者",
                "generation": 0
            }
        except Exception as e:
            print(f"生成成书组件时出错: {e}")
            return None