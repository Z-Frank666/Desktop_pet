import datetime
import os
import json
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TodoWidget(QDialog):
    """待办事项小组件，包含日历和待办管理功能"""

    def __init__(self, parent=None, data_file="todo_data.json"):
        super(TodoWidget, self).__init__(parent)
        self.data_file = data_file
        self.todo_data = self.load_todo_data()
        self.selected_date = datetime.date.today()
        self.init_ui()

    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("待办事项")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            TodoWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                border: 1px solid #1E3A8A;
            }
        """)
        self.resize(400, 450)

        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 标题栏
        title_bar = QWidget(self)
        title_bar.setMinimumHeight(36)
        title_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #1E3A8A, stop:1 #3B82F6);
                border-radius: 12px 12px 0 0;
                background-image: url("source/frost_pattern.png");
                background-repeat: no-repeat;
                background-position: right center;
                background-size: 40px;
            }
        """)

        title_label = QLabel("待办事项", title_bar)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font: bold 12pt '华文中宋';
                padding-left: 12px;
            }
        """)

        close_btn = QPushButton("×", title_bar)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FFFFFF;
                font: bold 14pt;
                border: none;
                padding: 0 10px;
            }
            QPushButton:hover {
                color: #E5E7EB;
            }
            QPushButton:pressed {
                color: #9CA3AF;
            }
        """)
        close_btn.clicked.connect(self.close)

        title_layout = QHBoxLayout(title_bar)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # 日历组件
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("""
            QCalendarWidget QAbstractItemView {
                background-color: white;
                alternate-background-color: #F3F4F6;
                selection-background-color: #3B82F6;
                selection-color: white;
                color: #1F2937;
                border: 1px solid #E5E7EB;
                border-radius: 0 0 12px 12px;
                padding: 8px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #3B82F6;
                border: 1px solid #1E3A8A;
                border-radius: 0;
            }
            QCalendarWidget QToolButton {
                background-color: transparent;
                color: white;
                font: 11pt '华文中宋';
                border: none;
                padding: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: rgba(96, 165, 250, 0.5);
            }
            QCalendarWidget QLabel {
                color: white;
                font: 11pt '华文中宋';
            }
        """)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.clicked.connect(self.date_selected)

        # 待办事项列表 - 改为支持复选框
        self.todo_list = QListWidget(self)
        self.todo_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #1E3A8A;
                font: 11pt '华文中宋';
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget::item {
                border-bottom: 1px solid #E5E7EB;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #DBEAFE;
                color: #1E3A8A;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                image: url(:/icons/check-box.svg);
            }
            QCheckBox::indicator:unchecked {
                image: url(:/icons/check-box-outline-blank.svg);
            }
        """)
        self.todo_list.itemChanged.connect(self.todo_status_changed)

        # 待办操作按钮
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("添加", self)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font: 11pt '华文中宋';
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        add_btn.clicked.connect(self.add_todo)

        delete_btn = QPushButton("删除", self)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                font: 11pt '华文中宋';
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:pressed {
                background-color: #B91C1C;
            }
        """)
        delete_btn.clicked.connect(self.delete_todo)

        edit_btn = QPushButton("编辑", self)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                font: 11pt '华文中宋';
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
            QPushButton:pressed {
                background-color: #B45309;
            }
        """)
        edit_btn.clicked.connect(self.edit_todo)

        # 添加标记完成按钮
        complete_btn = QPushButton("修改状态", self)
        complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                font: 11pt '华文中宋';
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        complete_btn.clicked.connect(self.mark_todo_complete)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(complete_btn)
        btn_layout.setSpacing(8)

        # 整合所有组件
        main_layout.addWidget(title_bar)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(QLabel("当前日期待办事项:", self))
        main_layout.addWidget(self.todo_list)
        main_layout.addLayout(btn_layout)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 初始化显示当前日期待办
        self.update_todo_list()

    def load_todo_data(self):
        """加载待办数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading todo data: {e}")
            return {}

    def save_todo_data(self):
        """保存待办数据"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.todo_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving todo data: {e}")
            QMessageBox.warning(self, "保存失败", f"无法保存待办数据: {e}")

    def date_selected(self, date):
        """日期选择事件处理"""
        self.selected_date = date.toPyDate()
        self.update_todo_list()

    def update_todo_list(self):
        """更新待办事项列表"""
        self.todo_list.clear()
        date_str = self.selected_date.strftime("%Y-%m-%d")

        if date_str in self.todo_data:
            for todo in self.todo_data[date_str]:
                item = QListWidgetItem(todo['content'])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked if todo['completed'] else Qt.Unchecked)
                item.setData(Qt.UserRole, todo['id'])  # 存储ID用于后续操作
                self.todo_list.addItem(item)

    def add_todo(self):
        """添加待办事项"""
        try:
            # 创建输入对话框
            dialog = QInputDialog(self)
            dialog.setWindowTitle("添加待办")
            dialog.setLabelText("输入待办事项:")
            dialog.setTextValue(f"待办事项 {self.todo_list.count() + 1}")
            dialog.setOkButtonText("确定")
            dialog.setCancelButtonText("取消")
            dialog.setInputMode(QInputDialog.TextInput)

            # 显示对话框并获取结果
            if dialog.exec_():
                text = dialog.textValue()
                if text:
                    date_str = self.selected_date.strftime("%Y-%m-%d")

                    if date_str not in self.todo_data:
                        self.todo_data[date_str] = []

                    # 生成唯一ID
                    todo_id = f"{date_str}-{len(self.todo_data[date_str]) + 1}"

                    # 创建新待办项
                    new_todo = {
                        'id': todo_id,
                        'content': text,
                        'completed': False,
                        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'updated_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    self.todo_data[date_str].append(new_todo)
                    self.update_todo_list()
                    self.save_todo_data()
                    QMessageBox.information(self, "成功", "待办事项已添加")
                else:
                    QMessageBox.warning(self, "提示", "待办事项不能为空")
        except Exception as e:
            print(f"Error in add_todo: {e}")
            QMessageBox.critical(self, "错误", f"添加待办事项时出错: {str(e)}")

    def delete_todo(self):
        """删除选中的待办事项"""
        current_item = self.todo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择要删除的待办事项")
            return

        date_str = self.selected_date.strftime("%Y-%m-%d")
        todo_id = current_item.data(Qt.UserRole)

        # 找到并删除对应的待办
        for i, todo in enumerate(self.todo_data.get(date_str, [])):
            if todo['id'] == todo_id:
                del self.todo_data[date_str][i]
                break

        self.update_todo_list()
        self.save_todo_data()
        QMessageBox.information(self, "成功", "待办事项已删除")

    def edit_todo(self):
        """编辑选中的待办事项"""
        current_item = self.todo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择要编辑的待办事项")
            return

        date_str = self.selected_date.strftime("%Y-%m-%d")
        todo_id = current_item.data(Qt.UserRole)

        # 找到对应的待办
        for todo in self.todo_data.get(date_str, []):
            if todo['id'] == todo_id:
                text, ok = QInputDialog.getText(
                    self, "编辑待办", "修改待办事项:",
                    text=todo['content']
                )

                if ok and text:
                    todo['content'] = text
                    todo['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.update_todo_list()
                    self.save_todo_data()
                    QMessageBox.information(self, "成功", "待办事项已更新")
                return

    def mark_todo_complete(self):
        """标记选中的待办事项为完成/未完成"""
        current_item = self.todo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择要标记的待办事项")
            return

        date_str = self.selected_date.strftime("%Y-%m-%d")
        todo_id = current_item.data(Qt.UserRole)

        # 找到对应的待办并切换完成状态
        for todo in self.todo_data.get(date_str, []):
            if todo['id'] == todo_id:
                todo['completed'] = not todo['completed']
                todo['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_todo_list()
                self.save_todo_data()
                status = "已完成" if todo['completed'] else "未完成"
                QMessageBox.information(self, "成功", f"待办事项状态已更新为: {status}")
                return

    def todo_status_changed(self, item):
        """待办事项状态改变事件处理"""
        date_str = self.selected_date.strftime("%Y-%m-%d")
        todo_id = item.data(Qt.UserRole)

        # 找到对应的待办并更新状态
        for todo in self.todo_data.get(date_str, []):
            if todo['id'] == todo_id:
                todo['completed'] = item.checkState() == Qt.Checked
                todo['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todo_data()
                break


# 示例使用代码
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # 创建待办组件实例
    todo_widget = TodoWidget(data_file="./source/todo.json")
    todo_widget.show()

    sys.exit(app.exec_())