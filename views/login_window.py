"""
登录窗口 - Login Window
PyQt5图形化登录界面
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LoginWindow(QDialog):
    """登录窗口类"""
    
    # 定义信号
    login_success = pyqtSignal()
    open_register = pyqtSignal()
    
    def __init__(self, user_controller):
        """
        初始化登录窗口
        :param user_controller: 用户控制器实例
        """
        super().__init__()
        self.user_controller = user_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("银行卡管理系统")
        self.setFixedSize(1400, 800)  # 适配2K分辨率
        
        # 设置窗口背景
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
            }
        """)
        
        # 主布局 - 水平布局（左右分栏）
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 左侧装饰区域
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # 左侧标题
        left_title = QLabel("银行卡管理系统")
        left_title.setFont(QFont("Microsoft YaHei UI", 48, QFont.Bold))
        left_title.setStyleSheet("color: white; background: transparent;")
        left_title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_title)
        
        left_layout.addSpacing(30)
        
        # 左侧副标题
        left_subtitle = QLabel("Bank Card Management System")
        left_subtitle.setFont(QFont("Arial", 20))
        left_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        left_subtitle.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_subtitle)
        
        left_layout.addSpacing(50)
        
        # 左侧描述
        left_desc = QLabel("安全 · 便捷 · 高效")
        left_desc.setFont(QFont("Microsoft YaHei UI", 24))
        left_desc.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent;")
        left_desc.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_desc)
        
        # 右侧登录表单区域
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: white;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(80, 0, 80, 0)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # 表单容器
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(0)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # 欢迎标题
        welcome_title = QLabel("欢迎登录")
        welcome_title.setFont(QFont("Microsoft YaHei UI", 36, QFont.Bold))
        welcome_title.setStyleSheet("color: #2d3436;")
        welcome_title.setAlignment(Qt.AlignLeft)
        welcome_title.setMinimumHeight(80)
        form_layout.addWidget(welcome_title)
        
        form_layout.addSpacing(15)
        
        # 欢迎副标题
        welcome_subtitle = QLabel("请输入您的账号信息")
        welcome_subtitle.setFont(QFont("Microsoft YaHei UI", 16))
        welcome_subtitle.setStyleSheet("color: #636e72;")
        welcome_subtitle.setAlignment(Qt.AlignLeft)
        welcome_subtitle.setMinimumHeight(40)
        form_layout.addWidget(welcome_subtitle)
        
        form_layout.addSpacing(50)
        
        # 用户名标签
        username_label = QLabel("用户名")
        username_label.setFont(QFont("Microsoft YaHei UI", 16, QFont.Bold))
        username_label.setStyleSheet("color: #2d3436;")
        username_label.setMinimumHeight(40)
        form_layout.addWidget(username_label)
        
        form_layout.addSpacing(10)
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setFont(QFont("Microsoft YaHei UI", 16))
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 18px 20px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.username_input.setMinimumHeight(65)
        form_layout.addWidget(self.username_input)
        
        form_layout.addSpacing(30)
        
        # 密码标签
        password_label = QLabel("密码")
        password_label.setFont(QFont("Microsoft YaHei UI", 16, QFont.Bold))
        password_label.setStyleSheet("color: #2d3436;")
        password_label.setMinimumHeight(40)
        form_layout.addWidget(password_label)
        
        form_layout.addSpacing(10)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Microsoft YaHei UI", 16))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 18px 20px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.password_input.setMinimumHeight(65)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(50)
        
        # 登录按钮
        self.login_button = QPushButton("登 录")
        self.login_button.setFont(QFont("Microsoft YaHei UI", 18, QFont.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 20px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4557c2, stop:1 #5a3580);
            }
        """)
        self.login_button.setMinimumHeight(70)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        form_layout.addSpacing(20)
        
        # 注册按钮
        self.register_button = QPushButton("没有账号？立即注册")
        self.register_button.setFont(QFont("Microsoft YaHei UI", 16))
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #667eea;
                padding: 18px;
                border: 2px solid #667eea;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f0f3ff;
            }
        """)
        self.register_button.setMinimumHeight(65)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)
        
        # 添加表单容器到右侧布局
        right_layout.addWidget(form_container)
        
        # 将左右面板添加到主布局（左侧占40%，右侧占60%）
        main_layout.addWidget(left_panel, 4)
        main_layout.addWidget(right_panel, 6)
        
        # 回车键绑定
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """处理登录事件"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "提示", "请输入用户名！")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "提示", "请输入密码！")
            self.password_input.setFocus()
            return
        
        success, message = self.user_controller.login(username, password)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.login_success.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "登录失败", message)
            self.password_input.clear()
            self.password_input.setFocus()
    
    def handle_register(self):
        """打开注册窗口"""
        self.open_register.emit()
    
    def clear_inputs(self):
        """清空输入框"""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()
