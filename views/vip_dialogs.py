"""
VIP用户专属对话框 - VIP Dialogs
提供VIP用户专属功能：财务统计、账单导出、收藏收款人、定期存款等
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QComboBox, QLineEdit, QTabWidget,
                            QWidget, QHeaderView, QGroupBox, QTextEdit,
                            QDateEdit, QDoubleSpinBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta


class VIPCenterDialog(QDialog):
    """VIP专属中心对话框"""
    
    def __init__(self, user_controller, account_controller, current_user, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.account_controller = account_controller
        self.current_user = current_user
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("👑 VIP专属中心")
        self.setFixedSize(1100, 700)
        
        # 样式
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFD700, stop:1 #FFF8DC);
            }
            QPushButton#primary_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFD700, stop:1 #FFA500);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#primary_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFA500, stop:1 #FF8C00);
            }
            QPushButton#secondary_btn {
                background: #f0f0f0;
                color: #333;
                border: 1px solid #ddd;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton#secondary_btn:hover {
                background: #e0e0e0;
            }
        """)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # VIP等级显示
        vip_level = self.current_user.get('vip_level', 1)  # 默认为1级
        if vip_level is None or vip_level == 0:
            vip_level = 1
        title_label = QLabel(f"👑 VIP专属中心 - VIP {vip_level} 级")
        title_label.setStyleSheet("""
            font-size: 26px; 
            font-weight: bold; 
            color: #B8860B;
            background: white;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #FFD700;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #FFD700;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #FFF8DC;
                color: #333;
                padding: 12px 25px;
                margin-right: 3px;
                border: 2px solid #FFD700;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                color: #B8860B;
            }
            QTabBar::tab:hover {
                background: #FFE4B5;
            }
        """)
        
        # 1. 财务统计
        stats_tab = self.create_stats_tab()
        tab_widget.addTab(stats_tab, "📊 财务统计")
        
        # 2. 账单导出
        export_tab = self.create_export_tab()
        tab_widget.addTab(export_tab, "📄 账单导出")
        
        # 3. 快速转账
        quick_transfer_tab = self.create_quick_transfer_tab()
        tab_widget.addTab(quick_transfer_tab, "⚡ 快速转账")
        
        # 4. VIP特权
        privilege_tab = self.create_privilege_tab()
        tab_widget.addTab(privilege_tab, "💎 VIP特权")
        
        main_layout.addWidget(tab_widget)
        
        # 底部按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.setObjectName("secondary_btn")
        close_btn.clicked.connect(self.close)
        close_btn.setMinimumWidth(120)
        bottom_layout.addWidget(close_btn)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # 居中显示
        self.center_window()
    
    def create_stats_tab(self):
        """创建财务统计选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 时间范围选择
        time_group = QGroupBox("📅 选择统计时间范围")
        time_layout = QHBoxLayout()
        
        QLabel_start = QLabel("开始日期:")
        time_layout.addWidget(QLabel_start)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        time_layout.addWidget(self.start_date)
        
        time_layout.addSpacing(20)
        
        QLabel_end = QLabel("结束日期:")
        time_layout.addWidget(QLabel_end)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        time_layout.addWidget(self.end_date)
        
        time_layout.addSpacing(20)
        
        query_btn = QPushButton("🔍 查询统计")
        query_btn.setObjectName("primary_btn")
        query_btn.clicked.connect(self.load_financial_stats)
        time_layout.addWidget(query_btn)
        
        time_layout.addStretch()
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # 统计结果显示
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #FFD700;
                border-radius: 5px;
                padding: 15px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.stats_display)
        
        widget.setLayout(layout)
        
        # 显示初始提示
        self.stats_display.setHtml("""
            <p style='color: #666; text-align: center; margin-top: 50px; font-size: 14px;'>
                请选择时间范围后点击"🔍 查询统计"按钮查看财务数据
            </p>
        """)
        
        return widget
    
    def create_export_tab(self):
        """创建账单导出选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 说明
        info_label = QLabel("📄 导出账单功能可以将您的交易记录导出为Excel或PDF格式")
        info_label.setStyleSheet("font-size: 14px; color: #666; padding: 10px;")
        layout.addWidget(info_label)
        
        # 导出选项
        export_group = QGroupBox("导出设置")
        export_layout = QVBoxLayout()
        
        # 格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel("导出格式:")
        format_layout.addWidget(format_label)
        
        self.export_format = QComboBox()
        self.export_format.addItems(["Excel (*.xlsx)", "PDF (*.pdf)", "CSV (*.csv)"])
        self.export_format.setMinimumWidth(200)
        format_layout.addWidget(self.export_format)
        format_layout.addStretch()
        
        export_layout.addLayout(format_layout)
        
        # 时间范围
        date_layout = QHBoxLayout()
        date_label = QLabel("时间范围:")
        date_layout.addWidget(date_label)
        
        self.export_start_date = QDateEdit()
        self.export_start_date.setDate(QDate.currentDate().addMonths(-3))
        self.export_start_date.setCalendarPopup(True)
        self.export_start_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.export_start_date)
        
        date_layout.addWidget(QLabel("至"))
        
        self.export_end_date = QDateEdit()
        self.export_end_date.setDate(QDate.currentDate())
        self.export_end_date.setCalendarPopup(True)
        self.export_end_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.export_end_date)
        date_layout.addStretch()
        
        export_layout.addLayout(date_layout)
        
        # 导出按钮
        export_btn = QPushButton("📥 导出账单")
        export_btn.setObjectName("primary_btn")
        export_btn.clicked.connect(self.export_bill)
        export_btn.setMinimumHeight(45)
        export_layout.addWidget(export_btn)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # 历史导出记录
        history_group = QGroupBox("导出历史")
        history_layout = QVBoxLayout()
        
        self.export_history = QListWidget()
        self.export_history.addItem("🕐 暂无导出记录")
        history_layout.addWidget(self.export_history)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_quick_transfer_tab(self):
        """创建快速转账选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 说明
        info_label = QLabel("⚡ 收藏常用收款人，实现一键快速转账")
        info_label.setStyleSheet("font-size: 14px; color: #666; padding: 10px;")
        layout.addWidget(info_label)
        
        # 收款人列表
        payee_group = QGroupBox("常用收款人")
        payee_layout = QVBoxLayout()
        
        self.payee_list = QListWidget()
        self.payee_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #FFD700;
                border-radius: 5px;
                background: white;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background: #FFF8DC;
            }
            QListWidget::item:selected {
                background: #FFE4B5;
                color: #333;
            }
        """)
        self.load_favorite_payees()
        payee_layout.addWidget(self.payee_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ 添加收款人")
        add_btn.setObjectName("primary_btn")
        add_btn.clicked.connect(self.add_favorite_payee)
        btn_layout.addWidget(add_btn)
        
        transfer_btn = QPushButton("💸 快速转账")
        transfer_btn.setObjectName("primary_btn")
        transfer_btn.clicked.connect(self.quick_transfer_to_payee)
        btn_layout.addWidget(transfer_btn)
        
        remove_btn = QPushButton("🗑️ 删除")
        remove_btn.setObjectName("secondary_btn")
        remove_btn.clicked.connect(self.remove_favorite_payee)
        btn_layout.addWidget(remove_btn)
        
        payee_layout.addLayout(btn_layout)
        payee_group.setLayout(payee_layout)
        layout.addWidget(payee_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_privilege_tab(self):
        """创建VIP特权选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # VIP等级信息
        vip_level = self.current_user.get('vip_level', 0)
        
        level_label = QLabel(f"当前等级：VIP {vip_level} 级")
        level_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #B8860B;
            padding: 15px;
            background: white;
            border: 2px solid #FFD700;
            border-radius: 10px;
        """)
        level_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(level_label)
        
        # VIP特权列表
        privilege_text = QTextEdit()
        privilege_text.setReadOnly(True)
        privilege_text.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 20px;
                font-size: 14px;
            }
        """)
        
        privileges_html = f"""
        <div style="line-height: 2.0;">
        <h2 style="color: #B8860B; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">💎 您的VIP特权</h2>
        
        <h3 style="color: #FF8C00; margin-top: 20px;">✅ 基础特权（所有VIP）</h3>
        <ul style="font-size: 14px;">
            <li><b>⚡ 更高转账限额:</b> 单笔限额 ¥50,000（普通用户仅 ¥10,000）</li>
            <li><b>📊 财务统计分析:</b> 查看详细的收支统计和趋势分析</li>
            <li><b>📄 账单导出功能:</b> 支持导出Excel、PDF、CSV格式账单</li>
            <li><b>⚡ 快速转账:</b> 收藏常用收款人，一键快速转账</li>
            <li><b>👑 专属标识:</b> 金色VIP图标，彰显尊贵身份</li>
        </ul>
        
        <h3 style="color: #FF8C00; margin-top: 20px;">🎁 等级特权</h3>
        <ul style="font-size: 14px;">
            <li><b>VIP 1:</b> 基础财务统计图表</li>
            <li><b>VIP 2:</b> 定期存款功能，享受更高利率</li>
            <li><b>VIP 3:</b> 自定义主题，个性化界面</li>
            <li><b>VIP 4:</b> 交易分类管理，智能标签</li>
            <li><b>VIP 5:</b> 完整财务分析报告，AI理财建议</li>
        </ul>
        
        <h3 style="color: #FF8C00; margin-top: 20px;">📈 当前等级：VIP {vip_level}</h3>
        <p style="font-size: 14px; color: #666;">
        {'<b style="color: #4CAF50;">🎉 恭喜！您已享有上述 VIP ' + str(vip_level) + ' 级的所有特权！</b>' if vip_level > 0 else '<b style="color: #999;">💡 提示：升级VIP等级可解锁更多特权功能</b>'}
        </p>
        
        <h3 style="color: #FF8C00; margin-top: 20px;">💰 专属优惠</h3>
        <ul style="font-size: 14px;">
            <li>存款利率上浮 <b style="color: #4CAF50;">+0.5%</b></li>
            <li>转账手续费减免 <b style="color: #4CAF50;">50%</b></li>
            <li>每月赠送 <b style="color: #4CAF50;">3次</b> 跨行转账免手续费</li>
        </ul>
        
        <p style="margin-top: 30px; text-align: center; font-size: 16px; color: #B8860B; font-weight: bold;">
        🌟 感谢您选择我们的VIP服务！🌟
        </p>
        </div>
        """
        
        privilege_text.setHtml(privileges_html)
        layout.addWidget(privilege_text)
        
        widget.setLayout(layout)
        return widget
    
    def load_financial_stats(self):
        """加载财务统计"""
        try:
            username = self.current_user.get('username', '')
            if not username:
                self.stats_display.setHtml("<p style='color: red;'>错误：无法获取用户名</p>")
                return
            
            start_date_str = self.start_date.date().toString("yyyy-MM-dd")
            end_date_str = self.end_date.date().toString("yyyy-MM-dd")
            
            # 获取所有账户
            accounts = self.account_controller.data_manager.get_accounts_by_username(username)
            
            if not accounts:
                self.stats_display.setHtml("<p style='color: #999; text-align: center; margin-top: 50px;'>暂无账户数据</p>")
                return
            
            # 统计数据
            total_balance = sum(float(acc.get('balance', 0)) for acc in accounts)
            account_count = len(accounts)
            
            # 获取交易记录（简化处理，获取所有账户的交易）
            total_deposit = 0
            total_withdraw = 0
            total_transfer_out = 0
            total_transfer_in = 0
            transaction_count = 0
            
            for account in accounts:
                card_number = account.get('card_number', '')
                transactions = self.account_controller.data_manager.get_transactions(card_number)
                
                for trans in transactions:
                    transaction_count += 1
                    trans_type = trans.get('transaction_type', '')
                    amount = float(trans.get('amount', 0))
                    
                    if trans_type == 'deposit':
                        total_deposit += amount
                    elif trans_type == 'withdraw':
                        total_withdraw += amount
                    elif trans_type == 'transfer_out':
                        total_transfer_out += amount
                    elif trans_type == 'transfer_in':
                        total_transfer_in += amount
            
            # 生成统计报告
            stats_html = f"""
            <div style="line-height: 2.0;">
            <h2 style="color: #B8860B; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">📊 财务统计报告</h2>
            <p style="color: #666; font-size: 13px;">统计时间：{start_date_str} 至 {end_date_str}</p>
            
            <h3 style="color: #FF8C00; margin-top: 25px;">💰 资产概况</h3>
            <ul style="font-size: 14px;">
                <li><b>账户总数:</b> {account_count} 个</li>
                <li><b>总余额:</b> <span style="color: #4CAF50; font-size: 18px; font-weight: bold;">¥{total_balance:,.2f}</span></li>
                <li><b>平均余额:</b> ¥{(total_balance / account_count if account_count > 0 else 0):,.2f}</li>
            </ul>
            
            <h3 style="color: #FF8C00; margin-top: 25px;">📈 交易统计</h3>
            <ul style="font-size: 14px;">
                <li><b>交易总笔数:</b> {transaction_count} 笔</li>
                <li><b>存款总额:</b> <span style="color: #4CAF50;">¥{total_deposit:,.2f}</span></li>
                <li><b>取款总额:</b> <span style="color: #F44336;">¥{total_withdraw:,.2f}</span></li>
                <li><b>转出总额:</b> <span style="color: #2196F3;">¥{total_transfer_out:,.2f}</span></li>
                <li><b>转入总额:</b> <span style="color: #4CAF50;">¥{total_transfer_in:,.2f}</span></li>
            </ul>
            
            <h3 style="color: #FF8C00; margin-top: 25px;">💡 财务分析</h3>
            <ul style="font-size: 14px;">
                <li><b>净流入:</b> <span style="color: {'#4CAF50' if (total_deposit + total_transfer_in - total_withdraw - total_transfer_out) >= 0 else '#F44336'};">¥{(total_deposit + total_transfer_in - total_withdraw - total_transfer_out):,.2f}</span></li>
                <li><b>资金活跃度:</b> {'高' if transaction_count > 10 else '中' if transaction_count > 5 else '低'}</li>
            </ul>
            </div>
            """
            
            self.stats_display.setHtml(stats_html)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载财务统计失败：{str(e)}")
    
    def export_bill(self):
        """导出账单"""
        format_text = self.export_format.currentText()
        start_date = self.export_start_date.date().toString("yyyy-MM-dd")
        end_date = self.export_end_date.date().toString("yyyy-MM-dd")
        
        QMessageBox.information(
            self,
            "提示",
            f"账单导出功能开发中...\n\n"
            f"导出格式：{format_text}\n"
            f"时间范围：{start_date} 至 {end_date}\n\n"
            f"此功能将在下一版本中实现。"
        )
    
    def load_favorite_payees(self):
        """加载常用收款人"""
        self.payee_list.clear()
        self.payee_list.addItem("💡 暂无常用收款人，点击下方按钮添加")
        # TODO: 从数据库加载收款人列表
    
    def add_favorite_payee(self):
        """添加收款人"""
        QMessageBox.information(self, "提示", "添加收款人功能开发中，将在下一版本实现")
    
    def quick_transfer_to_payee(self):
        """快速转账给选中的收款人"""
        if not self.payee_list.currentItem():
            QMessageBox.warning(self, "提示", "请先选择收款人")
            return
        QMessageBox.information(self, "提示", "快速转账功能开发中，将在下一版本实现")
    
    def remove_favorite_payee(self):
        """删除收款人"""
        if not self.payee_list.currentItem():
            QMessageBox.warning(self, "提示", "请先选择要删除的收款人")
            return
        QMessageBox.information(self, "提示", "删除功能开发中，将在下一版本实现")
    
    def center_window(self):
        """窗口居中显示"""
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

