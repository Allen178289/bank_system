"""
数据库初始化脚本
用于创建数据库表结构
"""
import mysql.connector
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DB_CONFIG


# 建表SQL语句
CREATE_TABLES_SQL = """
-- 创建数据库
CREATE DATABASE IF NOT EXISTS bank_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE bank_system;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码',
    real_name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    id_card VARCHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    phone VARCHAR(11) NOT NULL COMMENT '手机号',
    email VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_id_card (id_card),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 银行账户表
CREATE TABLE IF NOT EXISTS accounts (
    card_number VARCHAR(20) PRIMARY KEY COMMENT '银行卡号',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    account_type VARCHAR(20) NOT NULL COMMENT '账户类型(储蓄卡/信用卡)',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT '账户余额',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '账户状态(active/frozen/closed)',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    INDEX idx_username (username),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='银行账户表';

-- 交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '交易ID',
    card_number VARCHAR(20) NOT NULL COMMENT '银行卡号',
    transaction_type VARCHAR(20) NOT NULL COMMENT '交易类型(deposit/withdraw/transfer)',
    amount DECIMAL(15, 2) NOT NULL COMMENT '交易金额',
    balance_after DECIMAL(15, 2) NOT NULL COMMENT '交易后余额',
    description VARCHAR(200) DEFAULT NULL COMMENT '交易描述',
    transaction_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '交易时间',
    FOREIGN KEY (card_number) REFERENCES accounts(card_number) ON DELETE CASCADE,
    INDEX idx_card_number (card_number),
    INDEX idx_transaction_time (transaction_time),
    INDEX idx_transaction_type (transaction_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录表';
"""


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    try:
        # 连接MySQL（不指定数据库）
        conn_config = DB_CONFIG.copy()
        db_name = conn_config.pop('database')
        
        conn = mysql.connector.connect(**conn_config)
        cursor = conn.cursor()
        
        # 执行每条SQL语句
        for statement in CREATE_TABLES_SQL.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"✓ 执行成功")
                except mysql.connector.Error as err:
                    # 如果表已存在，跳过错误
                    if "already exists" in str(err).lower():
                        print(f"✓ 表已存在，跳过")
                    else:
                        raise
        
        conn.commit()
        print("\n✅ 数据库初始化成功！")
        print(f"数据库名称: {db_name}")
        print("已创建的表:")
        print("  - users (用户表)")
        print("  - accounts (银行账户表)")
        print("  - transactions (交易记录表)")
        
    except mysql.connector.Error as err:
        print(f"\n❌ 数据库初始化失败: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("银行卡管理系统 - 数据库初始化")
    print("=" * 60)
    print()
    
    # 显示配置信息
    print("数据库配置:")
    print(f"  主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print()
    
    # 确认
    confirm = input("确认要初始化数据库吗？(输入 yes 继续): ")
    if confirm.lower() == 'yes':
        init_database()
    else:
        print("已取消操作。")

