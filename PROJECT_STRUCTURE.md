# 项目结构说明

## 完整的文件结构

```
F:\bank_system\
│
├── models/                          # 模型层（Model）
│   ├── __init__.py                 # 模型模块初始化
│   ├── user.py                     # 用户数据模型
│   └── account.py                  # 账户数据模型
│
├── views/                           # 视图层（View）
│   ├── __init__.py                 # 视图模块初始化
│   └── main_view.py                # 主视图（包含所有UI交互）
│
├── controllers/                     # 控制器层（Controller）
│   ├── __init__.py                 # 控制器模块初始化
│   ├── user_controller.py          # 用户业务逻辑控制器
│   └── account_controller.py       # 账户业务逻辑控制器
│
├── utils/                           # 工具类
│   ├── __init__.py                 # 工具模块初始化
│   └── data_manager.py             # 数据持久化管理器
│
├── data/                            # 数据存储目录（运行时自动创建）
│   ├── users.json                  # 用户数据文件
│   └── accounts.json               # 账户数据文件
│
├── main.py                          # 主程序入口
├── README.md                        # 项目说明文档
├── USAGE.md                         # 使用指南
├── PROJECT_STRUCTURE.md             # 项目结构说明（本文件）
├── requirements.txt                 # 项目依赖
└── .gitignore                       # Git忽略文件
```

## 模块说明

### 1. Models（模型层）

#### user.py - 用户模型
- **User类**：定义用户数据结构和基本操作
- 属性：username, password, real_name, id_card, phone, email, created_at, is_active
- 方法：
  - `_hash_password()`: 密码加密（SHA256）
  - `verify_password()`: 密码验证
  - `to_dict()`: 对象序列化
  - `from_dict()`: 对象反序列化

#### account.py - 账户模型
- **Account类**：定义银行账户数据结构和业务方法
- 属性：card_number, username, balance, status, created_at, transaction_history
- 状态常量：STATUS_NORMAL, STATUS_FROZEN, STATUS_LOST, STATUS_CLOSED
- 方法：
  - `deposit()`: 存款
  - `withdraw()`: 取款
  - `get_balance()`: 查询余额
  - `freeze()/unfreeze()`: 冻结/解冻
  - `report_loss()/cancel_loss()`: 挂失/解除挂失
  - `close_account()`: 销户
  - `_add_transaction()`: 添加交易记录
  - `get_transaction_history()`: 获取交易历史

### 2. Views（视图层）

#### main_view.py - 主视图
- **MainView类**：负责所有用户界面展示和交互
- 静态方法（无需实例化）：
  - `show_welcome()`: 显示欢迎界面
  - `show_main_menu()`: 主菜单（未登录）
  - `show_user_menu()`: 用户菜单（已登录）
  - `show_user_management_menu()`: 用户管理菜单
  - `show_transaction_menu()`: 存取款管理菜单
  - `show_account_management_menu()`: 账户管理菜单
  - `get_input()`: 获取用户输入
  - `show_message()`: 显示消息
  - `pause()`: 等待用户按键
  - `confirm()`: 确认对话框
  - `show_user_info()`: 显示用户信息
  - `show_accounts()`: 显示账户列表
  - `show_transaction_history()`: 显示交易记录

### 3. Controllers（控制器层）

#### user_controller.py - 用户控制器
- **UserController类**：处理用户相关业务逻辑
- 方法：
  - `register()`: 用户注册
  - `login()`: 用户登录
  - `logout()`: 用户登出
  - `is_logged_in()`: 检查登录状态
  - `get_current_user()`: 获取当前用户
  - `update_user_info()`: 更新用户信息
  - `get_user_info()`: 获取用户信息
  - `change_password()`: 修改密码

#### account_controller.py - 账户控制器
- **AccountController类**：处理账户相关业务逻辑
- 方法：
  - `create_account()`: 开户
  - `get_my_accounts()`: 获取当前用户所有账户
  - `get_account_by_card()`: 根据卡号获取账户
  - `deposit()`: 存款
  - `withdraw()`: 取款
  - `check_balance()`: 查询余额
  - `freeze_account()/unfreeze_account()`: 冻结/解冻账户
  - `report_loss()/cancel_loss()`: 挂失/解除挂失
  - `close_account()`: 销户
  - `get_transaction_history()`: 获取交易历史

### 4. Utils（工具类）

#### data_manager.py - 数据管理器
- **DataManager类**：负责数据持久化
- 数据存储格式：JSON
- 方法：
  - `load_users()/save_users()`: 加载/保存用户数据
  - `load_accounts()/save_accounts()`: 加载/保存账户数据
  - `add_user()/update_user()/get_user()`: 用户CRUD操作
  - `add_account()/update_account()/get_account()`: 账户CRUD操作
  - `user_exists()`: 检查用户是否存在
  - `get_accounts_by_username()`: 获取用户的所有账户

### 5. Main（主程序）

#### main.py - 程序入口
- **BankSystem类**：系统主类，协调MVC三层
- 方法：
  - `run()`: 运行系统主循环
  - `show_main_menu()/show_user_menu()`: 显示菜单
  - `register()/login()/logout()`: 用户认证
  - `user_management()`: 用户管理
  - `transaction_management()`: 存取款管理
  - `account_management()`: 账户管理
  - 以及各种具体业务操作方法

## MVC架构说明

### Model（模型）
- 职责：定义数据结构，封装数据操作
- 特点：独立于界面，可复用
- 文件：`models/user.py`, `models/account.py`

### View（视图）
- 职责：用户界面展示，获取用户输入
- 特点：不包含业务逻辑，只负责显示
- 文件：`views/main_view.py`

### Controller（控制器）
- 职责：业务逻辑处理，协调Model和View
- 特点：接收用户输入，调用Model处理，更新View
- 文件：`controllers/user_controller.py`, `controllers/account_controller.py`

## 数据流向

```
用户操作
   ↓
View (获取输入)
   ↓
Controller (处理逻辑)
   ↓
Model (数据操作)
   ↓
DataManager (持久化)
   ↓
JSON文件
```

## 面向对象设计特点

1. **封装**：每个类都有明确的职责，数据和方法封装在一起
2. **继承**：未来可扩展（如VIPUser继承User）
3. **多态**：通过接口统一调用（如不同账户类型）
4. **单一职责**：每个类只负责一个功能模块
5. **依赖注入**：AccountController依赖UserController

## 设计模式

1. **MVC模式**：分离界面、业务逻辑、数据
2. **工厂模式**：from_dict()方法创建对象
3. **单例模式**：DataManager管理全局数据

## 如何运行

在项目根目录（F:\bank_system）执行：
```bash
python main.py
```

就这么简单！

