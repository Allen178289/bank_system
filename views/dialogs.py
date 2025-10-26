"""
对话框模块 - Dialogs
包含各种功能对话框
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame,
                            QTableWidget, QTableWidgetItem, QTextEdit, QComboBox,
                            QGroupBox, QHeaderView, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# ==================== 用户管理对话框 ====================
class UserManagementDialog(QDialog):
    """用户管理对话框"""
    
    def __init__(self, user_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("用户管理")
        self.setFixedSize(750, 600)
        self.apply_styles()
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("用户信息管理")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976D2; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #ddd;")
        layout.addWidget(line)
        
        # 显示用户信息
        info_group = QGroupBox("个人信息")
        info_layout = QVBoxLayout()
        
        user_info = self.user_controller.get_user_info()
        if user_info:
            for key, value in user_info.items():
                info_line = QLabel(f"{key}: {value}")
                info_line.setStyleSheet("font-size: 14px; padding: 8px;")
                info_layout.addWidget(info_line)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 功能按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 修改信息按钮
        update_btn = QPushButton("修改信息")
        update_btn.setObjectName("primary_btn")
        update_btn.setCursor(Qt.PointingHandCursor)
        update_btn.clicked.connect(self.show_update_dialog)
        button_layout.addWidget(update_btn)
        
        # 修改密码按钮
        change_pwd_btn = QPushButton("修改密码")
        change_pwd_btn.setObjectName("warning_btn")
        change_pwd_btn.setCursor(Qt.PointingHandCursor)
        change_pwd_btn.clicked.connect(self.show_change_password_dialog)
        button_layout.addWidget(change_pwd_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setObjectName("normal_btn")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                border-radius: 5px;
                border: none;
            }
            QPushButton#primary_btn {
                background-color: #1976D2;
                color: white;
            }
            QPushButton#primary_btn:hover {
                background-color: #1565C0;
            }
            QPushButton#warning_btn {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#warning_btn:hover {
                background-color: #F57C00;
            }
            QPushButton#normal_btn {
                background-color: white;
                color: #333;
                border: 2px solid #ddd;
            }
            QPushButton#normal_btn:hover {
                background-color: #f5f5f5;
            }
        """)
    
    def show_update_dialog(self):
        """显示修改信息对话框"""
        dialog = UpdateUserInfoDialog(self.user_controller, self)
        if dialog.exec_():
            # 刷新显示
            self.close()
            new_dialog = UserManagementDialog(self.user_controller, self.parent())
            new_dialog.exec_()
    
    def show_change_password_dialog(self):
        """显示修改密码对话框"""
        dialog = ChangePasswordDialog(self.user_controller, self)
        dialog.exec_()


