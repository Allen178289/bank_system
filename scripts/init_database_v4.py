"""
数据库初始化脚本 v4.0
用于创建/升级数据库表结构以支持v4.0所有新功能
"""
import mysql.connector
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DB_CONFIG


# 建表SQL语句 v4.0
CREATE_TABLES_SQL = """
-- 创建数据库
CREATE DATABASE IF NOT EXISTS bank_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE bank_system;

-- 用户表（新增角色、VIP等级等字段）
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码',
    real_name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    id_card VARCHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    phone VARCHAR(11) NOT NULL COMMENT '手机号',
    email VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    role VARCHAR(20) DEFAULT 'normal' COMMENT '角色(normal/vip/admin)',
    vip_level INT DEFAULT 0 COMMENT 'VIP等级(0-5)',
    theme VARCHAR(20) DEFAULT 'light' COMMENT '主题(light/dark)',
    language VARCHAR(10) DEFAULT 'zh_CN' COMMENT '语言(zh_CN/en_US)',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    last_login_time DATETIME DEFAULT NULL COMMENT '最后登录时间',
    INDEX idx_id_card (id_card),
    INDEX idx_phone (phone),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 银行账户表（新增定期存款、利率等字段）
CREATE TABLE IF NOT EXISTS accounts (
    card_number VARCHAR(20) PRIMARY KEY COMMENT '银行卡号',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    account_type VARCHAR(20) NOT NULL COMMENT '账户类型(savings/credit/fixed)',
    account_name VARCHAR(100) DEFAULT NULL COMMENT '账户名称(用户自定义)',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '账户余额',
    credit_limit DECIMAL(15, 2) DEFAULT 0.00 COMMENT '信用额度(仅信用卡)',
    interest_rate DECIMAL(5, 4) DEFAULT 0.0000 COMMENT '利率(年利率)',
    maturity_date DATE DEFAULT NULL COMMENT '到期日(定期存款)',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '账户状态(active/frozen/lost/closed)',
    daily_limit DECIMAL(15, 2) DEFAULT 50000.00 COMMENT '每日交易限额',
    monthly_limit DECIMAL(15, 2) DEFAULT 500000.00 COMMENT '每月交易限额',
    is_favorite BOOLEAN DEFAULT FALSE COMMENT '是否为收藏账户',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    INDEX idx_username (username),
    INDEX idx_status (status),
    INDEX idx_account_type (account_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='银行账户表';

-- 交易记录表（新增分类、转账对方等字段）
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '交易ID',
    card_number VARCHAR(20) NOT NULL COMMENT '银行卡号',
    transaction_type VARCHAR(20) NOT NULL COMMENT '交易类型(deposit/withdraw/transfer_out/transfer_in)',
    category VARCHAR(50) DEFAULT 'other' COMMENT '交易分类(income/expense/transfer/other)',
    subcategory VARCHAR(50) DEFAULT NULL COMMENT '交易子分类',
    amount DECIMAL(15, 2) NOT NULL COMMENT '交易金额',
    balance_after DECIMAL(15, 2) NOT NULL COMMENT '交易后余额',
    related_card VARCHAR(20) DEFAULT NULL COMMENT '关联卡号(转账对方)',
    description VARCHAR(200) DEFAULT NULL COMMENT '交易描述',
    transaction_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '交易时间',
    can_cancel BOOLEAN DEFAULT TRUE COMMENT '是否可撤销',
    is_cancelled BOOLEAN DEFAULT FALSE COMMENT '是否已撤销',
    cancelled_time DATETIME DEFAULT NULL COMMENT '撤销时间',
    FOREIGN KEY (card_number) REFERENCES accounts(card_number) ON DELETE CASCADE,
    INDEX idx_card_number (card_number),
    INDEX idx_transaction_time (transaction_time),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_category (category),
    INDEX idx_related_card (related_card)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录表';

-- 交易分类表
CREATE TABLE IF NOT EXISTS transaction_categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
    category_type VARCHAR(20) NOT NULL COMMENT '分类类型(income/expense)',
    icon VARCHAR(50) DEFAULT NULL COMMENT '图标',
    color VARCHAR(20) DEFAULT NULL COMMENT '颜色',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_system BOOLEAN DEFAULT FALSE COMMENT '是否系统分类',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易分类表';

-- 常用收款人表
CREATE TABLE IF NOT EXISTS favorite_payees (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    payee_card VARCHAR(20) NOT NULL COMMENT '收款人卡号',
    payee_name VARCHAR(100) NOT NULL COMMENT '收款人姓名',
    alias VARCHAR(100) DEFAULT NULL COMMENT '备注名',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='常用收款人表';

-- 账单表
CREATE TABLE IF NOT EXISTS bills (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '账单ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    bill_type VARCHAR(20) NOT NULL COMMENT '账单类型(monthly/yearly)',
    year INT NOT NULL COMMENT '年份',
    month INT DEFAULT NULL COMMENT '月份(月账单)',
    total_income DECIMAL(15, 2) DEFAULT 0.00 COMMENT '总收入',
    total_expense DECIMAL(15, 2) DEFAULT 0.00 COMMENT '总支出',
    transaction_count INT DEFAULT 0 COMMENT '交易笔数',
    health_score INT DEFAULT 0 COMMENT '财务健康评分',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    UNIQUE KEY unique_bill (username, bill_type, year, month),
    INDEX idx_username (username),
    INDEX idx_year_month (year, month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='账单表';

-- 系统日志表（管理员功能）
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    username VARCHAR(50) DEFAULT NULL COMMENT '用户名',
    action VARCHAR(100) NOT NULL COMMENT '操作',
    details TEXT DEFAULT NULL COMMENT '详情',
    ip_address VARCHAR(45) DEFAULT NULL COMMENT 'IP地址',
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '日志时间',
    INDEX idx_username (username),
    INDEX idx_log_time (log_time),
    INDEX idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统日志表';
"""

