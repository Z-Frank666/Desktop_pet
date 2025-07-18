# Q版优菈——桌面宠物多功能助手

## 一、项目概述
本项目是一个集成桌面宠物交互、待办事项管理、考研词汇记忆功能的跨场景桌面应用，通过可爱的动态宠物形象降低工具使用门槛，提升学习/工作效率。

---

## 二、核心功能
### 1. 智能桌面宠物（`main.py`）
- **动态交互**：
  - 随机切换待机动作（`source/normal`目录下的GIF动画，支持自定义替换）
  - 鼠标点击触发互动动画（`source/click/image.gif`）
  - 自动调整对话气泡位置（避免超出屏幕边界）
- **智能对话**：
  - 从`source/dialog.txt`读取随机对话（支持中文多轮交互）
  - 自动同步今日未完成待办（通过`get_today_incomplete_todos`函数读取`source/todo.json`）
- **右键菜单**：包含「对话」「待办」「背单词」「退出」等快捷入口，支持快速跳转功能模块。

### 2. 待办事项管理（`todo_widget.py`）
- **基础功能**：添加/删除待办项、标记完成状态，数据持久化存储至`source/todo.json`。
- **智能提醒**：今日未完成待办自动推送至宠物对话气泡（结合`main.py`的对话逻辑）。

### 3. 考研词汇记忆（`word_memory.py`）
- **词库支持**：读取`source/考研词汇5500-乱序版+国家名称.txt`（格式：`单词 释义`）。
- **双模式学习**：
  - 看英文识中文：显示单词，点击「显示中文」验证记忆。
  - 看中文拼英文：显示释义，输入英文单词后检查拼写（支持短单词提示）。
- **学习统计**：实时计算正确率（绿色≥80%/黄色≥50%/红色<50%），辅助学习效果评估。

---

## 三、技术架构
### 1. 技术栈
| 模块         | 技术/工具          | 作用说明                          |
|--------------|--------------------|-----------------------------------|
| 桌面宠物核心  | PyQt5              | 窗口管理、动画渲染、右键菜单实现  |
| 待办事项     | PyQt5 + JSON       | 窗口界面设计、数据持久化存储      |
| 背单词       | Tkinter            | 轻量级GUI框架，快速实现学习界面    |
| 数据存储     | JSON               | 待办数据（`todo.json`）、词库文件  |
| 资源管理     | 本地文件系统       | GIF动画（`source/normal`）、对话文本（`dialog.txt`）等资源存储 |

### 2. 架构设计
```
main.py（主程序）
├─ 桌面宠物核心逻辑（窗口初始化、动画控制、对话管理）
├─ 右键菜单路由（调用待办/背单词模块）
│
├─ todo_widget.py（待办模块）
│  └─ 待办窗口界面 + JSON数据操作
│
└─ word_memory.py（背单词模块）
   └─ Tkinter界面 + 词库解析 + 学习统计
```
- **模块解耦**：主程序仅负责流程控制，待办/背单词功能独立成文件，便于单独维护或扩展。
- **资源集中管理**：所有静态资源（动画、词库、对话文本）存储于`source`目录，路径统一配置，降低维护成本。
- **跨框架兼容**：PyQt5（主宠物）与Tkinter（背单词）通过独立进程调用，避免GUI框架冲突。

---

## 四、运行环境与依赖
### 环境要求
- Python 3.8+（Windows/Linux/macOS）
- PyQt5（桌面窗口）：`pip install PyQt5`
- Tkinter（背单词界面）：Python标准库（部分系统需额外安装`python3-tk`）

### 运行步骤
（1）本地pycharm或python环境运行
1. 克隆项目

2. 进入项目目录：
   ```bash
   cd Desktop_pet
   ```
3. 启动主程序：
   ```bash
   python main.py
   ```
（2）exe文件运行
1. 克隆项目

2. 进入项目目录点击Desktop_pet2.0.exe运行
   

        
