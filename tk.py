import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataLabelingApp:
    def __init__(self, root, csv_file):
        self.root = root
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)

        # Add 'is_selected' column if it doesn't exist
        if 'is_selected' not in self.df.columns:
            self.df['is_selected'] = 0
            self.df.to_csv(self.csv_file, index=False)

        self.current_index = 0
        self.categories = ['政治', '经济', '文化', '环保', '社会', '个人', '技术发展', '无关']
        self.positions = ['左倾', '右倾', '中立']

        # Set global font
        self.root.option_add("*Font", "DengXian 14")

        # GUI setup
        self.root.title("数据标注工具")
        self.root.state('zoomed')  # Maximize the window by default

        # Apply modern style
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for a modern look

        # Add background image
        self.background_image = tk.PhotoImage(file="OIP-C.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 左侧: 显示content和api_response
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.content_label = ttk.Label(self.left_frame, text="Content:")
        self.content_label.grid(row=0, column=0, sticky="w")

        self.content_text_frame = ttk.Frame(self.left_frame)
        self.content_text_frame.grid(row=1, column=0)
        self.content_text_scrollbar = ttk.Scrollbar(self.content_text_frame, orient="vertical")
        self.content_text_scrollbar.pack(side="right", fill="y")
        self.content_text = tk.Text(self.content_text_frame, width=60, height=10, wrap="word",
                                    yscrollcommand=self.content_text_scrollbar.set)
        self.content_text.insert("1.0", self.df.loc[self.current_index, 'content'])
        self.content_text.config(state="disabled")
        self.content_text.pack(side="left", fill="both", expand=True)
        self.content_text_scrollbar.config(command=self.content_text.yview)

        self.api_response_label = ttk.Label(self.left_frame, text="API Response:")
        self.api_response_label.grid(row=2, column=0, sticky="w")

        self.api_response_text_frame = ttk.Frame(self.left_frame)
        self.api_response_text_frame.grid(row=3, column=0)
        self.api_response_text_scrollbar = ttk.Scrollbar(self.api_response_text_frame, orient="vertical")
        self.api_response_text_scrollbar.pack(side="right", fill="y")
        self.api_response_text = tk.Text(self.api_response_text_frame, width=60, height=10, wrap="word",
                                         yscrollcommand=self.api_response_text_scrollbar.set)
        self.api_response_text.insert("1.0", self.df.loc[self.current_index, 'api_response'])
        self.api_response_text.config(state="disabled")
        self.api_response_text.pack(side="left", fill="both", expand=True)
        self.api_response_text_scrollbar.config(command=self.api_response_text.yview)

        self.api_response_lor_label = ttk.Label(self.left_frame, text="API Response LOR:")
        self.api_response_lor_label.grid(row=4, column=0, sticky="w")

        self.api_response_lor_text_frame = ttk.Frame(self.left_frame)
        self.api_response_lor_text_frame.grid(row=5, column=0)
        self.api_response_lor_text_scrollbar = ttk.Scrollbar(self.api_response_lor_text_frame, orient="vertical")
        self.api_response_lor_text_scrollbar.pack(side="right", fill="y")
        self.api_response_lor_text = tk.Text(self.api_response_lor_text_frame, width=60, height=10, wrap="word",
                                             yscrollcommand=self.api_response_lor_text_scrollbar.set)
        self.api_response_lor_text.insert("1.0", self.df.loc[self.current_index, 'api_response_lor'])
        self.api_response_lor_text.config(state="disabled")
        self.api_response_lor_text.pack(side="left", fill="both", expand=True)
        self.api_response_lor_text_scrollbar.config(command=self.api_response_lor_text.yview)

        # 右侧: 输入框，标注类别和立场
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        self.category_label = ttk.Label(self.right_frame, text="类别:")
        self.category_label.pack(anchor="w", pady=5)
        self.category_listbox = tk.Listbox(self.right_frame, selectmode=tk.MULTIPLE, width=30, height=10)
        self.category_listbox.pack(anchor="w", pady=5)
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

        self.position_label = ttk.Label(self.right_frame, text="立场:")
        self.position_label.pack(anchor="w", pady=5)
        self.position_var = tk.StringVar()
        for position in self.positions:
            rb = ttk.Radiobutton(self.right_frame, text=position, variable=self.position_var, value=position)
            rb.pack(anchor="w", pady=5)

        # Add checkbox for is_selected
        self.is_selected_var = tk.IntVar()
        self.is_selected_checkbox = ttk.Checkbutton(self.right_frame, text="选中", variable=self.is_selected_var , onvalue=1, offvalue=0)
        self.is_selected_checkbox.pack(anchor="w", pady=5)

        # 导航: 显示当前记录条数
        self.navigation_frame = ttk.Frame(self.root)
        self.navigation_frame.pack(side=tk.BOTTOM, pady=20)

        self.navigation_label = ttk.Label(self.navigation_frame, text=f"记录: {self.current_index + 1}/{len(self.df)}")
        self.navigation_label.pack(side=tk.LEFT)

        self.previous_button = ttk.Button(self.navigation_frame, text="上一条", command=self.previous_record, width=5)
        self.previous_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.navigation_frame, text="下一条", command=self.next_record, width=5)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # 跳转到指定记录
        self.jump_label = ttk.Label(self.navigation_frame, text="跳转:")
        self.jump_label.pack(side=tk.LEFT, padx=5)
        self.jump_entry = ttk.Entry(self.navigation_frame, width=5)
        self.jump_entry.pack(side=tk.LEFT, padx=5)
        self.jump_button = ttk.Button(self.navigation_frame, text="跳转", command=self.jump_to_record)
        self.jump_button.pack(side=tk.LEFT, padx=5)

        # 设置快捷键
        self.root.bind("<Left>", lambda event: self.previous_record())
        self.root.bind("<Right>", lambda event: self.next_record())
        self.root.bind("<Return>", lambda event: self.next_record())
        self.root.bind("<Control-s>", lambda event: self.save_record())

        # 按钮: 保存并更新数据
        self.save_button = ttk.Button(self.right_frame, text="保存", command=self.save_record)
        self.save_button.pack(pady=10)
        self.update_display()

    def update_display(self):
        """更新GUI显示内容并自动保存"""
        self.content_text.config(state="normal")
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", self.df.loc[self.current_index, 'content'])
        self.content_text.config(state="disabled")

        self.api_response_text.config(state="normal")
        self.api_response_text.delete("1.0", tk.END)
        self.api_response_text.insert("1.0", self.df.loc[self.current_index, 'api_response'])
        self.api_response_text.config(state="disabled")

        self.api_response_lor_text.config(state="normal")
        self.api_response_lor_text.delete("1.0", tk.END)
        self.api_response_lor_text.insert("1.0", self.df.loc[self.current_index, 'api_response_lor'])
        self.api_response_lor_text.config(state="disabled")

        # Update category listbox
        try:
            selected_categories = eval(self.df.loc[self.current_index, 'category'])
        except:
            selected_categories = ['无关']

        self.category_listbox.selection_clear(0, tk.END)
        for category in selected_categories:
            idx = self.categories.index(category)
            self.category_listbox.selection_set(idx)

            # Update position radiobutton
        category_lor = self.df.loc[self.current_index, 'category_lor']
        if isinstance(category_lor, str):
            self.position_var.set(eval(category_lor))
        elif isinstance(category_lor, list) and category_lor:
            self.position_var.set(category_lor[0])
        else:
            self.position_var.set('')
        # Update is_selected checkbox
        self.is_selected_var.set(self.df.loc[self.current_index, 'is_selected'])

        self.navigation_label.config(text=f"记录: {self.current_index + 1}/{len(self.df)}")

    def save_record(self):
        """保存当前标注记录"""
        selected_categories = [self.categories[i] for i in self.category_listbox.curselection()]
        self.df.loc[self.current_index, 'category'] = str(selected_categories)
        self.df.loc[self.current_index, 'category_lor'] = [self.position_var.get()] if self.position_var.get() else None
        self.df.loc[self.current_index, 'is_selected'] = self.is_selected_var.get()
        self.df.to_csv(self.csv_file, index=False)

    def next_record(self):
        """跳转到下一条记录"""
        if self.current_index < len(self.df) - 1:
            self.save_record()
            self.current_index += 1
            self.update_display()

    def previous_record(self):
        """跳转到上一条记录"""
        if self.current_index > 0:
            self.save_record()
            self.current_index -= 1
            self.update_display()

    def jump_to_record(self):
        """跳转到指定记录"""
        try:
            index = int(self.jump_entry.get()) - 1
            if 0 <= index < len(self.df):
                self.save_record()
                self.current_index = index
                self.update_display()
        except ValueError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DataLabelingApp(root, "data.csv")
    root.mainloop()