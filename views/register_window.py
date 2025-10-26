"""
注册窗口 - Register Window
PyQt5图形化注册界面
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QWidget, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class RegisterWindow(QDialog):
    """注册窗口类"""
    
    # 定义信号
    register_success = pyqtSignal()
    
    def __init__(self, user_controller):
        """
        初始化注册窗口
        :param user_controller: 用户控制器实例
        """
        super().__init__()
        self.user_controller = user_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("银行卡管理系统 - 注册")
        self.setFixedSize(1400, 800)  # 与登录窗口一致的尺寸
        
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
        left_title = QLabel("欢迎注册")
        left_title.setFont(QFont("Microsoft YaHei UI", 48, QFont.Bold))
        left_title.setStyleSheet("color: white; background: transparent;")
        left_title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_title)
        
        left_layout.addSpacing(30)
        
        # 左侧副标题
        left_subtitle = QLabel("User Registration")
        left_subtitle.setFont(QFont("Arial", 20))
        left_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        left_subtitle.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_subtitle)
        
        left_layout.addSpacing(50)
        
        # 左侧描述
        left_desc = QLabel("安全 · 便捷 · 可靠")
        left_desc.setFont(QFont("Microsoft YaHei UI", 24))
        left_desc.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent;")
        left_desc.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_desc)
        
        # 右侧注册表单区域
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: white;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 30, 60, 30)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f2f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c4c4c4;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        # 表单容器
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(0)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        welcome_title = QLabel("创建新账户")
        welcome_title.setFont(QFont("Microsoft YaHei UI", 32, QFont.Bold))
        welcome_title.setStyleSheet("color: #2d3436;")
        welcome_title.setAlignment(Qt.AlignLeft)
        welcome_title.setMinimumHeight(70)
        form_layout.addWidget(welcome_title)
        
        form_layout.addSpacing(10)
        
        # 副标题
        welcome_subtitle = QLabel("请填写以下信息完成注册")
        welcome_subtitle.setFont(QFont("Microsoft YaHei UI", 14))
        welcome_subtitle.setStyleSheet("color: #636e72;")
        welcome_subtitle.setAlignment(Qt.AlignLeft)
        welcome_subtitle.setMinimumHeight(35)
        form_layout.addWidget(welcome_subtitle)
        
        form_layout.addSpacing(30)
        
        # 用户名
        username_label = QLabel("用户名 (至少3个字符)")
        username_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        username_label.setStyleSheet("color: #2d3436;")
        username_label.setMinimumHeight(35)
        form_layout.addWidget(username_label)
        
        form_layout.addSpacing(8)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.username_input.setMinimumHeight(55)
        form_layout.addWidget(self.username_input)
        
        form_layout.addSpacing(20)
        
        # 密码
        password_label = QLabel("密码 (至少6个字符)")
        password_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        password_label.setStyleSheet("color: #2d3436;")
        password_label.setMinimumHeight(35)
        form_layout.addWidget(password_label)
        
        form_layout.addSpacing(8)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.password_input.setMinimumHeight(55)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(20)
        
        # 确认密码
        confirm_label = QLabel("确认密码")
        confirm_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        confirm_label.setStyleSheet("color: #2d3436;")
        confirm_label.setMinimumHeight(35)
        form_layout.addWidget(confirm_label)
        
        form_layout.addSpacing(8)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("请再次输入密码")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.confirm_input.setMinimumHeight(55)
        form_layout.addWidget(self.confirm_input)
        
        form_layout.addSpacing(20)
        
        # 真实姓名
        realname_label = QLabel("真实姓名")
        realname_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        realname_label.setStyleSheet("color: #2d3436;")
        realname_label.setMinimumHeight(35)
        form_layout.addWidget(realname_label)
        
        form_layout.addSpacing(8)
        
        self.realname_input = QLineEdit()
        self.realname_input.setPlaceholderText("请输入真实姓名")
        self.realname_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.realname_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.realname_input.setMinimumHeight(55)
        form_layout.addWidget(self.realname_input)
        
        form_layout.addSpacing(20)
        
        # 身份证号
        idcard_label = QLabel("身份证号 (18位)")
        idcard_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        idcard_label.setStyleSheet("color: #2d3436;")
        idcard_label.setMinimumHeight(35)
        form_layout.addWidget(idcard_label)
        
        form_layout.addSpacing(8)
        
        self.idcard_input = QLineEdit()
        self.idcard_input.setPlaceholderText("请输入18位身份证号")
        self.idcard_input.setMaxLength(18)
        self.idcard_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.idcard_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.idcard_input.setMinimumHeight(55)
        form_layout.addWidget(self.idcard_input)
        
        form_layout.addSpacing(20)
        
        # 手机号
        phone_label = QLabel("手机号 (11位)")
        phone_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        phone_label.setStyleSheet("color: #2d3436;")
        phone_label.setMinimumHeight(35)
        form_layout.addWidget(phone_label)
        
        form_layout.addSpacing(8)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("请输入11位手机号")
        self.phone_input.setMaxLength(11)
        self.phone_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.phone_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.phone_input.setMinimumHeight(55)
        form_layout.addWidget(self.phone_input)
        
        form_layout.addSpacing(20)
        
        # 邮箱
        email_label = QLabel("邮箱 (可选)")
        email_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        email_label.setStyleSheet("color: #2d3436;")
        email_label.setMinimumHeight(35)
        form_layout.addWidget(email_label)
        
        form_layout.addSpacing(8)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("请输入邮箱地址")
        self.email_input.setFont(QFont("Microsoft YaHei UI", 14))
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #2d3436;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.email_input.setMinimumHeight(55)
        form_layout.addWidget(self.email_input)
        
        form_layout.addSpacing(35)
        
        # 注册按钮
        self.register_button = QPushButton("注 册")
        self.register_button.setFont(QFont("Microsoft YaHei UI", 16, QFont.Bold))
        self.register_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 18px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
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
        self.register_button.setMinimumHeight(60)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)
        
        form_layout.addSpacing(15)
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setFont(QFont("Microsoft YaHei UI", 15))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #667eea;
                padding: 16px;
                border: 2px solid #667eea;
                border-radius: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #f0f3ff;
            }
        """)
        self.cancel_button.setMinimumHeight(55)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        form_layout.addWidget(self.cancel_button)
        
        form_layout.addSpacing(30)
        
        # 将表单容器添加到滚动区域
        scroll_area.setWidget(form_container)
        
        # 将滚动区域添加到右侧布局
        right_layout.addWidget(scroll_area)
        
        # 将左右面板添加到主布局（左侧占40%，右侧占60%）
        main_layout.addWidget(left_panel, 4)
        main_layout.addWidget(right_panel, 6)
    
    def handle_register(self):
        """处理注册事件"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pwd = self.confirm_input.text().strip()
        real_name = self.realname_input.text().strip()
        id_card = self.idcard_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        
        # 验证输入
        if not username:
            QMessageBox.warning(self, "提示", "请输入用户名！")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "提示", "请输入密码！")
            self.password_input.setFocus()
            return
        
        if not confirm_pwd:
            QMessageBox.warning(self, "提示", "请输入确认密码！")
            self.confirm_input.setFocus()
            return
        
        if password != confirm_pwd:
            QMessageBox.warning(self, "提示", "两次密码输入不一致！")
            self.confirm_input.clear()
            self.confirm_input.setFocus()
            return
        
        if not real_name:
            QMessageBox.warning(self, "提示", "请输入真实姓名！")
            self.realname_input.setFocus()
            return
        
        if not id_card:
            QMessageBox.warning(self, "提示", "请输入身份证号！")
            self.idcard_input.setFocus()
            return
        
        if not phone:
            QMessageBox.warning(self, "提示", "请输入手机号！")
            self.phone_input.setFocus()
            return
        
        # 调用控制器注册
        success, message = self.user_controller.register(
            username, password, real_name, id_card, phone, email
        )
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.register_success.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "注册失败", message)
    
    def clear_inputs(self):
        """清空所有输入框"""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.realname_input.clear()
        self.idcard_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.username_input.setFocus()
