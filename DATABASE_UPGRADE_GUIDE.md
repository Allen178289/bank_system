# 数据库升级指南

## 📋 升级步骤

### 1. 安装MySQL数据库

如果您还没有安装MySQL，请先安装：

**Windows:**
- 下载MySQL安装包: https://dev.mysql.com/downloads/mysql/
- 运行安装程序并设置root密码

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### 2. 安装Python依赖

```bash
# 激活虚拟环境
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 安装MySQL驱动
pip install mysql-connector-python
```

### 3. 配置数据库连接

编辑 `config/database_config.py` 文件，修改数据库配置：

```python
DB_CONFIG = {
    'host': 'localhost',        # 数据库服务器地址
    'port': 3306,               # 数据库端口
    'user': 'root',             # 数据库用户名
    'password': 'your_password',# ⚠️ 修改为您的实际密码
    'database': 'bank_system',  # 数据库名称
    'charset': 'utf8mb4',
    'autocommit': True
}
```

### 4. 初始化数据库表结构

运行数据库初始化脚本：

```bash
python scripts/init_database.py
```

这将自动创建：
- `bank_system` 数据库
- `users` 表（用户信息）
- `accounts` 表（银行账户）
- `transactions` 表（交易记录）

### 5. 迁移现有数据（可选）

如果您之前使用JSON文件存储数据，可以将数据迁移到数据库：

```bash
python scripts/migrate_to_database.py
```

这将把 `data/users.json` 和 `data/accounts.json` 中的数据导入到MySQL数据库。

### 6. 切换到数据库版本

修改相关控制器文件，将数据管理器从 `DataManager` 改为 `DatabaseManager`：

**修改 `controllers/user_controller.py`：**
```python
# 旧版本
from utils.data_manager import DataManager

# 新版本
from utils.database_manager import DatabaseManager as DataManager
```

**修改 `controllers/account_controller.py`：**
```python
# 旧版本
from utils.data_manager import DataManager

# 新版本
from utils.database_manager import DatabaseManager as DataManager
```

### 7. 测试运行

```bash
python main_gui.py
```

---

## 🗄️ 数据库表结构

### users 表（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| username | VARCHAR(50) | 用户名（主键） |
| password | VARCHAR(255) | 密码 |
| real_name | VARCHAR(50) | 真实姓名 |
| id_card | VARCHAR(18) | 身份证号（唯一） |
| phone | VARCHAR(11) | 手机号 |
| email | VARCHAR(100) | 邮箱 |
| created_time | DATETIME | 创建时间 |
| updated_time | DATETIME | 更新时间 |

### accounts 表（银行账户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| card_number | VARCHAR(20) | 银行卡号（主键） |
| username | VARCHAR(50) | 用户名（外键） |
| account_type | VARCHAR(20) | 账户类型 |
| balance | DECIMAL(15,2) | 账户余额 |
| status | VARCHAR(20) | 账户状态 |
| created_time | DATETIME | 创建时间 |
| updated_time | DATETIME | 更新时间 |

### transactions 表（交易记录表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 交易ID（主键，自增） |
| card_number | VARCHAR(20) | 银行卡号（外键） |
| transaction_type | VARCHAR(20) | 交易类型 |
| amount | DECIMAL(15,2) | 交易金额 |
| balance_after | DECIMAL(15,2) | 交易后余额 |
| description | VARCHAR(200) | 交易描述 |
| transaction_time | DATETIME | 交易时间 |

---

## ⚠️ 注意事项

1. **备份数据**: 升级前请备份 `data/users.json` 和 `data/accounts.json` 文件
2. **密码安全**: 请在 `database_config.py` 中使用强密码
3. **兼容性**: 数据库版本完全兼容原JSON版本的功能
4. **性能提升**: 数据库版本在大数据量时性能更好
5. **并发支持**: 数据库版本支持多用户并发访问

---

## 🔧 常见问题

### Q1: 连接数据库失败

**A:** 请检查：
- MySQL服务是否启动
- `database_config.py` 中的配置是否正确
- 用户名密码是否正确
- 是否安装了 `mysql-connector-python`

### Q2: 表已存在错误

**A:** 这是正常的，初始化脚本会自动跳过已存在的表

### Q3: 数据迁移失败

**A:** 请确保：
- 已经运行过数据库初始化脚本
- JSON文件格式正确
- 数据库用户有写入权限

### Q4: 想要回退到JSON版本

**A:** 只需将控制器中的导入语句改回：
```python
from utils.data_manager import DataManager
```

---

## 📞 技术支持

如有问题，请查看项目文档或提交Issue。

---

**升级完成后，您的银行卡管理系统将使用MySQL数据库存储数据！** 🎉