# 初始化默认数据
INSERT_DEFAULT_DATA = """
USE bank_system;

-- 插入默认交易分类
INSERT IGNORE INTO transaction_categories (category_name, category_type, icon, color, sort_order, is_system) VALUES
('工资收入', 'income', '💰', '#4CAF50', 1, TRUE),
('投资收入', 'income', '📈', '#8BC34A', 2, TRUE),
('其他收入', 'income', '💵', '#CDDC39', 3, TRUE),
('餐饮美食', 'expense', '🍔', '#F44336', 1, TRUE),
('购物消费', 'expense', '🛒', '#E91E63', 2, TRUE),
('交通出行', 'expense', '🚗', '#9C27B0', 3, TRUE),
('住房物业', 'expense', '🏠', '#673AB7', 4, TRUE),
('医疗健康', 'expense', '💊', '#3F51B5', 5, TRUE),
('教育培训', 'expense', '📚', '#2196F3', 6, TRUE),
('娱乐休闲', 'expense', '🎮', '#03A9F4', 7, TRUE),
('通讯费用', 'expense', '📱', '#00BCD4', 8, TRUE),
('其他支出', 'expense', '💳', '#009688', 9, TRUE);
"""


def init_database():
    """初始化数据库"""
    print("开始初始化数据库 v4.0...")
    print("=" * 60)
    
    try:
        # 连接MySQL（不指定数据库）
        conn_config = DB_CONFIG.copy()
        db_name = conn_config.pop('database')
        
        conn = mysql.connector.connect(**conn_config)
        cursor = conn.cursor()
        
        print("\n📊 创建/更新表结构...")
        # 执行建表SQL
        for statement in CREATE_TABLES_SQL.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    # 只显示CREATE TABLE的语句
                    if 'CREATE TABLE' in statement.upper():
                        table_name = statement.split('CREATE TABLE')[1].split('IF NOT EXISTS')[1].split('(')[0].strip()
                        print(f"  ✓ 表 {table_name} 已创建/更新")
                except mysql.connector.Error as err:
                    if "already exists" in str(err).lower() or "duplicate column" in str(err).lower():
                        pass  # 忽略已存在的错误
                    else:
                        print(f"  ⚠ 警告: {err}")
        
        print("\n📝 插入默认数据...")
        # 插入默认数据
        for statement in INSERT_DEFAULT_DATA.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if cursor.rowcount > 0:
                        print(f"  ✓ 已插入 {cursor.rowcount} 条记录")
                except mysql.connector.Error as err:
                    if "duplicate" not in str(err).lower():
                        print(f"  ⚠ 警告: {err}")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ 数据库 v4.0 初始化成功！")
        print("=" * 60)
        print(f"\n数据库名称: {db_name}")
        print("\n已创建/更新的表:")
        print("  ✓ users              - 用户表（新增角色、VIP等级等）")
        print("  ✓ accounts           - 银行账户表（新增定期存款、限额等）")
        print("  ✓ transactions       - 交易记录表（新增分类、撤销等）")
        print("  ✓ transaction_categories - 交易分类表（新）")
        print("  ✓ favorite_payees    - 常用收款人表（新）")
        print("  ✓ bills              - 账单表（新）")
        print("  ✓ system_logs        - 系统日志表（新）")
        
        print("\n✨ v4.0 新功能支持:")
        print("  • 角色权限系统（普通/VIP/管理员）")
        print("  • 定期存款和利率计算")
        print("  • 转账功能")
        print("  • 交易分类和搜索")
        print("  • 交易限额管理")
        print("  • 交易撤销功能")
        print("  • 常用收款人")
        print("  • 月度/年度账单")
        print("  • 主题和多语言")
        print("  • 系统日志")
        
    except mysql.connector.Error as err:
        print(f"\n❌ 数据库初始化失败: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return True


def check_and_upgrade():
    """检查并升级现有数据库"""
    print("\n🔍 检查现有数据库...")
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 检查users表是否有role字段
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        has_role = cursor.fetchone() is not None
        
        if not has_role:
            print("  ⚡ 检测到旧版数据库，开始升级...")
            
            # 添加新字段到users表
            upgrade_sqls = [
                "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'normal' COMMENT '角色' AFTER email",
                "ALTER TABLE users ADD COLUMN vip_level INT DEFAULT 0 COMMENT 'VIP等级' AFTER role",
                "ALTER TABLE users ADD COLUMN theme VARCHAR(20) DEFAULT 'light' COMMENT '主题' AFTER vip_level",
                "ALTER TABLE users ADD COLUMN language VARCHAR(10) DEFAULT 'zh_CN' COMMENT '语言' AFTER theme",
                "ALTER TABLE users ADD COLUMN last_login_time DATETIME DEFAULT NULL COMMENT '最后登录时间' AFTER updated_time",
            ]
            
            for sql in upgrade_sqls:
                try:
                    cursor.execute(sql)
                    print(f"    ✓ 已添加字段")
                except mysql.connector.Error:
                    pass  # 字段可能已存在
            
            conn.commit()
            print("  ✅ 数据库升级完成！")
        else:
            print("  ✓ 数据库已是最新版本")
        
    except mysql.connector.Error as err:
        print(f"  ⚠ 检查失败: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    print("=" * 60)
    print(" 银行卡管理系统 v4.0 - 数据库初始化/升级工具")
    print("=" * 60)
    print()
    
    # 显示配置信息
    print("数据库配置:")
    print(f"  主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print()
    
    # 确认
    print("此脚本将:")
    print("  1. 创建新的表结构（如果不存在）")
    print("  2. 升级现有表（添加新字段）")
    print("  3. 插入默认数据")
    print()
    
    confirm = input("确认要执行吗？(输入 yes 继续): ")
    if confirm.lower() == 'yes':
        # 先尝试升级
        check_and_upgrade()
        # 然后初始化
        init_database()
    else:
        print("已取消操作。")

