#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口类
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget,
    QLineEdit, QPushButton, QLabel, QListWidget,
    QListWidgetItem, QGroupBox, QGridLayout, QFrame,
    QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal

import webbrowser
import platform
import ctypes
from src.tools.tool_manager import ToolManager
from src.navigation.navigation_manager import NavigationManager


class ToolButton(QPushButton):
    """工具按钮类"""
    
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setText(tool.name)
        self.setMinimumSize(120, 60)
        self.setMaximumSize(120, 60)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # 初始设置为亮色模式样式
        self.setStyleSheet("""
            ToolButton {
                background-color: #ffffff;
                border: 1px solid #d2e3fc;
                border-radius: 0px;
                padding: 5px;
                font-size: 11px;
                font-weight: bold;
                color: #1a73e8;
            }
            ToolButton:hover {
                background-color: #f0f7ff;
                border: 2px solid #1a73e8;
            }
            ToolButton:pressed {
                background-color: #e8f0fe;
            }
        """)
    
    def update_theme(self, is_dark):
        """更新主题样式"""
        if is_dark:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    border: 1px solid #444444;
                    border-radius: 0px;
                    padding: 5px;
                    font-size: 11px;
                    font-weight: bold;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #444444;
                    border: 2px solid #666666;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #d2e3fc;
                    border-radius: 0px;
                    padding: 5px;
                    font-size: 11px;
                    font-weight: bold;
                    color: #1a73e8;
                }
                QPushButton:hover {
                    background-color: #f0f7ff;
                    border: 2px solid #1a73e8;
                }
                QPushButton:pressed {
                    background-color: #e8f0fe;
                }
            """)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        if self.parent():
            window = self.window()
            if hasattr(window, 'show_tool_tooltip'):
                window.show_tool_tooltip(self.tool)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        if self.parent():
            window = self.window()
            if hasattr(window, 'hide_tool_tooltip'):
                window.hide_tool_tooltip()


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        # 检测系统主题
        self.is_dark_theme = self.is_system_dark_mode()
        self.init_ui()
        self.tool_manager = ToolManager()
        self.navigation_manager = NavigationManager()
        self.init_data()
        self.current_category = None
        self.is_pinned = False
        # 初始化主题
        self.update_theme()
    
    def is_system_dark_mode(self):
        """检测系统是否处于暗黑模式"""
        if platform.system() == 'Windows':
            # Windows系统检测
            try:
                # Windows 10/11 暗黑模式检测
                key = ctypes.windll.reg.OpenKeyEx(ctypes.windll.reg.HKEY_CURRENT_USER,
                                               "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                                               0, ctypes.windll.reg.KEY_READ)
                value = ctypes.c_ulong()
                size = ctypes.c_ulong(ctypes.sizeof(value))
                result = ctypes.windll.reg.QueryValueEx(key, "AppsUseLightTheme", None, None, ctypes.byref(value), ctypes.byref(size))
                ctypes.windll.reg.CloseKey(key)
                # 如果返回值为0，表示成功，value.value为0表示暗黑模式，1表示亮色模式
                if result == 0:
                    return value.value == 0
            except:
                pass
        elif platform.system() == 'Darwin':
            # macOS系统检测
            try:
                import subprocess
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                                      capture_output=True, text=True)
                return result.stdout.strip() == 'Dark'
            except:
                pass
        elif platform.system() == 'Linux':
            # Linux系统检测（基于常见桌面环境）
            try:
                import os
                # 检查GTK主题
                gtk_theme = os.environ.get('GTK_THEME', '')
                if 'dark' in gtk_theme.lower():
                    return True
                # 检查KDE主题
                kde_theme = os.environ.get('KDE_SESSION_VERSION', '')
                if kde_theme:
                    try:
                        import subprocess
                        result = subprocess.run(['kreadconfig5', '--file', 'kdeglobals', '--group', 'General', '--key', 'ColorScheme'],
                                              capture_output=True, text=True)
                        return 'dark' in result.stdout.strip().lower()
                    except:
                        pass
            except:
                pass
        # 默认返回亮色模式
        return False
    
    def update_theme(self):
        """更新主题"""
        # 更新主题按钮图标
        if self.is_dark_theme:
            self.theme_btn.setText("☀️")
        else:
            self.theme_btn.setText("🌙")
        
        # 更新标题栏样式
        if self.is_dark_theme:
            self.title_bar.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border-bottom: 2px solid #444444;
                }
            """)
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            self.creator_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            self.minimize_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            self.close_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            if self.is_pinned:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #ffffff;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        color: #ffffff;
                    }
                """)
            else:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #666666;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        color: #ffffff;
                    }
                """)
        else:
            self.title_bar.setStyleSheet("""
                QFrame {
                    background-color: #e8f0fe;
                    border-bottom: 2px solid #d2e3fc;
                }
            """)
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #1a73e8;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            self.creator_label.setStyleSheet("""
                QLabel {
                    color: #1a73e8;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            self.minimize_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #1a73e8;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            self.close_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #1a73e8;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #1a73e8;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #ff0000;
                }
            """)
            if self.is_pinned:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #1a73e8;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #1a73e8;
                    }
                    QPushButton:pressed {
                        color: #1a73e8;
                    }
                """)
            else:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #cccccc;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #1a73e8;
                    }
                    QPushButton:pressed {
                        color: #1a73e8;
                    }
                """)
        
        # 更新工具提示区域样式
        if self.is_dark_theme:
            self.tooltip_area.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border-bottom: 2px solid #444444;
                }
            """)
            self.tooltip_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.tooltip_desc.setStyleSheet("""
                QLabel {
                    color: #cccccc;
                    font-size: 12px;
                }
            """)
        else:
            self.tooltip_area.setStyleSheet("""
                QFrame {
                    background-color: #e8f0fe;
                    border-bottom: 2px solid #d2e3fc;
                }
            """)
            self.tooltip_label.setStyleSheet("""
                QLabel {
                    color: #1a73e8;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.tooltip_desc.setStyleSheet("""
                QLabel {
                    color: #174ea6;
                    font-size: 12px;
                }
            """)
        
        # 更新左侧分类面板样式
        if self.is_dark_theme:
            self.left_panel.setStyleSheet("""
                QFrame {
                    background-color: #1e1e1e;
                    border-right: 2px solid #444444;
                }
            """)
            title_label = self.left_panel.findChild(QLabel)
            if title_label:
                title_label.setStyleSheet("""
                    QLabel {
                        color: #ffffff;
                        padding: 10px;
                        background-color: #333333;
                        border-radius: 0px;
                    }
                """)
            self.search_edit.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #444444;
                    border-radius: 0px;
                    background-color: #333333;
                    color: #ffffff;
                }
                QLineEdit:focus {
                    border: 2px solid #666666;
                }
            """)
            self.category_list.setStyleSheet("""
                QListWidget {
                    background-color: #333333;
                    border: 1px solid #444444;
                    border-radius: 0px;
                    padding: 5px;
                    outline: none;
                    color: #ffffff;
                }
                QListWidget::item {
                    padding: 10px;
                    border-radius: 0px;
                    margin: 2px;
                    outline: none;
                    color: #ffffff;
                }
                QListWidget::item:hover {
                    background-color: #444444;
                    color: #ffffff;
                    outline: none;
                }
                QListWidget::item:selected {
                    background-color: #555555;
                    color: #ffffff;
                    outline: none;
                }
            """)
        else:
            self.left_panel.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border-right: 2px solid #d2e3fc;
                }
            """)
            title_label = self.left_panel.findChild(QLabel)
            if title_label:
                title_label.setStyleSheet("""
                    QLabel {
                        color: #1a73e8;
                        padding: 10px;
                        background-color: #e8f0fe;
                        border-radius: 0px;
                    }
                """)
            self.search_edit.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #d2e3fc;
                    border-radius: 0px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #1a73e8;
                }
            """)
            self.category_list.setStyleSheet("""
                QListWidget {
                    background-color: white;
                    border: 1px solid #d2e3fc;
                    border-radius: 0px;
                    padding: 5px;
                    outline: none;
                }
                QListWidget::item {
                    padding: 10px;
                    border-radius: 0px;
                    margin: 2px;
                    outline: none;
                }
                QListWidget::item:hover {
                    background-color: #1a73e8;
                    color: white;
                    outline: none;
                }
                QListWidget::item:selected {
                    background-color: #174ea6;
                    color: white;
                    outline: none;
                }
            """)
        
        # 更新右侧内容面板样式
        if self.is_dark_theme:
            self.right_panel.setStyleSheet("""
                QFrame {
                    background-color: #1e1e1e;
                }
            """)
            self.category_title.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    padding: 10px 0;
                    border-bottom: 1px solid #444444;
                }
            """)
        else:
            self.right_panel.setStyleSheet("""
                QFrame {
                    background-color: white;
                }
            """)
            self.category_title.setStyleSheet("""
                QLabel {
                    color: #1a73e8;
                    padding: 10px 0;
                    border-bottom: 1px solid #d2e3fc;
                }
            """)
        
        # 更新所有工具按钮的主题
        for tool_btn in self.tools_container.findChildren(ToolButton):
            tool_btn.update_theme(self.is_dark_theme)
        
        # 更新所有QPushButton类型的按钮（如推荐应用和网站导航中的按钮）
        for btn in self.tools_container.findChildren(QPushButton):
            if not isinstance(btn, ToolButton):
                if self.is_dark_theme:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #333333;
                            border: 1px solid #444444;
                            border-radius: 0px;
                            padding: 5px;
                            font-size: 11px;
                            font-weight: bold;
                            color: #ffffff;
                        }
                        QPushButton:hover {
                            background-color: #444444;
                            border: 2px solid #666666;
                        }
                        QPushButton:pressed {
                            background-color: #555555;
                        }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ffffff;
                            border: 1px solid #d2e3fc;
                            border-radius: 0px;
                            padding: 5px;
                            font-size: 11px;
                            font-weight: bold;
                            color: #1a73e8;
                        }
                        QPushButton:hover {
                            background-color: #f0f7ff;
                            border: 2px solid #1a73e8;
                        }
                        QPushButton:pressed {
                            background-color: #e8f0fe;
                        }
                    """)
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口属性
        self.setWindowTitle("SCTools")
        self.setGeometry(100, 100, 850, 500)
        self.setFixedSize(850, 500)
        # 隐藏默认标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        # 设置窗口图标
        import os
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "工具.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 自定义标题栏
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QFrame {
                background-color: #e8f0fe;
                border-bottom: 2px solid #d2e3fc;
            }
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(10)
        
        # 窗口标题
        self.title_label = QLabel("ScTools")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(self.title_label)
        
        # 制作人信息
        self.creator_label = QLabel(" - 制作人: 沙尘612")
        self.creator_label.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(self.creator_label)
        
        # 占位符
        title_layout.addStretch()
        
        # 置顶按钮
        self.pin_btn = QPushButton("置顶")
        self.pin_btn.setFixedSize(40, 24)
        self.pin_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #cccccc;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #1a73e8;
            }
            QPushButton:pressed {
                color: #1a73e8;
            }
        """)
        self.pin_btn.clicked.connect(self.toggle_pin)
        title_layout.addWidget(self.pin_btn)
        
        # 主题切换按钮
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(24, 24)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #1a73e8;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff0000;
            }
            QPushButton:pressed {
                color: #ff0000;
            }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme)
        title_layout.addWidget(self.theme_btn)
        
        # 最小化按钮
        self.minimize_btn = QPushButton("－")
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #1a73e8;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff0000;
            }
            QPushButton:pressed {
                color: #ff0000;
            }
        """)
        self.minimize_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.minimize_btn)
        
        # 关闭按钮
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #1a73e8;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff0000;
            }
            QPushButton:pressed {
                color: #ff0000;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.close_btn)
        
        main_layout.addWidget(self.title_bar)
        
        # 顶部工具提示区域
        self.tooltip_area = QFrame()
        self.tooltip_area.setFixedHeight(40)
        self.tooltip_area.setStyleSheet("""
            QFrame {
                background-color: #e8f0fe;
                border-bottom: 2px solid #d2e3fc;
            }
        """)
        tooltip_layout = QHBoxLayout(self.tooltip_area)
        tooltip_layout.setContentsMargins(20, 5, 20, 5)
        
        # 工具提示标签
        self.tooltip_label = QLabel("")
        self.tooltip_label.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.tooltip_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tooltip_layout.addWidget(self.tooltip_label)
        
        # 工具描述标签
        self.tooltip_desc = QLabel("")
        self.tooltip_desc.setStyleSheet("""
            QLabel {
                color: #174ea6;
                font-size: 12px;
            }
        """)
        self.tooltip_desc.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        tooltip_layout.addWidget(self.tooltip_desc)
        
        main_layout.addWidget(self.tooltip_area)
        
        # 内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 左侧分类面板
        self.left_panel = QFrame()
        self.left_panel.setFixedWidth(150)
        self.left_panel.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-right: 2px solid #d2e3fc;
            }
        """)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        title_label = QLabel("工具分类")
        title_font = QFont("Microsoft YaHei", 14, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                padding: 10px;
                background-color: #e8f0fe;
                border-radius: 0px;
            }
        """)
        left_layout.addWidget(title_label)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索工具...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #d2e3fc;
                border-radius: 0px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
            }
        """)
        self.search_edit.textChanged.connect(self.on_search)
        left_layout.addWidget(self.search_edit)
        
        # 分类列表
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #d2e3fc;
                border-radius: 0px;
                padding: 5px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 0px;
                margin: 2px;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #1a73e8;
                color: white;
                outline: none;
            }
            QListWidget::item:selected {
                background-color: #174ea6;
                color: white;
                outline: none;
            }
        """)
        self.category_list.itemClicked.connect(self.on_category_clicked)
        left_layout.addWidget(self.category_list)
        
        # 右侧内容面板
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # 分类标题
        self.category_title = QLabel("请选择一个分类")
        category_title_font = QFont("Microsoft YaHei", 16, QFont.Bold)
        self.category_title.setFont(category_title_font)
        self.category_title.setAlignment(Qt.AlignLeft)
        self.category_title.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                padding: 10px 0;
                border-bottom: 1px solid #d2e3fc;
            }
        """)
        right_layout.addWidget(self.category_title)
        
        # 工具内容区域（固定行列，无滚动条）
        self.tools_container = QWidget()
        self.tools_layout = QGridLayout(self.tools_container)
        self.tools_layout.setSpacing(10)
        self.tools_layout.setContentsMargins(0, 0, 0, 0)
        # 设置网格布局的对齐方式，让工具按钮从左上角开始排列
        self.tools_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        right_layout.addWidget(self.tools_container, 1)
        
        # 添加到内容布局
        content_layout.addWidget(self.left_panel)
        content_layout.addWidget(self.right_panel)
        
        # 添加到主布局
        main_layout.addWidget(content_widget)
    
    def show_tool_tooltip(self, tool):
        """显示工具提示"""
        if hasattr(tool, 'description'):
            # 工具对象或导航项对象
            if hasattr(tool, 'url'):
                # 导航项对象
                self.tooltip_label.setText(f"网站: {tool.name}")
                self.tooltip_desc.setText(tool.description)
            else:
                # 工具对象
                self.tooltip_label.setText(f"工具: {tool.name}")
                self.tooltip_desc.setText(tool.description)
    
    def hide_tool_tooltip(self):
        """隐藏工具提示"""
        if self.current_category:
            self.tooltip_label.setText(f"分类: {self.current_category}")
            self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
        else:
            self.tooltip_label.setText("ScTools - 多功能工具应用")
            self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, 'drag_start_position'):
                self.move(event.globalPos() - self.drag_start_position)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if hasattr(self, 'drag_start_position'):
            delattr(self, 'drag_start_position')
    
    def toggle_pin(self):
        """切换置顶状态"""
        self.is_pinned = not self.is_pinned
        
        # 设置窗口置顶
        if self.is_pinned:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        
        # 重新显示窗口
        self.show()
        
        # 更新置顶按钮样式
        if self.is_dark_theme:
            if self.is_pinned:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #ffffff;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        color: #ffffff;
                    }
                """)
            else:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #666666;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        color: #ffffff;
                    }
                """)
        else:
            if self.is_pinned:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #1a73e8;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #1a73e8;
                    }
                    QPushButton:pressed {
                        color: #1a73e8;
                    }
                """)
            else:
                self.pin_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #cccccc;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #1a73e8;
                    }
                    QPushButton:pressed {
                        color: #1a73e8;
                    }
                """)
    
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_theme = not self.is_dark_theme
        
        # 重新显示当前分类
        if self.current_category:
            self.show_category_tools(self.current_category)
        
        # 更新主题
        self.update_theme()
    
    def init_data(self):
        """初始化数据"""
        # 初始化分类列表
        self.init_categories()
        # 初始化默认内容
        self.init_default_content()
    
    def init_categories(self):
        """初始化分类列表"""
        categories = ["网站导航", "推荐应用", "系统工具", "磁盘工具", "硬件检测", "系统优化", "其他工具"]
        for category in categories:
            self.category_list.addItem(category)
    
    def on_category_clicked(self, item):
        """分类点击事件"""
        category_name = item.text()
        self.current_category = category_name
        self.show_category_tools(category_name)
        self.tooltip_label.setText(f"分类: {category_name}")
        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
    
    def init_default_content(self):
        """初始化默认内容"""
        # 清空工具容器
        self.clear_tools_container()
        
        # 更新分类标题
        self.category_title.setText("欢迎使用SCTools")
        
        # 临时修改网格布局的对齐方式为居中
        self.tools_layout.setAlignment(Qt.AlignCenter)
        
        # 创建欢迎标签
        welcome_label = QLabel("ScTools是一个集成多种实用小工具的应用程序，\n包含系统工具、网络工具、效率工具等类别。\n\n请从左侧选择一个分类查看工具。")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                padding: 20px;
                max-width: 500px;
                text-align: center;
                min-height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
        """)
        
        # 将欢迎标签添加到网格布局，占据整个区域
        self.tools_layout.addWidget(welcome_label, 0, 0, 1, 5)
    
    def on_search(self, text):
        """搜索工具"""
        # 过滤工具树
        self.filter_tool_tree(text)
    
    def on_tool_category_clicked(self, item, column):
        """工具分类点击事件"""
        if item.parent():
            # 点击了具体工具
            tool_name = item.text(column)
            self.show_tool_detail(tool_name)
        else:
            # 点击了分类
            category_name = item.text(column)
            self.show_category_tools(category_name)
    
    def on_search(self, text):
        """搜索工具"""
        # 显示搜索结果
        if text:
            self.show_search_results(text)
        else:
            # 清空搜索结果，显示默认内容
            self.clear_tools_container()
            self.init_default_content()
    
    def show_search_results(self, keyword):
        """显示搜索结果"""
        # 搜索工具
        search_results = self.tool_manager.search_tools(keyword)
        
        # 清空工具容器
        self.clear_tools_container()
        
        # 更新分类标题
        self.category_title.setText(f"搜索结果: {keyword}")
        
        # 修改网格布局的对齐方式，让搜索结果从左上角开始排列
        self.tools_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        if search_results:
            # 显示搜索结果
            row = 0
            col = 0
            for tool in search_results:
                tool_btn = ToolButton(tool, self.tools_container)
                tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                self.tools_layout.addWidget(tool_btn, row, col)
                col += 1
                if col >= 5:
                    col = 0
                    row += 1
        else:
            # 没有搜索结果
            no_result_label = QLabel("没有找到匹配的工具")
            no_result_label.setAlignment(Qt.AlignCenter)
            no_result_label.setStyleSheet("""
                QLabel {
                    color: #7f8c8d;
                    font-size: 14px;
                    padding: 50px;
                }
            """)
            self.tools_layout.addWidget(no_result_label, 0, 0)
    
    def show_category_tools(self, category_name):
        """显示分类工具列表"""
        # 清空工具容器
        self.clear_tools_container()
        
        # 更新分类标题
        self.category_title.setText(category_name)
        
        # 修改网格布局的对齐方式，让工具按钮从左上角开始排列
        self.tools_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # 显示工具
        row = 0
        col = 0
        for tool in self.tool_manager.tools:
            # 根据分类名称过滤工具
            if category_name == "系统工具":
                if tool.name in ["PCMaster", "Win11轻松设置", "WinNTSetup", "EasyRC", "HEU KMS激活", "ResHacker"]:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool.name)
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"工具: {t.name}")
                        self.tooltip_desc.setText(t.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText(f"分类: {category_name}")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1
            elif category_name == "磁盘工具":
                if tool.name in ["CrystalDiskInfo", "CrystalDiskMark", "DiskGenius", "WizTree", "分区助手", "Recuva"]:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool.name)
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"工具: {t.name}")
                        self.tooltip_desc.setText(t.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText(f"分类: {category_name}")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1




            elif category_name == "硬件检测":
                if tool.name in ["图拉丁硬件检测", "AIDA64", "GPU-Z", "ChipGenius", "Monitorinfo", "鼠标测试", "MOUSERATE", "键盘测试", "BIOSBackup"]:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool.name)
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"工具: {t.name}")
                        self.tooltip_desc.setText(t.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText(f"分类: {category_name}")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1
            elif category_name == "系统优化":
                if tool.name in ["CCleaner", "HiBit卸载器", "Dism++", "ContextMenuManager", "CrystalMark Retro"]:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool.name)
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"工具: {t.name}")
                        self.tooltip_desc.setText(t.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText(f"分类: {category_name}")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1

            elif category_name == "推荐应用":
                # 清空工具容器
                self.clear_tools_container()
                
                # 更新分类标题
                self.category_title.setText("推荐应用")
                
                # 修改网格布局的对齐方式，让推荐应用按钮从左上角开始排列
                self.tools_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                
                # 推荐应用列表
                recommended_tools = [
                    {"name": "格式工厂", "url": "https://www.pcgeshi.com/", "description": "多媒体格式转换工具"},
                    {"name": "PDFGear", "url": "https://www.pdfgear.com/", "description": "PDF工具"},
                    {"name": "PyCharm", "url": "https://www.jetbrains.com/pycharm/download/", "description": "Python IDE"},
                    {"name": "VSCode", "url": "https://code.visualstudio.com/Download", "description": "代码编辑器"},
                    {"name": "Obsidian", "url": "https://obsidian.md/download", "description": "知识管理，笔记软件"},
                    {"name": "LocalSend", "url": "https://localsend.org/download/", "description": "文件传输工具"},
                    {"name": "LXMusic", "url": "https://lxmusic.toside.cn/", "description": "音乐播放器"},
                    {"name": "Ani", "url": "https://myani.org/", "description": "动画软件"},
                    {"name": "Kazumi", "url": "https://kazumi.cn/", "description": "动漫软件"},
                    {"name": "PotPlayer", "url": "https://potplayer.info/download/", "description": "视频播放器"},
                    {"name": "TranslucentTB", "url": "https://translucenttb.net/", "description": "任务栏美化工具"},
                    {"name": "Steam", "url": "https://store.steampowered.com/download/", "description": "游戏平台"},
                    {"name": "Epic", "url": "https://www.epicgames.com/store/en-US/download", "description": "游戏平台"},
                    {"name": "Steam++", "url": "https://steampp.net/download", "description": "Steam辅助工具"},
                    {"name": "V2RayN", "url": "https://github.com/2dust/v2rayN/releases", "description": "网络工具，科学上网"},
                    {"name": "Blender", "url": "https://www.blender.org/download/", "description": "3D建模和动画软件"},
                    {"name": "OBS", "url": "https://obsproject.com/download", "description": "开源直播和录屏软件"},
                    {"name": "Chrome", "url": "https://www.google.com/chrome/downloads/", "description": "谷歌浏览器"},
                    {"name": "彩虹工具箱", "url": "https://rainbowbyte.com/", "description": "多功能工具集合"},
                    {"name": "贴汁", "url": "hhttps://tiez.name666.top/zh/", "description": "第三方粘贴板"},
                    {"name": "小智桌面", "url": "https://xzdesktop.cqttech.com/", "description": "桌面整理工具"},
                    {"name": "MTools", "url": "https://github.com/HG-ha/MTools", "description": "媒体多功能工具集合"},
                    {"name": "Waifu2x", "url": "https://gitee.com/aaronfeng0711/Waifu2x-Extension-GUI", "description": "图像放大和降噪工具"},
                    {"name": "Uotan Toolbox", "url": "https://toolbox.uotan.cn/", "description": "刷机工具箱"},
                    {"name": "网易有道翻译", "url": "https://fanyi.youdao.com/", "description": "在线翻译工具"}
                ]
                
                # 显示推荐应用
                row = 0
                col = 0
                for tool in recommended_tools:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool["name"])
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    # 连接点击事件
                    tool_btn.clicked.connect(lambda checked, url=tool["url"]: webbrowser.open(url))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"推荐应用: {t['name']}")
                        self.tooltip_desc.setText(t['description'])
                    
                    def leave_event(event):
                        self.tooltip_label.setText("分类: 推荐应用")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    # 添加到布局
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1
            elif category_name == "其他工具":
                if tool.name in ["NDM", "Motrix", "QBittorrent", "Windows超级管理器", "定时关机", "定时闹钟", "图片爬取", "Everything"]:
                    # 创建工具按钮
                    tool_btn = QPushButton(tool.name)
                    tool_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        tool_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    tool_btn.clicked.connect(lambda checked, t=tool: self.run_tool(t.name))
                    # 添加悬停事件
                    def enter_event(event, t=tool):
                        self.tooltip_label.setText(f"工具: {t.name}")
                        self.tooltip_desc.setText(t.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText(f"分类: {category_name}")
                        self.tooltip_desc.setText("鼠标悬停在工具上查看详细说明")
                    
                    tool_btn.enterEvent = enter_event
                    tool_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(tool_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1
            elif category_name == "网站导航":
                # 清空工具容器
                self.clear_tools_container()
                
                # 更新分类标题
                self.category_title.setText("网站导航")
                
                # 修改网格布局的对齐方式，让导航按钮从左上角开始排列
                self.tools_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                
                # 显示导航项
                row = 0
                col = 0
                for nav_item in self.navigation_manager.get_nav_items():
                    # 创建导航按钮
                    nav_btn = QPushButton(nav_item.name)
                    nav_btn.setFixedSize(120, 60)
                    # 根据当前主题设置按钮样式
                    if self.is_dark_theme:
                        nav_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #333333;
                                border: 1px solid #444444;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #ffffff;
                            }
                            QPushButton:hover {
                                background-color: #444444;
                                border: 2px solid #666666;
                            }
                            QPushButton:pressed {
                                background-color: #555555;
                            }
                        """)
                    else:
                        nav_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;
                                border: 1px solid #d2e3fc;
                                border-radius: 0px;
                                padding: 5px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #1a73e8;
                            }
                            QPushButton:hover {
                                background-color: #f0f7ff;
                                border: 2px solid #1a73e8;
                            }
                            QPushButton:pressed {
                                background-color: #e8f0fe;
                            }
                        """)
                    nav_btn.clicked.connect(lambda checked, item=nav_item: self.navigation_manager.open_url(item.url))
                    # 添加悬停事件
                    def enter_event(event, item=nav_item):
                        self.tooltip_label.setText(f"网站: {item.name}")
                        self.tooltip_desc.setText(item.description)
                    
                    def leave_event(event):
                        self.tooltip_label.setText("分类: 网站导航")
                        self.tooltip_desc.setText("鼠标悬停在网站上查看详细说明")
                    
                    nav_btn.enterEvent = enter_event
                    nav_btn.leaveEvent = leave_event
                    self.tools_layout.addWidget(nav_btn, row, col)
                    col += 1
                    if col >= 5:
                        col = 0
                        row += 1


    def clear_tools_container(self):
        """清空工具容器"""
        while self.tools_layout.count():
            item = self.tools_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def run_tool(self, tool_name):
        """运行工具"""
        # 获取工具对象
        tool = self.tool_manager.get_tool_by_name(tool_name)
        if tool:
            # 运行工具
            tool.run()
            # 更新工具提示
            self.tooltip_label.setText(f"工具已启动: {tool_name}")
            self.tooltip_desc.setText("工具正在运行中...")
