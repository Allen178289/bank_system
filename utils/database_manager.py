"""
数据库管理器 - Database Manager
负责数据的持久化存储和读取（使用MySQL数据库）
"""
import mysql.connector
from mysql.connector import pooling
import json
from datetime import datetime
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DB_CONFIG, POOL_CONFIG


class DatabaseManager:
    """数据库管理器类"""
    
    _pool = None
    
    def __init__(self):
        """初始化数据库管理器"""
        if DatabaseManager._pool is None:
            try:
                # 强制使用纯Python实现，避免C扩展与PyQt冲突
                config_with_pure_python = DB_CONFIG.copy()
                config_with_pure_python['use_pure'] = True  # 关键：使用纯Python实现
                
                pool_config = POOL_CONFIG.copy()
                
                # 创建连接池
                DatabaseManager._pool = pooling.MySQLConnectionPool(
                    **config_with_pure_python,
                    **pool_config
                )
                print("数据库连接池创建成功！")
            except mysql.connector.Error as err:
                print(f"数据库连接失败: {err}")
                raise
    
    def get_connection(self):
        """从连接池获取连接"""
        try:
            return self._pool.get_connection()
        except mysql.connector.Error as err:
            print(f"获取数据库连接失败: {err}")
            raise
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """
        执行SQL查询
        :param query: SQL语句
        :param params: 参数
        :param fetch_one: 是否只获取一条记录
        :param fetch_all: 是否获取所有记录
        :return: 查询结果
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            print(f"SQL执行错误: {err}")
            print(f"SQL语句: {query}")
            print(f"参数: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    # ==================== 用户相关操作 ====================
    
    def add_user(self, user_dict):
        """添加用户"""
        query = """
        INSERT INTO users (username, password, real_name, id_card, phone, email, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user_dict['username'],
            user_dict['password'],
            user_dict['real_name'],
            user_dict['id_card'],
            user_dict['phone'],
            user_dict.get('email'),
            user_dict.get('role', 'normal')  # 默认为普通用户
        )
        self.execute_query(query, params)
    
    def update_user(self, username, user_dict):
        """更新用户信息"""
        query = """
        UPDATE users 
        SET password=%s, real_name=%s, id_card=%s, phone=%s, email=%s, role=%s
        WHERE username=%s
        """
        params = (
            user_dict['password'],
            user_dict['real_name'],
            user_dict['id_card'],
            user_dict['phone'],
            user_dict.get('email'),
            user_dict.get('role', 'normal'),
            username
        )
        return self.execute_query(query, params) > 0
    
    def get_user(self, username):
        """获取用户"""
        query = "SELECT * FROM users WHERE username=%s"
        return self.execute_query(query, (username,), fetch_one=True)
    
    def user_exists(self, username):
        """检查用户是否存在"""
        query = "SELECT COUNT(*) as count FROM users WHERE username=%s"
        result = self.execute_query(query, (username,), fetch_one=True)
        return result['count'] > 0
    
    def load_users(self):
        """加载所有用户（为兼容性保留）"""
        query = "SELECT * FROM users"
        users_list = self.execute_query(query, fetch_all=True)
        # 转换为字典格式以兼容原代码
        return {user['username']: dict(user) for user in users_list}
    
    def get_all_users_list(self):
        """获取所有用户列表（管理员功能）"""
        query = "SELECT * FROM users ORDER BY created_time DESC"
        users_list = self.execute_query(query, fetch_all=True)
        # 返回列表格式
        return [dict(user) for user in users_list]
    
    def save_users(self, users_dict):
        """保存所有用户（为兼容性保留，实际不需要批量保存）"""
        pass
    
    # ==================== 账户相关操作 ====================
    
    def add_account(self, account_dict):
        """添加账户"""
        # 如果有创建时间，则使用提供的时间，否则数据库会自动使用当前时间
        if 'created_at' in account_dict:
            query = """
            INSERT INTO accounts (card_number, username, account_type, balance, status, created_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # 转换 created_at 字符串为 datetime
            created_time = account_dict['created_at']
            if isinstance(created_time, str):
                from datetime import datetime
                try:
                    created_time = datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
                except:
                    created_time = None
            
            params = (
                account_dict['card_number'],
                account_dict['username'],
                account_dict['account_type'],
                account_dict['balance'],
                account_dict.get('status', 'active'),
                created_time
            )
        else:
            query = """
            INSERT INTO accounts (card_number, username, account_type, balance, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                account_dict['card_number'],
                account_dict['username'],
                account_dict['account_type'],
                account_dict['balance'],
                account_dict.get('status', 'active')
            )
        self.execute_query(query, params)
        
        # 如果有初始交易记录，也要保存
        if 'transaction_history' in account_dict and account_dict['transaction_history']:
            for trans in account_dict['transaction_history']:
                self.add_transaction(
                    account_dict['card_number'],
                    trans['type'],
                    trans['amount'],
                    trans['balance_after'],
                    trans.get('description', ''),
                    trans.get('time')
                )
    
    def update_account(self, card_number, account_dict):
        """更新账户信息"""
        query = """
        UPDATE accounts 
        SET username=%s, account_type=%s, balance=%s, status=%s
        WHERE card_number=%s
        """
        params = (
            account_dict['username'],
            account_dict['account_type'],
            account_dict['balance'],
            account_dict.get('status', 'active'),
            card_number
        )
        result = self.execute_query(query, params) > 0
        
        # 检查是否有新的交易记录需要保存
        if 'transaction_history' in account_dict and account_dict['transaction_history']:
            # 获取数据库中已有的交易记录数量
            existing_transactions = self.get_transactions(card_number)
            existing_count = len(existing_transactions)
            new_transactions = account_dict['transaction_history']
            
            # 如果新的交易记录数量大于已有的，说明有新交易需要保存
            if len(new_transactions) > existing_count:
                # transaction_history 中的交易是按时间顺序排列的，最新的在末尾
                # 保存新增的交易记录（从 existing_count 开始到末尾）
                for i in range(existing_count, len(new_transactions)):
                    trans = new_transactions[i]
                    self.add_transaction(
                        card_number,
                        trans['type'],
                        trans['amount'],
                        trans['balance_after'],
                        trans.get('description', ''),
                        trans.get('time')
                    )
        
        return result
    
    def get_account(self, card_number):
        """获取账户（包含交易记录）"""
        query = "SELECT * FROM accounts WHERE card_number=%s"
        account = self.execute_query(query, (card_number,), fetch_one=True)
        
        if account:
            account = dict(account)
            # 将数据库的 created_time 映射为 Account 模型的 created_at
            if 'created_time' in account:
                account['created_at'] = account['created_time'].strftime('%Y-%m-%d %H:%M:%S') if account['created_time'] else None
                del account['created_time']
            # 获取交易记录（使用 transaction_history 键名以匹配 Account 模型）
            account['transaction_history'] = self.get_transactions(card_number)
        
        return account
    
    def get_accounts_by_username(self, username):
        """获取用户的所有账户"""
        query = "SELECT * FROM accounts WHERE username=%s"
        accounts = self.execute_query(query, (username,), fetch_all=True)
        
        # 为每个账户添加交易记录（使用 transaction_history 键名以匹配 Account 模型）
        result = []
        for account in accounts:
            account = dict(account)
            # 将数据库的 created_time 映射为 Account 模型的 created_at
            if 'created_time' in account:
                account['created_at'] = account['created_time'].strftime('%Y-%m-%d %H:%M:%S') if account['created_time'] else None
                del account['created_time']
            account['transaction_history'] = self.get_transactions(account['card_number'])
            result.append(account)
        
        return result
    
    def delete_account(self, card_number):
        """删除账户"""
        query = "DELETE FROM accounts WHERE card_number=%s"
        return self.execute_query(query, (card_number,)) > 0
    
    def load_accounts(self):
        """加载所有账户（为兼容性保留）"""
        query = "SELECT * FROM accounts"
        accounts_list = self.execute_query(query, fetch_all=True)
        
        # 转换为字典格式以兼容原代码
        accounts_dict = {}
        for account in accounts_list:
            account = dict(account)
            # 将数据库的 created_time 映射为 Account 模型的 created_at
            if 'created_time' in account:
                account['created_at'] = account['created_time'].strftime('%Y-%m-%d %H:%M:%S') if account['created_time'] else None
                del account['created_time']
            account['transaction_history'] = self.get_transactions(account['card_number'])
            accounts_dict[account['card_number']] = account
        
        return accounts_dict
    
    def save_accounts(self, accounts_dict):
        """保存所有账户（为兼容性保留，实际不需要批量保存）"""
        pass
    
    # ==================== 交易记录相关操作 ====================
    
    def add_transaction(self, card_number, trans_type, amount, balance_after, description='', trans_time=None):
        """添加交易记录"""
        query = """
        INSERT INTO transactions (card_number, transaction_type, amount, balance_after, description, transaction_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        if trans_time is None:
            trans_time = datetime.now()
        elif isinstance(trans_time, str):
            # 如果是字符串格式的时间，转换为datetime
            try:
                trans_time = datetime.strptime(trans_time, '%Y-%m-%d %H:%M:%S')
            except:
                trans_time = datetime.now()
        
        params = (card_number, trans_type, amount, balance_after, description, trans_time)
        self.execute_query(query, params)
    
    def get_transactions(self, card_number, limit=None):
        """获取账户的交易记录"""
        if limit:
            query = """
            SELECT * FROM transactions 
            WHERE card_number=%s 
            ORDER BY transaction_time ASC 
            LIMIT %s
            """
            params = (card_number, limit)
        else:
            query = """
            SELECT * FROM transactions 
            WHERE card_number=%s 
            ORDER BY transaction_time ASC
            """
            params = (card_number,)
        
        transactions = self.execute_query(query, params, fetch_all=True)
        
        # 转换为兼容原格式的字典列表（按时间升序，最新的在末尾）
        result = []
        for trans in transactions:
            result.append({
                'type': trans['transaction_type'],
                'amount': float(trans['amount']),
                'balance_after': float(trans['balance_after']),
                'description': trans['description'] or '',
                'time': trans['transaction_time'].strftime('%Y-%m-%d %H:%M:%S') if trans['transaction_time'] else ''
            })
        
        return result
    
    def get_all_transactions(self, limit=None):
        """获取所有交易记录（管理员功能）"""
        if limit:
            query = """
            SELECT t.*, a.username 
            FROM transactions t
            LEFT JOIN accounts a ON t.card_number = a.card_number
            ORDER BY t.transaction_time DESC 
            LIMIT %s
            """
            params = (limit,)
        else:
            query = """
            SELECT t.*, a.username 
            FROM transactions t
            LEFT JOIN accounts a ON t.card_number = a.card_number
            ORDER BY t.transaction_time DESC
            """
            params = ()
        
        transactions = self.execute_query(query, params, fetch_all=True)
        
        # 转换为字典列表（按时间降序，最新的在前面）
        result = []
        for trans in transactions:
            result.append({
                'card_number': trans['card_number'],
                'username': trans.get('username', '未知'),
                'transaction_type': trans['transaction_type'],
                'amount': float(trans['amount']),
                'balance_after': float(trans['balance_after']),
                'transaction_time': trans['transaction_time'].strftime('%Y-%m-%d %H:%M:%S') if trans['transaction_time'] else '',
                'remark': trans.get('description', '')
            })
        
        return result
    
    # ==================== VIP用户相关操作 ====================
    
    def get_user_financial_summary(self, username):
        """获取用户的财务汇总信息"""
        summary = {
            'total_balance': 0.0,
            'total_deposit': 0.0,
            'total_withdraw': 0.0,
            'total_transfer_out': 0.0,
            'total_transfer_in': 0.0,
            'total_transactions': 0
        }
        
        # 获取用户所有账户
        accounts = self.get_accounts_by_username(username)
        if not accounts:
            return summary
        
        card_numbers = [acc['card_number'] for acc in accounts]
        
        # 计算总余额
        for acc in accounts:
            summary['total_balance'] += float(acc.get('balance', 0.0))
        
        # 获取所有相关交易
        for card_number in card_numbers:
            transactions = self.get_transactions(card_number)
            for trans in transactions:
                summary['total_transactions'] += 1
                amount = float(trans.get('amount', 0.0))
                trans_type = trans.get('transaction_type', '')
                
                if trans_type == 'deposit':
                    summary['total_deposit'] += amount
                elif trans_type == 'withdraw':
                    summary['total_withdraw'] += amount
                elif trans_type == 'transfer':
                    # 转账都算作转出
                    summary['total_transfer_out'] += amount
        
        return summary
    
    def get_user_transactions(self, username, limit=None):
        """获取指定用户的所有交易记录"""
        # 先获取用户的所有账户
        accounts = self.get_accounts_by_username(username)
        if not accounts:
            return []
        
        card_numbers = [acc['card_number'] for acc in accounts]
        
        # 构建查询语句
        placeholders = ','.join(['%s'] * len(card_numbers))
        query = f"""
        SELECT * FROM transactions 
        WHERE card_number IN ({placeholders})
        ORDER BY transaction_time DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        transactions = self.execute_query(query, tuple(card_numbers), fetch_all=True)
        
        # 格式化交易记录
        formatted_transactions = []
        for trans in transactions:
            trans_dict = dict(trans)
            # 处理时间格式
            if 'transaction_time' in trans_dict and trans_dict['transaction_time']:
                if isinstance(trans_dict['transaction_time'], datetime):
                    trans_dict['transaction_time'] = trans_dict['transaction_time'].strftime('%Y-%m-%d %H:%M:%S')
            # 处理金额
            if 'amount' in trans_dict:
                trans_dict['amount'] = float(trans_dict['amount'])
            if 'balance_after' in trans_dict:
                trans_dict['balance_after'] = float(trans_dict['balance_after'])
            formatted_transactions.append(trans_dict)
        
        return formatted_transactions
    
    def get_user_favorite_payees(self, username):
        """获取用户的常用收款人列表"""
        # 由于我们还没有favorite_payees表，先返回空列表
        # TODO: 需要创建favorite_payees表
        return []
    
    def add_favorite_payee(self, username, payee_card_number, alias):
        """添加常用收款人"""
        # 由于我们还没有favorite_payees表，先返回提示信息
        # TODO: 需要创建favorite_payees表
        return False, "常用收款人功能即将推出，敬请期待！"
    
    def close(self):
        """关闭连接池（通常在应用退出时调用）"""
        # MySQL连接池会自动管理连接，这里不需要显式关闭
        pass

