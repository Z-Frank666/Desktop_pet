import datetime
import json
import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from todo_widget import TodoWidget


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initPall()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()

    # 窗体初始化
    def init(self):
        # 初始化
        # 设置窗口属性:窗口无标题栏且固定在最前面
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 重绘组件、刷新
        self.repaint()

    # 托盘化设置初始化
    def initPall(self):
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('source/tigerIcon.jpg')
        # 设置右键显示最小化的菜单项
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(icons))
        showing = QAction(u'显示', self, triggered=self.showwin)
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    # 宠物静态gif图加载
    def initPetImage(self):
        # 创建主容器布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 对话框定义 - 使用气泡样式
        self.talkLabel = QLabel(self)
        self.talkLabel.setWordWrap(True)  # 自动换行
        self.talkLabel.setAlignment(Qt.AlignCenter)
        self.updateBubbleStyle()  # 设置气泡样式

        # 定义显示图片部分
        self.image = QLabel(self)
        self.movie = QMovie("source/normal/image_1.gif")
        self.movie.setScaledSize(QSize(200, 200))
        self.image.setMovie(self.movie)
        self.movie.start()

        # 将控件添加到布局中
        main_layout.addWidget(self.talkLabel, alignment=Qt.AlignCenter | Qt.AlignTop)
        main_layout.addWidget(self.image, alignment=Qt.AlignCenter)

        self.resize(220, 300)  # 调整整体大小
        self.randomPosition()
        self.show()

        # 加载动画和对话
        self.pet1 = []
        for i in os.listdir("source/normal"):
            self.pet1.append("source/normal/" + i)

        self.dialog = []
        todo_msg = get_today_incomplete_todos(todo_file="./source/todo.json")

        # 读取目录下dialog文件
        try:
            with open("source/dialog.txt", "r", encoding="utf-8") as f:
                text = f.read()
                self.dialog = text.split("\n")
        except Exception as e:
            print(f"Error reading dialog.txt: {e}")
            self.dialog = ["无法加载对话"]
        if todo_msg:
            self.dialog.append(todo_msg)
        # for i in self.dialog:print(i)
        # print(len(self.dialog))

    # 更新气泡样式


    def updateBubbleStyle(self):
        # 优菈主题气泡样式（冰元素+贵族质感）
        bubble_style = """
        QLabel {
            /* 冰蓝渐变背景 */
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                       stop:0 #3B82F6, stop:1 #60A5FA);
            color: #FFFFFF;                      /* 白色文本 */
            font: 11pt '华文中宋';                /* 优雅字体 */
            border-radius: 16px;                  /* 更大圆角模拟冰棱弧度 */
            padding: 12px 18px;                   /* 增加内边距 */
            border: 2px solid #1E3A8A;            /* 劳伦斯家族蓝边框 */
            position: relative;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3); /* 深蓝阴影 */
            /* 动态悬停效果 */
            transition: all 0.3s ease;
        }

        QLabel:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(30, 58, 138, 0.5);
            background-opacity: 255;
        }

        QLabel::after {
            /* 冰蓝三角气泡尾 */
            content: "";
            position: absolute;
            bottom: -16px;
            left: 30%;
            margin-left: -10px;
            border-width: 16px 12px 0;
            border-style: solid;
            border-color: #60A5FA transparent transparent;
        }

        /* 贵族霜花纹饰（需在source目录放置frost_pattern.png） */
        QLabel {
            background-image: url("source/frost_pattern.png");
            background-repeat: no-repeat;
            background-position: top right;
            background-size: 60px;
        }
        """
        self.talkLabel.setStyleSheet(bubble_style)

    # 宠物正常待机动作
    def petNormalAction(self):
        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(3000)
        self.condition = 0

        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(3000)
        self.talk_condition = 0
        self.talk()

    # 随机动作切换
    def randomAct(self):
        if not self.condition:
            self.movie = QMovie(random.choice(self.pet1))
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
        else:
            self.movie = QMovie("./source/click/image.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
            self.condition = 0
            self.talk_condition = 0

    # 宠物对话框行为处理
    def talk(self):
        if not self.talk_condition:
            text = random.choice(self.dialog)
            self.talkLabel.setText(text)
        else:
            self.talkLabel.setText("别点我")
            self.talk_condition = 0

        # 优化气泡框大小自适应
        self.optimizeBubbleSize()
        # 确保对话框不会超出屏幕
        self.keepBubbleOnScreen()

    # 优化气泡框大小以适应文本内容
    def optimizeBubbleSize(self):
        # 设置最大宽度限制
        max_width = 350

        # 获取当前字体和文本
        font = self.talkLabel.font()
        text = self.talkLabel.text()

        # 计算文本在当前字体下的宽度和高度
        metrics = QFontMetrics(font)
        rect = metrics.boundingRect(0, 0, max_width, 16777215,
                                    Qt.TextWordWrap | Qt.AlignCenter, text)

        # 考虑内边距和边框
        padding = 24  # 左右各12px
        border = 2  # 左右各1px

        # 计算气泡框的最佳宽度
        text_width = rect.width()
        bubble_width = min(text_width + padding + border, max_width)

        # 设置气泡框的固定宽度并调整高度以适应文本
        self.talkLabel.setFixedWidth(bubble_width)
        self.talkLabel.adjustSize()

    # 确保气泡对话框不会超出屏幕
    def keepBubbleOnScreen(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()

        # 如果对话框超出屏幕右侧
        if pet_geo.right() > screen_geo.right():
            new_x = screen_geo.right() - pet_geo.width()
            self.move(new_x, pet_geo.y())

        # 如果对话框超出屏幕底部
        if pet_geo.bottom() > screen_geo.bottom():
            new_y = screen_geo.bottom() - pet_geo.height()
            self.move(pet_geo.x(), new_y)

    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()

    # 显示宠物
    def showwin(self):
        self.setWindowOpacity(1)

    # 宠物随机位置
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = int((screen_geo.width() - pet_geo.width()) * random.random())
        height = int((screen_geo.height() - pet_geo.height()) * random.random())
        self.move(width, height)

    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        self.condition = 1
        self.talk_condition = 1
        self.talk()
        self.randomAct()

        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        self.setCursor(QCursor(Qt.OpenHandCursor))

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    # 宠物右键点击交互 - 添加对话选项
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        todoAction = menu.addAction("待办")
        talkAction = menu.addAction("对话")
        memoryAction = menu.addAction("背单词")
        menu.addSeparator()
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAction:
            qApp.quit()
        elif action == hide:
            self.setWindowOpacity(0)
        elif action == talkAction:
            self.showInputDialog()
        elif action == todoAction:
            self.showTodoWidget()  # 新增：显示待办窗口
        elif action == memoryAction:
            self.showMemoryWidget()  # 新增：显示背单词窗口

    def showMemoryWidget(self):
        # 导入背单词应用类
        from word_memory import VocabularyApp
        import tkinter as tk
        # 创建 Tkinter 主窗口并启动应用
        root = tk.Tk()
        app = VocabularyApp(root)
        root.mainloop()


    def showTodoWidget(self):
        # 实例化待办窗口（父组件设为当前宠物窗口，数据文件指向项目内路径）
        self.todo_window = TodoWidget(parent=self, data_file="./source/todo.json")
        # 设置窗口位置（可选：跟随宠物位置）
        self.todo_window.move(self.pos().x() + self.width() + 10, self.pos().y())
        self.todo_window.show()

    # 显示输入对话框
    def showInputDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("与优菈对话")
        dialog.setWindowFlags(dialog.windowFlags() | Qt.FramelessWindowHint)  # 隐藏默认标题栏
        dialog.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景

        # 主布局（保持原有样式）
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏（保持原有样式）
        title_bar = QWidget(dialog)
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
        title_label = QLabel("与优菈对话", title_bar)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font: bold 12pt '华文中宋';
                padding-left: 12px;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.addWidget(title_label)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # 输入框容器（保持原有样式）
        input_container = QWidget(dialog)
        input_container.setStyleSheet("""
            QWidget {
                background: rgba(59, 130, 246, 0.7);
                border: 2px solid #1E3A8A;
                border-radius: 0 0 12px 12px;
                box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
            }
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(16, 12, 16, 12)

        # 输入框（保持原有样式）
        self.inputText = QLineEdit(input_container)
        self.inputText.setPlaceholderText("输入消息，按回车发送")
        self.inputText.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #FFFFFF;
                font: 12pt '华文中宋';
                border: 1px solid #60A5FA;
                border-radius: 8px;
                padding: 8px 12px;
                box-shadow: inset 0 2px 4px rgba(30, 58, 138, 0.2);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            QLineEdit:focus {
                border-color: #93C5FD;
                box-shadow: inset 0 2px 4px rgba(30, 58, 138, 0.3),
                            0 0 0 2px rgba(147, 197, 253, 0.5);
            }
        """)
        self.inputText.setFocus()

        # 连接回车键信号
        self.inputText.returnPressed.connect(lambda: self.handleUserInput(dialog))

        # 添加控件到布局
        input_layout.addWidget(self.inputText)
        main_layout.addWidget(title_bar)
        main_layout.addWidget(input_container)

        # 调整对话框大小
        dialog.resize(360, 100)

        # 调整输入框位置至宠物右侧
        self.adjustDialogPosition(dialog)

        # 显示对话框
        dialog.exec_()

    # 调整对话框位置至宠物右侧
    def adjustDialogPosition(self, dialog):
        # 获取宠物位置和尺寸
        pet_pos = self.pos()
        pet_size = self.size()
        dialog_size = dialog.size()

        # 计算理想位置（宠物右侧，顶部对齐）
        ideal_x = pet_pos.x() + pet_size.width() + 10  # 右侧偏移10px
        ideal_y = pet_pos.y()

        # 获取屏幕几何信息
        screen_geo = QDesktopWidget().screenGeometry()

        # 检测是否超出屏幕右侧
        if ideal_x + dialog_size.width() > screen_geo.width():
            # 超出则显示在宠物左侧
            ideal_x = pet_pos.x() - dialog_size.width() - 10
            # 确保不超出屏幕左侧
            if ideal_x < 0:
                ideal_x = 0

        # 检测是否超出屏幕顶部或底部
        if ideal_y < 0:
            ideal_y = 0
        if ideal_y + dialog_size.height() > screen_geo.height():
            ideal_y = screen_geo.height() - dialog_size.height()

        # 应用位置调整
        dialog.move(ideal_x, ideal_y)

    # 处理用户输入
    def handleUserInput(self, dialog):
        user_input = self.inputText.text().strip()
        if user_input:
            # 生成回复
            response = self.generateResponse(user_input)
            # 显示回复
            self.talkLabel.setText(response)
            self.talk_condition = 1
            self.optimizeBubbleSize()
            self.keepBubbleOnScreen()
            # 关闭对话框
            dialog.accept()

    # 生成回复（简单实现，可扩展为更复杂的对话逻辑）
    def generateResponse(self, user_input):
        # 优菈角色特性关键词匹配（融入贵族气质/傲娇性格/冰元素设定）
        keywords = {
            # 基础问候类（带傲娇语气）
            "你好": "哼，居然主动向我打招呼...别以为这样就能让我对你另眼相看，旅者。",
            "再见": "终于要分开了吗？也好，省得我一直想着该如何「报复」你刚才的无礼举动。",
            "名字": "听好了——我是优菈·劳伦斯，浪花骑士。记住这个名字，别在关键时刻给我丢脸。",
            # "时间": f"现在是{datetime.now().strftime("%Y年%m月%d日%H时%M分")}，我在等你回来。",

            # 角色背景类（劳伦斯家族/复仇主题）
            "劳伦斯": "哦？居然知道劳伦斯家族的名号...看来你对蒙德的历史有点研究。不过别用那种眼神看我，我和那些迂腐的贵族可不一样。",
            "复仇": "复仇是劳伦斯的传统，但我不会滥伤无辜。比如你刚才偷瞄我的事...我记下了，迟早会「好好回报」你的。",
            "贵族": "身为劳伦斯家族的末裔，优雅与高傲是刻在骨子里的。但别误会，我可不是那些只会摆架子的废物贵族。",

            # 元素与战斗类（冰元素/浪花骑士）
            "冰": "冰元素的力量吗？就像我的「极寒」一样，能让所有轻视劳伦斯的人尝到刺骨的滋味。",
            "浪花骑士": "浪花骑士的职责是守护蒙德，但这不代表我会对冒犯者手软。你刚才的行为，我已经列入「报复清单」了。",

            # 日常互动类（傲娇式关心）
            "谢谢": "啧，不过是举手之劳...别以为这样我就会对你降低「报复」的标准，旅者。",
            "饿了": "劳伦斯家族的人从不被食欲左右...但如果你非要请我喝一杯「蒲公英酒」，我倒是可以勉强陪你。",
            "冷": "冰元素力环绕的我怎么会冷？不过看你瑟瑟发抖的样子...算了，这股寒气分你一点，就当是「特别报复」了。"
        }

        # 检查关键词匹配
        for keyword, response in keywords.items():
            if keyword in user_input:
                return response

        # if("时间" in user_input):
        #     return f"现在是{datetime.now().strftime("%Y年%m月%d日%H时%M分")}，我在等你回来。"

        # 优菈风格的默认回复（保留傲娇+优雅语气）
        return random.choice([
            "哼，无聊...下次再用更有趣的话题来挑战我吧，旅者。",
            "你的话让我想起了某个需要「报复」的家伙...不过现在，先把你列入观察名单。",
            "劳伦斯的优雅不是谁都能理解的...你刚才的表情，我就当作是对我的赞美了。",
            "别用那种好奇的眼神盯着我！再看的话，我可要执行「眼神冒犯」的报复了哦？",
            "虽然不想承认，但你的话题还算有点意思...这就算是我今天允许你和我说话的理由吧。"
        ])


def get_today_incomplete_todos(todo_file="./source/todo.json", target_date=None) -> str:
    """
    以劳伦斯家的优雅，清点今日尚未了结的「债务」清单
    :param todo_file: 待办数据文件路径（默认使用项目内的source/todo.json）
    :param target_date: 目标日期（格式：YYYY-MM-DD），默认使用今天
    :return: 格式化后的未完成待办字符串，附带贵族式的「优雅」措辞
    """
    # 如果没有提供目标日期，则使用今天
    if target_date:
        today = target_date
    else:
        today = datetime.date.today().strftime("%Y-%m-%d")

    try:
        with open(todo_file, "r", encoding="utf-8") as f:
            todo_data = json.load(f)
    except FileNotFoundError:
        return "哼，看来是有人误把我的「债务清单」藏起来了... 文件未找到。"
    except json.JSONDecodeError:
        return "这文件的格式... 简直比蒙德城的酒鬼还要混乱！"

    # 获取目标日期待办列表
    today_todos = todo_data.get(today, [])
    incomplete_todos = [todo["content"] for todo in today_todos if not todo["completed"]]

    if not incomplete_todos:
        return "今天无未完成待办事项——哈哈，看来旅行者的效率就连西风骑士团也要甘拜下风！"

    # 以贵族式的优雅罗列「债务」
    debt_list = "；".join([f"{i + 1}. {todo}" for i, todo in enumerate(incomplete_todos)])
    return f"今天尚未清偿的「债务」如下：{debt_list}；记住，劳伦斯家的「优雅」从不允许拖欠！"

if __name__ == '__main__':
    # print(get_today_incomplete_todos(todo_file="./source/todo.json"))
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())