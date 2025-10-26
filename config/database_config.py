"""
数据库配置 - Database Configuration
"""

# MySQL数据库配置
DB_CONFIG = {
    'host': 'localhost',      # 数据库服务器地址
    'port': 3306,             # 数据库端口
    'user': 'root',           # 数据库用户名
    'password': '123456',  # 数据库密码（请修改为您的实际密码）
    'database': 'bank_system',    # 数据库名称
    'charset': 'utf8mb4',
    'autocommit': True
}

# 连接池配置
POOL_CONFIG = {
    'pool_name': 'bank_pool',
    'pool_size': 5,
    'pool_reset_session': True
}

