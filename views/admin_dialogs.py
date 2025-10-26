"""
管理员专用对话框 - Admin Dialogs
提供管理员专属功能：用户管理、账户管理、交易查询、系统统计
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QComboBox, QLineEdit, QTabWidget,
                            QWidget, QHeaderView, QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime


class AdminPanelDialog(QDialog):
    """管理员控制面板主对话框"""
    
    def __init__(self, user_controller, account_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.account_controller = account_controller
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔧 管理员控制面板")
        self.setFixedSize(1100, 700)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #1976D2;
            }
            QTabBar::tab:hover {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
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
            QPushButton#danger_btn {
                background-color: #F44336;
                color: white;
            }
            QPushButton#danger_btn:hover {
                background-color: #D32F2F;
            }
            QPushButton#success_btn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#success_btn:hover {
                background-color: #45a049;
            }
            QPushButton#warning_btn {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#warning_btn:hover {
                background-color: #F57C00;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("🔧 管理员控制面板")
        title_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #FF5722; 
            padding: 10px;
            margin-bottom: 15px;
        """)
        main_layout.addWidget(title_label)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                color: #333;
                padding: 10px 20px;
                margin-right: 5px;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #FF5722;
                border-bottom: 2px solid #FF5722;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
        """)
        
        # 1. 用户管理选项卡
        user_tab = self.create_user_management_tab()
        tab_widget.addTab(user_tab, "👥 用户管理")
        
        # 2. 账户管理选项卡
        account_tab = self.create_account_management_tab()
        tab_widget.addTab(account_tab, "💳 账户管理")
        
        # 3. 交易查询选项卡
        transaction_tab = self.create_transaction_query_tab()
        tab_widget.addTab(transaction_tab, "📊 交易查询")
        
        # 4. 系统统计选项卡
        stats_tab = self.create_system_stats_tab()
        tab_widget.addTab(stats_tab, "📈 系统统计")
        
        main_layout.addWidget(tab_widget)
        
        # 底部按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.setObjectName("danger_btn")
        close_btn.clicked.connect(self.close)
        close_btn.setMinimumWidth(120)
        bottom_layout.addWidget(close_btn)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # 居中显示
        self.center_window()
    
    def create_user_management_tab(self):
        """创建用户管理选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部操作栏
        top_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self.refresh_user_table)
        top_layout.addWidget(refresh_btn)
        
        top_layout.addStretch()
        
        # 搜索框
        search_label = QLabel("搜索用户:")
        top_layout.addWidget(search_label)
        
        self.user_search_input = QLineEdit()
        self.user_search_input.setPlaceholderText("输入用户名或真实姓名")
        self.user_search_input.setMinimumWidth(200)
        self.user_search_input.textChanged.connect(self.filter_users)
        top_layout.addWidget(self.user_search_input)
        
        layout.addLayout(top_layout)
        
        # 用户列表表格
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)
        self.user_table.setHorizontalHeaderLabels(['用户名', '真实姓名', '身份证号', '手机号', '角色', '注册时间', '操作'])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.user_table.setColumnWidth(0, 120)
        self.user_table.setColumnWidth(1, 100)
        self.user_table.setColumnWidth(2, 150)
        self.user_table.setColumnWidth(3, 120)
        self.user_table.setColumnWidth(4, 100)
        self.user_table.setColumnWidth(5, 180)
        
        layout.addWidget(self.user_table)
        
        # 加载用户数据
        self.refresh_user_table()
        
        widget.setLayout(layout)
        return widget
    
    def create_account_management_tab(self):
        """创建账户管理选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部操作栏
        top_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self.refresh_account_table)
        top_layout.addWidget(refresh_btn)
        
        top_layout.addStretch()
        
        # 搜索框
        search_label = QLabel("搜索账户:")
        top_layout.addWidget(search_label)
        
        self.account_search_input = QLineEdit()
        self.account_search_input.setPlaceholderText("输入卡号或用户名")
        self.account_search_input.setMinimumWidth(200)
        self.account_search_input.textChanged.connect(self.filter_accounts)
        top_layout.addWidget(self.account_search_input)
        
        layout.addLayout(top_layout)
        
        # 账户列表表格
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(6)
        self.account_table.setHorizontalHeaderLabels(['卡号', '所属用户', '余额 (元)', '状态', '开户时间', '操作'])
        self.account_table.horizontalHeader().setStretchLastSection(True)
        self.account_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.account_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.account_table.setAlternatingRowColors(True)
        self.account_table.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.account_table.setColumnWidth(0, 200)
        self.account_table.setColumnWidth(1, 120)
        self.account_table.setColumnWidth(2, 150)
        self.account_table.setColumnWidth(3, 100)
        self.account_table.setColumnWidth(4, 180)
        
        layout.addWidget(self.account_table)
        
        # 加载账户数据
        self.refresh_account_table()
        
        widget.setLayout(layout)
        return widget
    
    def create_transaction_query_tab(self):
        """创建交易查询选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部操作栏
        top_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self.refresh_transaction_table)
        top_layout.addWidget(refresh_btn)
        
        top_layout.addStretch()
        
        # 交易类型筛选
        filter_label = QLabel("交易类型:")
        top_layout.addWidget(filter_label)
        
        self.transaction_type_filter = QComboBox()
        self.transaction_type_filter.addItems(['全部', '存款', '取款', '转账', '开户'])
        self.transaction_type_filter.currentTextChanged.connect(self.filter_transactions)
        top_layout.addWidget(self.transaction_type_filter)
        
        # 搜索框
        search_label = QLabel("搜索:")
        top_layout.addWidget(search_label)
        
        self.transaction_search_input = QLineEdit()
        self.transaction_search_input.setPlaceholderText("输入卡号")
        self.transaction_search_input.setMinimumWidth(200)
        self.transaction_search_input.textChanged.connect(self.filter_transactions)
        top_layout.addWidget(self.transaction_search_input)
        
        layout.addLayout(top_layout)
        
        # 交易记录表格
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(6)
        self.transaction_table.setHorizontalHeaderLabels(['卡号', '交易类型', '金额 (元)', '余额 (元)', '交易时间', '备注'])
        self.transaction_table.horizontalHeader().setStretchLastSection(True)
        self.transaction_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.transaction_table.setColumnWidth(0, 200)
        self.transaction_table.setColumnWidth(1, 100)
        self.transaction_table.setColumnWidth(2, 120)
        self.transaction_table.setColumnWidth(3, 120)
        self.transaction_table.setColumnWidth(4, 180)
        
        layout.addWidget(self.transaction_table)
        
        # 加载交易数据
        self.refresh_transaction_table()
        
        widget.setLayout(layout)
        return widget
    
    def create_system_stats_tab(self):
        """创建系统统计选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新统计数据")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self.refresh_system_stats)
        layout.addWidget(refresh_btn)
        
        # 统计信息显示区域
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                font-family: 'Microsoft YaHei', 'SimHei', monospace;
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        layout.addWidget(self.stats_text)
        
        # 加载统计数据
        self.refresh_system_stats()
        
        widget.setLayout(layout)
        return widget
    
    # ==================== 用户管理功能 ====================
    
    def refresh_user_table(self):
        """刷新用户表格"""
        try:
            # 获取所有用户（使用列表格式）
            users = self.user_controller.data_manager.get_all_users_list()
            self.all_users = users  # 保存所有用户数据用于筛选
            
            self.display_users(users)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载用户数据失败：{str(e)}")
    
    def display_users(self, users):
        """显示用户列表"""
        self.user_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # 用户名
            username_item = QTableWidgetItem(user['username'])
            username_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 0, username_item)
            
            # 真实姓名
            real_name_item = QTableWidgetItem(user['real_name'])
            real_name_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 1, real_name_item)
            
            # 身份证号
            id_card_item = QTableWidgetItem(user['id_card'])
            id_card_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 2, id_card_item)
            
            # 手机号
            phone_item = QTableWidgetItem(user['phone'])
            phone_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 3, phone_item)
            
            # 角色
            role = user.get('role', 'normal')
            from utils.permission_manager import PermissionManager
            role_name = PermissionManager.get_role_name(role)
            role_item = QTableWidgetItem(role_name)
            role_item.setTextAlignment(Qt.AlignCenter)
            
            # 根据角色设置颜色
            if role == 'admin':
                role_item.setForeground(Qt.red)
            elif role == 'vip':
                role_item.setForeground(Qt.darkYellow)
            else:
                role_item.setForeground(Qt.darkGreen)
            
            self.user_table.setItem(row, 4, role_item)
            
            # 注册时间 - 优先使用 created_time
            created_time = user.get('created_time') or user.get('created_at', '未知')
            if created_time and created_time != '未知':
                if isinstance(created_time, str):
                    time_str = created_time
                else:
                    time_str = created_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                time_str = '未知'
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 5, time_item)
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(5, 2, 5, 2)
            btn_layout.setSpacing(5)
            
            # 修改角色按钮
            role_btn = QPushButton("修改角色")
            role_btn.setObjectName("warning_btn")
            role_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
            role_btn.setCursor(Qt.PointingHandCursor)
            role_btn.clicked.connect(lambda checked, u=user: self.change_user_role(u))
            btn_layout.addWidget(role_btn)
            
            btn_widget.setLayout(btn_layout)
            self.user_table.setCellWidget(row, 6, btn_widget)
    
    def filter_users(self):
        """筛选用户"""
        if not hasattr(self, 'all_users'):
            return
        
        search_text = self.user_search_input.text().lower()
        
        if not search_text:
            self.display_users(self.all_users)
            return
        
        # 筛选用户
        filtered_users = [
            user for user in self.all_users
            if search_text in str(user.get('username', '')).lower() or 
               search_text in str(user.get('real_name', '')).lower()
        ]
        
        self.display_users(filtered_users)
    
    def center_window(self):
        """窗口居中显示"""
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def change_user_role(self, user_dict):
        """修改用户角色"""
        from PyQt5.QtWidgets import QInputDialog
        from utils.permission_manager import PermissionManager
        
        current_role = user_dict.get('role', 'normal')
        current_role_name = PermissionManager.get_role_name(current_role)
        
        # 角色选择
        roles = ['普通用户', 'VIP用户', '管理员']
        role_map = {
            '普通用户': 'normal',
            'VIP用户': 'vip',
            '管理员': 'admin'
        }
        
        new_role_name, ok = QInputDialog.getItem(
            self,
            "修改用户角色",
            f"用户 {user_dict['username']} ({user_dict['real_name']})\n当前角色：{current_role_name}\n\n请选择新角色：",
            roles,
            0,
            False
        )
        
        if ok and new_role_name:
            new_role = role_map[new_role_name]
            
            # 确认修改
            reply = QMessageBox.question(
                self,
                "确认修改",
                f"确定要将用户 {user_dict['username']} 的角色从 {current_role_name} 修改为 {new_role_name} 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    # 更新用户角色
                    user_dict['role'] = new_role
                    self.user_controller.data_manager.update_user(user_dict['username'], user_dict)
                    
                    QMessageBox.information(self, "成功", f"用户 {user_dict['username']} 的角色已修改为 {new_role_name}")
                    self.refresh_user_table()
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"修改角色失败：{str(e)}")
    
    # ==================== 账户管理功能 ====================
    
    def refresh_account_table(self):
        """刷新账户表格"""
        try:
            # 获取所有账户（转换为列表）
            accounts_dict = self.account_controller.data_manager.load_accounts()
            # 将字典转换为列表
            accounts = list(accounts_dict.values()) if isinstance(accounts_dict, dict) else accounts_dict
            self.all_accounts = accounts  # 保存所有账户数据用于筛选
            
            self.display_accounts(accounts)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载账户数据失败：{str(e)}")
    
    def display_accounts(self, accounts):
        """显示账户列表"""
        self.account_table.setRowCount(len(accounts))
        
        for row, account in enumerate(accounts):
            # 卡号
            card_item = QTableWidgetItem(account['card_number'])
            card_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 0, card_item)
            
            # 所属用户
            username_item = QTableWidgetItem(account['username'])
            username_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 1, username_item)
            
            # 余额
            balance_item = QTableWidgetItem(f"{account['balance']:.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.account_table.setItem(row, 2, balance_item)
            
            # 状态
            status_item = QTableWidgetItem(account['status'])
            status_item.setTextAlignment(Qt.AlignCenter)
            if account['status'] == '正常':
                status_item.setForeground(Qt.darkGreen)
            elif account['status'] == '冻结':
                status_item.setForeground(Qt.blue)
            else:
                status_item.setForeground(Qt.red)
            self.account_table.setItem(row, 3, status_item)
            
            # 开户时间 - 优先使用 created_time
            created_time = account.get('created_time') or account.get('created_at', '未知')
            if created_time and created_time != '未知':
                if isinstance(created_time, str):
                    time_str = created_time
                else:
                    time_str = created_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                time_str = '未知'
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 4, time_item)
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(5, 2, 5, 2)
            btn_layout.setSpacing(5)
            
            # 查看交易记录按钮
            view_btn = QPushButton("交易记录")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            view_btn.setCursor(Qt.PointingHandCursor)
            view_btn.clicked.connect(lambda checked, cn=account['card_number']: self.view_account_transactions(cn))
            btn_layout.addWidget(view_btn)
            
            btn_widget.setLayout(btn_layout)
            self.account_table.setCellWidget(row, 5, btn_widget)
    
    def filter_accounts(self):
        """筛选账户"""
        if not hasattr(self, 'all_accounts'):
            return
        
        search_text = self.account_search_input.text().lower()
        
        if not search_text:
            self.display_accounts(self.all_accounts)
            return
        
        # 筛选账户
        filtered_accounts = [
            account for account in self.all_accounts
            if search_text in account['card_number'].lower() or search_text in account['username'].lower()
        ]
        
        self.display_accounts(filtered_accounts)
    
    def view_account_transactions(self, card_number):
        """查看账户交易记录"""
        from views.dialogs import TransactionHistoryDialog
        dialog = TransactionHistoryDialog(self.account_controller, card_number, self)
        dialog.exec_()
    
    # ==================== 交易查询功能 ====================
    
    def refresh_transaction_table(self):
        """刷新交易表格"""
        try:
            # 获取所有交易记录
            transactions = self.account_controller.data_manager.get_all_transactions()
            self.all_transactions = transactions  # 保存所有交易数据用于筛选
            
            self.display_transactions(transactions)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载交易数据失败：{str(e)}")
    
    def display_transactions(self, transactions):
        """显示交易记录"""
        self.transaction_table.setRowCount(len(transactions))
        
        for row, trans in enumerate(transactions):
            # 卡号
            card_item = QTableWidgetItem(trans['card_number'])
            card_item.setTextAlignment(Qt.AlignCenter)
            self.transaction_table.setItem(row, 0, card_item)
            
            # 交易类型
            type_item = QTableWidgetItem(trans['transaction_type'])
            type_item.setTextAlignment(Qt.AlignCenter)
            # 根据类型设置颜色
            if trans['transaction_type'] in ['存款', '开户']:
                type_item.setForeground(Qt.darkGreen)
            elif trans['transaction_type'] == '取款':
                type_item.setForeground(Qt.darkRed)
            else:
                type_item.setForeground(Qt.darkBlue)
            self.transaction_table.setItem(row, 1, type_item)
            
            # 金额
            amount_item = QTableWidgetItem(f"{trans['amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 2, amount_item)
            
            # 余额
            balance_item = QTableWidgetItem(f"{trans['balance_after']:.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 3, balance_item)
            
            # 交易时间
            time_item = QTableWidgetItem(trans['transaction_time'])
            time_item.setTextAlignment(Qt.AlignCenter)
            self.transaction_table.setItem(row, 4, time_item)
            
            # 备注
            remark = trans.get('remark', '')
            remark_item = QTableWidgetItem(remark)
            self.transaction_table.setItem(row, 5, remark_item)
    
    def filter_transactions(self):
        """筛选交易记录"""
        if not hasattr(self, 'all_transactions'):
            return
        
        search_text = self.transaction_search_input.text().lower()
        trans_type = self.transaction_type_filter.currentText()
        
        # 筛选
        filtered = self.all_transactions
        
        # 按类型筛选
        if trans_type != '全部':
            filtered = [t for t in filtered if t['transaction_type'] == trans_type]
        
        # 按卡号搜索
        if search_text:
            filtered = [t for t in filtered if search_text in t['card_number'].lower()]
        
        self.display_transactions(filtered)
    
    # ==================== 系统统计功能 ====================
    
    def refresh_system_stats(self):
        """刷新系统统计数据"""
        try:
            # 获取统计数据
            users_dict = self.user_controller.data_manager.load_users()
            accounts_dict = self.account_controller.data_manager.load_accounts()
            transactions = self.account_controller.data_manager.get_all_transactions()
            
            # 转换为列表
            users = list(users_dict.values()) if isinstance(users_dict, dict) else users_dict
            accounts = list(accounts_dict.values()) if isinstance(accounts_dict, dict) else accounts_dict
            
            # 统计各类数据
            total_users = len(users)
            normal_users = sum(1 for u in users if u.get('role', 'normal') == 'normal')
            vip_users = sum(1 for u in users if u.get('role', 'normal') == 'vip')
            admin_users = sum(1 for u in users if u.get('role', 'normal') == 'admin')
            
            total_accounts = len(accounts)
            # 状态可能是英文（active）或中文（正常）
            active_accounts = sum(1 for a in accounts if a.get('status', '') in ['active', '正常'])
            frozen_accounts = sum(1 for a in accounts if a.get('status', '') in ['frozen', '冻结'])
            
            total_balance = sum(float(a.get('balance', 0)) for a in accounts)
            
            total_transactions = len(transactions)
            # 交易类型可能是英文或中文
            deposit_count = sum(1 for t in transactions if t.get('transaction_type', '') in ['deposit', '存款'])
            withdraw_count = sum(1 for t in transactions if t.get('transaction_type', '') in ['withdraw', '取款'])
            transfer_count = sum(1 for t in transactions if 'transfer' in t.get('transaction_type', '') or '转账' in t.get('transaction_type', ''))
            
            total_deposit = sum(float(t.get('amount', 0)) for t in transactions if t.get('transaction_type', '') in ['deposit', '存款'])
            total_withdraw = sum(float(t.get('amount', 0)) for t in transactions if t.get('transaction_type', '') in ['withdraw', '取款'])
            
            # 构建统计报告
            stats_html = f"""
            <div style="line-height: 2.0;">
            <h2 style="color: #1976D2; border-bottom: 2px solid #1976D2; padding-bottom: 10px;">📊 系统数据统计报告</h2>
            
            <h3 style="color: #4CAF50; margin-top: 25px;">👥 用户统计</h3>
            <ul style="font-size: 14px;">
                <li><b>用户总数:</b> {total_users} 人</li>
                <li><b>普通用户:</b> {normal_users} 人</li>
                <li><b>VIP用户:</b> {vip_users} 人</li>
                <li><b>管理员:</b> {admin_users} 人</li>
            </ul>
            
            <h3 style="color: #FF9800; margin-top: 25px;">💳 账户统计</h3>
            <ul style="font-size: 14px;">
                <li><b>账户总数:</b> {total_accounts} 个</li>
                <li><b>正常账户:</b> {active_accounts} 个</li>
                <li><b>冻结账户:</b> {frozen_accounts} 个</li>
                <li><b>系统总资金:</b> <span style="color: #F44336; font-size: 16px; font-weight: bold;">¥{total_balance:,.2f}</span></li>
                <li><b>平均账户余额:</b> ¥{(total_balance / total_accounts if total_accounts > 0 else 0):,.2f}</li>
            </ul>
            
            <h3 style="color: #2196F3; margin-top: 25px;">📈 交易统计</h3>
            <ul style="font-size: 14px;">
                <li><b>交易总笔数:</b> {total_transactions} 笔</li>
                <li><b>存款笔数:</b> {deposit_count} 笔</li>
                <li><b>取款笔数:</b> {withdraw_count} 笔</li>
                <li><b>转账笔数:</b> {transfer_count} 笔</li>
                <li><b>累计存款:</b> <span style="color: #4CAF50;">¥{total_deposit:,.2f}</span></li>
                <li><b>累计取款:</b> <span style="color: #F44336;">¥{total_withdraw:,.2f}</span></li>
            </ul>
            
            <h3 style="color: #9C27B0; margin-top: 25px;">⏰ 系统信息</h3>
            <ul style="font-size: 14px;">
                <li><b>统计时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><b>系统版本:</b> v4.0 (管理员功能版)</li>
                <li><b>数据库:</b> MySQL</li>
            </ul>
            </div>
            """
            
            self.stats_text.setHtml(stats_html)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载统计数据失败：{str(e)}")