class UpdateUserInfoDialog(QDialog):
    """修改用户信息对话框"""
    
    def __init__(self, user_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("修改个人信息")
        self.setFixedSize(550, 320)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 手机号
        phone_layout = QVBoxLayout()
        phone_label = QLabel("新手机号 (11位，留空则不修改):")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("请输入新手机号")
        self.phone_input.setMaxLength(11)
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)
        
        # 邮箱
        email_layout = QVBoxLayout()
        email_label = QLabel("新邮箱 (留空则不修改):")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("请输入新邮箱")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        confirm_btn = QPushButton("确认修改")
        confirm_btn.clicked.connect(self.handle_update)
        button_layout.addWidget(confirm_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 18px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
        """)
    
    def handle_update(self):
        """处理更新"""
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        
        if not phone and not email:
            QMessageBox.warning(self, "提示", "请至少修改一项信息！")
            return
        
        success, message = self.user_controller.update_user_info(
            phone if phone else None,
            email if email else None
        )
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()
        else:
            QMessageBox.critical(self, "失败", message)


class ChangePasswordDialog(QDialog):
    """修改密码对话框"""
    
    def __init__(self, user_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("修改密码")
        self.setFixedSize(550, 350)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 旧密码
        old_pwd_layout = QVBoxLayout()
        old_pwd_label = QLabel("旧密码:")
        self.old_pwd_input = QLineEdit()
        self.old_pwd_input.setEchoMode(QLineEdit.Password)
        self.old_pwd_input.setPlaceholderText("请输入旧密码")
        old_pwd_layout.addWidget(old_pwd_label)
        old_pwd_layout.addWidget(self.old_pwd_input)
        layout.addLayout(old_pwd_layout)
        
        # 新密码
        new_pwd_layout = QVBoxLayout()
        new_pwd_label = QLabel("新密码 (至少6个字符):")
        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        self.new_pwd_input.setPlaceholderText("请输入新密码")
        new_pwd_layout.addWidget(new_pwd_label)
        new_pwd_layout.addWidget(self.new_pwd_input)
        layout.addLayout(new_pwd_layout)
        
        # 确认密码
        confirm_layout = QVBoxLayout()
        confirm_label = QLabel("确认新密码:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("请再次输入新密码")
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        layout.addLayout(confirm_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        confirm_btn = QPushButton("确认修改")
        confirm_btn.clicked.connect(self.handle_change_password)
        button_layout.addWidget(confirm_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 18px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
        """)
    
    def handle_change_password(self):
        """处理修改密码"""
        old_pwd = self.old_pwd_input.text().strip()
        new_pwd = self.new_pwd_input.text().strip()
        confirm_pwd = self.confirm_input.text().strip()
        
        if not old_pwd:
            QMessageBox.warning(self, "提示", "请输入旧密码！")
            return
        
        if not new_pwd:
            QMessageBox.warning(self, "提示", "请输入新密码！")
            return
        
        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "提示", "两次密码输入不一致！")
            return
        
        success, message = self.user_controller.change_password(old_pwd, new_pwd)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()
        else:
            QMessageBox.critical(self, "失败", message)


