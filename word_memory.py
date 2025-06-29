import sys
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
import tkinter.font as font


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title('考研词汇记忆助手')
        self.root.geometry('750x750')
        self.root.configure(bg="#f5f5f5")  # 设置背景色

        # 确保中文显示正常
        self.font_config()

        # 加载词库
        self.vocab_path = Path('source/考研词汇5500-乱序版+国家名称.txt')
        self.word_list = self.load_vocabulary()
        self.current_word = None
        self.current_mode = "english_to_chinese"

        # 创建UI
        self.create_widgets()  # 先创建所有UI组件

        # 初始显示
        self.update_mode_display()
        self.show_next_word()  # 然后显示第一个单词

    def font_config(self):
        """配置字体，确保中文显示正常"""
        try:
            default_font = font.nametofont("TkDefaultFont")
            default_font.configure(family="微软雅黑", size=12)
            self.root.option_add("*Font", default_font)
        except Exception as e:
            print(f"字体配置失败: {e}")
            self.root.option_add("*Font", "SimHei 12")

    def create_widgets(self):
        """创建界面组件"""
        # 顶部标题
        title_frame = tk.Frame(self.root, bg="#4a7abc", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="考研词汇记忆助手",
                               font=("微软雅黑", 20, "bold"), bg="#4a7abc", fg="white")
        title_label.pack(pady=15)

        # 模式选择
        mode_frame = tk.Frame(self.root, bg="#f5f5f5")
        mode_frame.pack(pady=20)

        self.mode_var = tk.StringVar(value="english_to_chinese")

        # 使用ttk按钮获得更好的外观
        ttk.Radiobutton(mode_frame, text="看英文识中文", variable=self.mode_var,
                        value="english_to_chinese", command=self.change_mode).pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(mode_frame, text="看中文拼英文", variable=self.mode_var,
                        value="chinese_to_english", command=self.change_mode).pack(side=tk.LEFT, padx=20)

        # 结果反馈
        self.result_label = tk.Label(self.root, text='', font=('微软雅黑', 16), fg='green', bg="#f5f5f5")
        self.result_label.pack(pady=10)

        # 单词/释义显示区域
        self.display_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RAISED, bd=2)
        self.display_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)

        # 英文单词
        self.word_label = tk.Label(self.display_frame, text='点击"下一个单词"开始学习',
                                   font=('微软雅黑', 28), wraplength=650, bg="#ffffff")
        self.word_label.pack(pady=30)

        # 中文释义
        self.meaning_label = tk.Label(self.display_frame, text='',
                                      font=('微软雅黑', 18), wraplength=650, bg="#f0f8ff",
                                      relief=tk.SUNKEN, padx=10, pady=10)
        self.meaning_label.pack(pady=20, padx=20)

        # 输入框 (用于拼写英文)
        self.input_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.input_frame.pack(pady=10, fill=tk.X)

        self.answer_entry = ttk.Entry(self.input_frame, font=('微软雅黑', 16), width=30)
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)

        # 按钮区域
        self.btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.btn_frame.pack(pady=20)

        # 使用ttk按钮获得更好的外观
        self.next_btn = ttk.Button(self.btn_frame, text='下一个单词', command=self.show_next_word)
        self.show_meaning_btn = ttk.Button(self.btn_frame, text='显示中文', command=self.show_meaning)
        self.check_btn = ttk.Button(self.btn_frame, text='检查答案', command=self.check_answer)

        # 底部状态栏
        status_frame = tk.Frame(self.root, bg="#e0e0e0", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_label = tk.Label(status_frame, text="单词总数: " + str(len(self.word_list)),
                                font=("微软雅黑", 10), bg="#e0e0e0")
        status_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def load_vocabulary(self):
        """加载词库文件，返回[ (单词, 释义) ]列表"""
        try:
            with open(self.vocab_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            # 分割单词和释义（假设格式为"单词 释义"）
            word_pairs = []
            for line in lines:
                if ' ' in line:
                    word, meaning = line.split(' ', 1)
                    word_pairs.append((word.strip(), meaning.strip()))
            return word_pairs

        except FileNotFoundError:
            messagebox.showerror('错误', '未找到词库文件：source/考研词汇5500-乱序版+国家名称.txt')
            sys.exit(1)
        except Exception as e:
            messagebox.showerror('错误', f'词库解析失败：{str(e)}')
            sys.exit(1)

    def change_mode(self):
        """切换学习模式"""
        self.current_mode = self.mode_var.get()
        self.update_mode_display()
        self.show_next_word()

    def update_mode_display(self):
        """更新模式显示"""
        # 隐藏所有按钮
        self.next_btn.pack_forget()
        self.show_meaning_btn.pack_forget()
        self.check_btn.pack_forget()

        if self.current_mode == "english_to_chinese":
            self.word_label.config(text='点击"下一个单词"开始学习', fg='black')
            self.meaning_label.config(text='')
            self.answer_entry.pack_forget()
            self.next_btn.pack(side=tk.LEFT, padx=10)
            self.show_meaning_btn.pack(side=tk.LEFT, padx=10)
        else:
            self.word_label.config(text='点击"下一个单词"开始学习', fg='black')
            self.meaning_label.config(text='')
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.pack(pady=10)
            self.check_btn.pack(side=tk.LEFT, padx=10)
            self.next_btn.pack(side=tk.LEFT, padx=10)

    def show_next_word(self):
        """显示下一个随机单词"""
        if self.word_list:
            self.current_word = random.choice(self.word_list)
            self.result_label.config(text='')

            # 隐藏单词和释义
            self.word_label.config(fg='#f5f5f5')
            self.meaning_label.config(fg='#f5f5f5')

            if self.current_mode == "english_to_chinese":
                self.word_label.config(text=self.current_word[0], fg='#f5f5f5')
                self.meaning_label.config(text='')
                self.next_btn.pack(side=tk.LEFT, padx=10)
                self.show_meaning_btn.pack(side=tk.LEFT, padx=10)
                self.check_btn.pack_forget()
            else:
                # 看中文拼英文模式
                self.meaning_label.config(text=self.current_word[1], fg='#f5f5f5')
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()  # 自动聚焦到输入框

                # 保存完整单词和提示单词
                self.full_word = self.current_word[0]

                # 显示部分字母作为提示
                word = self.current_word[0]
                if len(word) > 3:
                    # 显示首尾字母，中间留几个空格
                    hint_positions = [0, len(word) - 1]  # 始终显示首尾字母
                    # 随机选择1-2个中间位置显示
                    if len(word) > 5:
                        hint_positions.extend(random.sample(range(1, len(word) - 1), min(2, len(word) - 3)))

                    hint = ''.join([word[i] if i in hint_positions else '_' for i in range(len(word))])
                    self.word_label.config(text=hint, fg='#f5f5f5')
                else:
                    # 短单词只隐藏中间一个字母
                    hint = word[0] + '_' * (len(word) - 2) + word[-1] if len(word) > 1 else word
                    self.word_label.config(text=hint, fg='#f5f5f5')

                self.check_btn.pack(side=tk.LEFT, padx=10)
                self.next_btn.pack(side=tk.LEFT, padx=10)
                self.show_meaning_btn.pack_forget()

            # 执行淡入动画
            self.fade_in(self.word_label)
            self.fade_in(self.meaning_label, delay=500)
        else:
            messagebox.showinfo('提示', '词库已全部学习完成！')

    def fade_in(self, widget, step=0, delay=0):
        """替代的淡入动画效果"""
        colors = ['#d0d0d0', '#a0a0a0', '#707070', '#404040', '#101010']
        if step < len(colors):
            widget.configure(fg=colors[step])
            widget.after(100 + delay, lambda: self.fade_in(widget, step + 1, delay))
        else:
            # 恢复正常颜色
            if widget == self.word_label:
                widget.configure(fg='#2c3e50')
            else:
                widget.configure(fg='black')

    def show_meaning(self):
        """显示中文释义（看英文识中文模式）"""
        if self.current_word and self.current_mode == "english_to_chinese":
            self.meaning_label.config(text=self.current_word[1])
            self.fade_in(self.meaning_label)

    def check_answer(self, event=None):
        """检查答案"""
        if not self.current_word or self.current_mode != "chinese_to_english":
            return

        # 禁用检查按钮，防止重复点击
        self.check_btn.config(state=tk.DISABLED)

        # 检查英文拼写
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_word[0].lower()

        if user_answer == correct_answer:
            self.result_label.config(text='✅ 正确！', fg='#27ae60')
        else:
            self.result_label.config(text=f'❌ 错误！正确答案是: {self.current_word[0]}', fg='#e74c3c')

        # 显示完整的英文单词
        self.word_label.config(text=self.full_word)
        self.fade_in(self.word_label)

        # 添加闪烁动画效果
        self.result_label.config(bg="#ffffff")
        self.result_label.after(100, lambda: self.result_label.config(bg="#f5f5f5"))
        self.result_label.after(200, lambda: self.result_label.config(bg="#ffffff"))
        self.result_label.after(300, lambda: self.result_label.config(bg="#f5f5f5"))

        # 启用检查按钮
        self.check_btn.config(state=tk.NORMAL)

    def reset_after_check(self):
        """检查答案后重置状态"""
        self.check_btn.config(state=tk.NORMAL)
        self.show_next_word()


if __name__ == '__main__':
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()