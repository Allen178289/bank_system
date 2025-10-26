"""
主窗口 - Main Window
PyQt5图形化主界面（登录后）
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox, QFrame, QGroupBox, QHeaderView, QMenu, QAction)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon


class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 定义信号
    logout_signal = pyqtSignal()
    
    def __init__(self, user_controller, account_controller):
        """
        初始化主窗口
        :param user_controller: 用户控制器实例
        :param account_controller: 账户控制器实例
        """
        super().__init__()
        self.user_controller = user_controller
        self.account_controller = account_controller
        self.init_ui()
        self.refresh_accounts()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("银行卡管理系统")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel#welcome_label {
                font-size: 22px;
                font-weight: bold;
                color: #1976D2;
            }
            QLabel#info_label {
                font-size: 14px;
                color: #666;
            }
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
                border: none;
                min-height: 20px;
            }
            QPushButton#primary_btn {
                background-color: #1976D2;
                color: white;
            }
            QPushButton#primary_btn:hover {
                background-color: #1565C0;
            }
            QPushButton#secondary_btn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#secondary_btn:hover {
                background-color: #45a049;
            }
            QPushButton#warning_btn {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#warning_btn:hover {
                background-color: #F57C00;
            }
            QPushButton#danger_btn {
                background-color: #F44336;
                color: white;
            }
            QPushButton#danger_btn:hover {
                background-color: #D32F2F;
            }
            QPushButton#normal_btn {
                background-color: white;
                color: #333;
                border: 2px solid #ddd;
            }
            QPushButton#normal_btn:hover {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #e0e0e0;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
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
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 25, 30, 25)
        
        # 顶部信息栏
        top_layout = QHBoxLayout()
        
        # 欢迎信息
        current_user = self.user_controller.get_current_user()
        welcome_label = QLabel(f"欢迎，{current_user.real_name}")
        welcome_label.setObjectName("welcome_label")
        top_layout.addWidget(welcome_label)
        
        top_layout.addStretch()
        
        # 用户名标签
        username_label = QLabel(f"用户名: {current_user.username}")
        username_label.setObjectName("info_label")
        top_layout.addWidget(username_label)
        
        # 退出登录按钮
        logout_btn = QPushButton("退出登录")
        logout_btn.setObjectName("normal_btn")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.handle_logout)
        top_layout.addWidget(logout_btn)
        
        main_layout.addLayout(top_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)
        
        # 功能按钮区域
        button_group = QGroupBox("功能菜单")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 用户管理
        user_btn = QPushButton("👤 用户管理")
        user_btn.setObjectName("primary_btn")
        user_btn.setCursor(Qt.PointingHandCursor)
        user_btn.clicked.connect(self.show_user_management)
        button_layout.addWidget(user_btn)
        
        # 开户
        create_account_btn = QPushButton("➕ 开户")
        create_account_btn.setObjectName("secondary_btn")
        create_account_btn.setCursor(Qt.PointingHandCursor)
        create_account_btn.clicked.connect(self.handle_create_account)
        button_layout.addWidget(create_account_btn)
        
        # 存款
        deposit_btn = QPushButton("💰 存款")
        deposit_btn.setObjectName("secondary_btn")
        deposit_btn.setCursor(Qt.PointingHandCursor)
        deposit_btn.clicked.connect(self.handle_deposit)
        button_layout.addWidget(deposit_btn)
        
        # 取款
        withdraw_btn = QPushButton("💸 取款")
        withdraw_btn.setObjectName("warning_btn")
        withdraw_btn.setCursor(Qt.PointingHandCursor)
        withdraw_btn.clicked.connect(self.handle_withdraw)
        button_layout.addWidget(withdraw_btn)
        
        # 账户管理
        account_mgmt_btn = QPushButton("⚙️ 账户管理")
        account_mgmt_btn.setObjectName("normal_btn")
        account_mgmt_btn.setCursor(Qt.PointingHandCursor)
        account_mgmt_btn.clicked.connect(self.show_account_management)
        button_layout.addWidget(account_mgmt_btn)
        
        # 刷新
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setObjectName("normal_btn")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_accounts)
        button_layout.addWidget(refresh_btn)
        
        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)
        
        # 账户列表区域
        account_group = QGroupBox("我的账户")
        account_layout = QVBoxLayout()
        
        # 创建表格
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(5)
        self.account_table.setHorizontalHeaderLabels(['卡号', '余额 (元)', '状态', '开户时间', '操作'])
        self.account_table.horizontalHeader().setStretchLastSection(True)
        self.account_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.account_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.account_table.setAlternatingRowColors(True)
        self.account_table.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.account_table.setColumnWidth(0, 250)
        self.account_table.setColumnWidth(1, 180)
        self.account_table.setColumnWidth(2, 120)
        self.account_table.setColumnWidth(3, 220)
        
        # 设置行高
        self.account_table.verticalHeader().setDefaultSectionSize(50)
        
        account_layout.addWidget(self.account_table)
        account_group.setLayout(account_layout)
        main_layout.addWidget(account_group)
        
        # 设置布局
        central_widget.setLayout(main_layout)
    
    def refresh_accounts(self):
        """刷新账户列表"""
        accounts = self.account_controller.get_my_accounts()
        
        self.account_table.setRowCount(len(accounts))
        
        for row, account in enumerate(accounts):
            # 卡号
            card_item = QTableWidgetItem(account.card_number)
            card_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 0, card_item)
            
            # 余额
            balance_item = QTableWidgetItem(f"{account.balance:.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.account_table.setItem(row, 1, balance_item)
            
            # 状态
            status_item = QTableWidgetItem(account.status)
            status_item.setTextAlignment(Qt.AlignCenter)
            # 根据状态设置颜色
            if account.status == "正常":
                status_item.setForeground(Qt.darkGreen)
            elif account.status == "冻结":
                status_item.setForeground(Qt.blue)
            elif account.status == "挂失":
                status_item.setForeground(Qt.red)
            else:
                status_item.setForeground(Qt.gray)
            self.account_table.setItem(row, 2, status_item)
            
            # 开户时间
            time_item = QTableWidgetItem(account.created_at)
            time_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 3, time_item)
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(5, 2, 5, 2)
            btn_layout.setSpacing(5)
            
            # 查看交易记录按钮
            detail_btn = QPushButton("交易记录")
            detail_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            detail_btn.setCursor(Qt.PointingHandCursor)
            detail_btn.clicked.connect(lambda checked, cn=account.card_number: self.view_transaction_history(cn))
            btn_layout.addWidget(detail_btn)
            
            btn_widget.setLayout(btn_layout)
            self.account_table.setCellWidget(row, 4, btn_widget)
    
    def handle_create_account(self):
        """处理开户"""
        from views.dialogs import CreateAccountDialog
        dialog = CreateAccountDialog(self.account_controller, self)
        if dialog.exec_():
            self.refresh_accounts()
    
    def handle_deposit(self):
        """处理存款"""
        from views.dialogs import DepositDialog
        dialog = DepositDialog(self.account_controller, self)
        if dialog.exec_():
            self.refresh_accounts()
    
    def handle_withdraw(self):
        """处理取款"""
        from views.dialogs import WithdrawDialog
        dialog = WithdrawDialog(self.account_controller, self)
        if dialog.exec_():
            self.refresh_accounts()
    
    def show_user_management(self):
        """显示用户管理"""
        from views.dialogs import UserManagementDialog
        dialog = UserManagementDialog(self.user_controller, self)
        dialog.exec_()
    
    def show_account_management(self):
        """显示账户管理"""
        from views.dialogs import AccountManagementDialog
        dialog = AccountManagementDialog(self.account_controller, self)
        if dialog.exec_():
            self.refresh_accounts()
    
    def view_transaction_history(self, card_number):
        """查看交易记录"""
        from views.dialogs import TransactionHistoryDialog
        dialog = TransactionHistoryDialog(self.account_controller, card_number, self)
        dialog.exec_()
    
    def handle_logout(self):
        """处理退出登录"""
        reply = QMessageBox.question(
            self, '确认', '确定要退出登录吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.user_controller.logout()
            if success:
                QMessageBox.information(self, "成功", message)
                self.logout_signal.emit()
                self.close()
            else:
                QMessageBox.warning(self, "警告", message)
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        reply = QMessageBox.question(
            self, '确认退出', '确定要退出系统吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