# ==================== 开户对话框 ====================
class CreateAccountDialog(QDialog):
    """开户对话框"""
    
    def __init__(self, account_controller, parent=None):
        super().__init__(parent)
        self.account_controller = account_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("开户")
        self.setFixedSize(550, 270)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("开设新账户")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976D2; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 初始余额
        balance_layout = QVBoxLayout()
        balance_label = QLabel("初始存款金额 (元):")
        self.balance_input = QDoubleSpinBox()
        self.balance_input.setRange(0, 1000000000)
        self.balance_input.setDecimals(2)
        self.balance_input.setValue(0)
        self.balance_input.setPrefix("¥ ")
        balance_layout.addWidget(balance_label)
        balance_layout.addWidget(self.balance_input)
        layout.addLayout(balance_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        create_btn = QPushButton("开户")
        create_btn.clicked.connect(self.handle_create)
        button_layout.addWidget(create_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QDoubleSpinBox {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
        """)
    
    def handle_create(self):
        """处理开户"""
        initial_balance = self.balance_input.value()
        
        success, message, card_number = self.account_controller.create_account(initial_balance)
        
        if success:
            QMessageBox.information(self, "成功", f"{message}\n\n请妥善保管您的卡号！")
            self.accept()
        else:
            QMessageBox.critical(self, "失败", message)


# ==================== 存款对话框 ====================
class DepositDialog(QDialog):
    """存款对话框"""
    
    def __init__(self, account_controller, parent=None):
        super().__init__(parent)
        self.account_controller = account_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("存款")
        self.setFixedSize(600, 320)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("存款操作")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4CAF50; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 选择账户
        account_layout = QVBoxLayout()
        account_label = QLabel("选择账户:")
        self.account_combo = QComboBox()
        self.load_accounts()
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_combo)
        layout.addLayout(account_layout)
        
        # 存款金额
        amount_layout = QVBoxLayout()
        amount_label = QLabel("存款金额 (元):")
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 1000000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(100)
        self.amount_input.setPrefix("¥ ")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        deposit_btn = QPushButton("存款")
        deposit_btn.clicked.connect(self.handle_deposit)
        button_layout.addWidget(deposit_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QComboBox, QDoubleSpinBox {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
        """)
    
    def load_accounts(self):
        """加载账户列表"""
        accounts = self.account_controller.get_my_accounts()
        self.account_combo.clear()
        for account in accounts:
            self.account_combo.addItem(
                f"{account.card_number} - 余额: ¥{account.balance:.2f} - {account.status}",
                account.card_number
            )
    
    def handle_deposit(self):
        """处理存款"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户，请先开户！")
            return
        
        card_number = self.account_combo.currentData()
        amount = self.amount_input.value()
        
        success, message = self.account_controller.deposit(card_number, amount)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()
        else:
            QMessageBox.critical(self, "失败", message)


# ==================== 取款对话框 ====================
class WithdrawDialog(QDialog):
    """取款对话框"""
    
    def __init__(self, account_controller, parent=None):
        super().__init__(parent)
        self.account_controller = account_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("取款")
        self.setFixedSize(600, 320)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("取款操作")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF9800; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 选择账户
        account_layout = QVBoxLayout()
        account_label = QLabel("选择账户:")
        self.account_combo = QComboBox()
        self.load_accounts()
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_combo)
        layout.addLayout(account_layout)
        
        # 取款金额
        amount_layout = QVBoxLayout()
        amount_label = QLabel("取款金额 (元):")
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 1000000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(100)
        self.amount_input.setPrefix("¥ ")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        withdraw_btn = QPushButton("取款")
        withdraw_btn.clicked.connect(self.handle_withdraw)
        button_layout.addWidget(withdraw_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QComboBox, QDoubleSpinBox {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
        """)
    
    def load_accounts(self):
        """加载账户列表"""
        accounts = self.account_controller.get_my_accounts()
        self.account_combo.clear()
        for account in accounts:
            self.account_combo.addItem(
                f"{account.card_number} - 余额: ¥{account.balance:.2f} - {account.status}",
                account.card_number
            )
    
    def handle_withdraw(self):
        """处理取款"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户，请先开户！")
            return
        
        card_number = self.account_combo.currentData()
        amount = self.amount_input.value()
        
        success, message = self.account_controller.withdraw(card_number, amount)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()
        else:
            QMessageBox.critical(self, "失败", message)


# ==================== 账户管理对话框 ====================
class AccountManagementDialog(QDialog):
    """账户管理对话框"""
    
    def __init__(self, account_controller, parent=None):
        super().__init__(parent)
        self.account_controller = account_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("账户管理")
        self.setFixedSize(650, 520)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("账户管理")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976D2; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 选择账户
        account_layout = QVBoxLayout()
        account_label = QLabel("选择账户:")
        self.account_combo = QComboBox()
        self.load_accounts()
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_combo)
        layout.addLayout(account_layout)
        
        # 操作按钮组
        operations_group = QGroupBox("账户操作")
        operations_layout = QVBoxLayout()
        operations_layout.setSpacing(10)
        
        # 挂失按钮
        report_loss_btn = QPushButton("🔒 挂失")
        report_loss_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        report_loss_btn.clicked.connect(self.handle_report_loss)
        operations_layout.addWidget(report_loss_btn)
        
        # 解除挂失按钮
        cancel_loss_btn = QPushButton("🔓 解除挂失")
        cancel_loss_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        cancel_loss_btn.clicked.connect(self.handle_cancel_loss)
        operations_layout.addWidget(cancel_loss_btn)
        
        # 冻结按钮
        freeze_btn = QPushButton("❄️ 冻结账户")
        freeze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        freeze_btn.clicked.connect(self.handle_freeze)
        operations_layout.addWidget(freeze_btn)
        
        # 解冻按钮
        unfreeze_btn = QPushButton("☀️ 解冻账户")
        unfreeze_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        unfreeze_btn.clicked.connect(self.handle_unfreeze)
        operations_layout.addWidget(unfreeze_btn)
        
        # 销户按钮
        close_btn = QPushButton("⛔ 销户")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        close_btn.clicked.connect(self.handle_close_account)
        operations_layout.addWidget(close_btn)
        
        operations_group.setLayout(operations_layout)
        layout.addWidget(operations_group)
        
        # 关闭按钮
        close_dialog_btn = QPushButton("关闭")
        close_dialog_btn.clicked.connect(self.accept)
        layout.addWidget(close_dialog_btn)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QComboBox {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: white;
            }
        """)
    
    def load_accounts(self):
        """加载账户列表"""
        accounts = self.account_controller.get_my_accounts()
        self.account_combo.clear()
        for account in accounts:
            self.account_combo.addItem(
                f"{account.card_number} - {account.status}",
                account.card_number
            )
    
    def handle_report_loss(self):
        """挂失"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户！")
            return
        
        card_number = self.account_combo.currentData()
        
        reply = QMessageBox.question(
            self, '确认', '确定要挂失该账户吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.account_controller.report_loss(card_number)
            if success:
                QMessageBox.information(self, "成功", message)
                self.load_accounts()
            else:
                QMessageBox.critical(self, "失败", message)
    
    def handle_cancel_loss(self):
        """解除挂失"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户！")
            return
        
        card_number = self.account_combo.currentData()
        success, message = self.account_controller.cancel_loss(card_number)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.load_accounts()
        else:
            QMessageBox.critical(self, "失败", message)
    
    def handle_freeze(self):
        """冻结"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户！")
            return
        
        card_number = self.account_combo.currentData()
        
        reply = QMessageBox.question(
            self, '确认', '确定要冻结该账户吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.account_controller.freeze_account(card_number)
            if success:
                QMessageBox.information(self, "成功", message)
                self.load_accounts()
            else:
                QMessageBox.critical(self, "失败", message)
    
    def handle_unfreeze(self):
        """解冻"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户！")
            return
        
        card_number = self.account_combo.currentData()
        success, message = self.account_controller.unfreeze_account(card_number)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.load_accounts()
        else:
            QMessageBox.critical(self, "失败", message)
    
    def handle_close_account(self):
        """销户"""
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "提示", "您还没有开户！")
            return
        
        card_number = self.account_combo.currentData()
        
        reply = QMessageBox.question(
            self, '警告', '确定要销户吗？此操作不可恢复！\n\n注意：账户余额必须为0才能销户。',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.account_controller.close_account(card_number)
            if success:
                QMessageBox.information(self, "成功", message)
                self.load_accounts()
            else:
                QMessageBox.critical(self, "失败", message)


# ==================== 交易记录对话框 ====================
class TransactionHistoryDialog(QDialog):
    """交易记录对话框"""
    
    def __init__(self, account_controller, card_number, parent=None):
        super().__init__(parent)
        self.account_controller = account_controller
        self.card_number = card_number
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"交易记录 - {self.card_number}")
        self.setFixedSize(900, 650)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel(f"账户交易记录")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976D2; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 卡号显示
        card_label = QLabel(f"卡号: {self.card_number}")
        card_label.setStyleSheet("font-size: 15px; color: #666;")
        card_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(card_label)
        
        # 交易记录表格
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(4)
        self.transaction_table.setHorizontalHeaderLabels(['时间', '类型', '金额 (元)', '余额 (元)'])
        self.transaction_table.horizontalHeader().setStretchLastSection(True)
        self.transaction_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.transaction_table.setColumnWidth(0, 180)
        self.transaction_table.setColumnWidth(1, 100)
        self.transaction_table.setColumnWidth(2, 120)
        
        self.transaction_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # 设置行高
        self.transaction_table.verticalHeader().setDefaultSectionSize(45)
        
        # 加载交易记录
        self.load_transactions()
        
        layout.addWidget(self.transaction_table)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
            }
        """)
    
    def load_transactions(self):
        """加载交易记录"""
        success, transactions = self.account_controller.get_transaction_history(self.card_number)
        
        if not success or not transactions:
            self.transaction_table.setRowCount(0)
            return
        
        self.transaction_table.setRowCount(len(transactions))
        
        for row, trans in enumerate(transactions):
            # 时间
            time_item = QTableWidgetItem(trans['time'])
            time_item.setTextAlignment(Qt.AlignCenter)
            self.transaction_table.setItem(row, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(trans['type'])
            type_item.setTextAlignment(Qt.AlignCenter)
            # 根据类型设置颜色
            if trans['type'] == '存款':
                type_item.setForeground(Qt.darkGreen)
            elif trans['type'] == '取款':
                type_item.setForeground(Qt.darkRed)
            self.transaction_table.setItem(row, 1, type_item)
            
            # 金额
            amount_item = QTableWidgetItem(f"{trans['amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 2, amount_item)
            
            # 余额
            balance_item = QTableWidgetItem(f"{trans['balance_after']:.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 3, balance_item)

