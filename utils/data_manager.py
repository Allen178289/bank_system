"""
数据管理器 - Data Manager
负责数据的持久化存储和读取（使用JSON文件）
"""
import json
import os


class DataManager:
    """数据管理器类"""
    
    def __init__(self, data_dir='data'):
        """
        初始化数据管理器
        :param data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.accounts_file = os.path.join(data_dir, 'accounts.json')
        
        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # 确保数据文件存在
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        
        if not os.path.exists(self.accounts_file):
            self._save_json(self.accounts_file, {})
    
    @staticmethod
    def _load_json(file_path):
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    @staticmethod
    def _save_json(file_path, data):
        """保存JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_users(self):
        """加载所有用户数据"""
        return self._load_json(self.users_file)
    
    def save_users(self, users_dict):
        """保存所有用户数据"""
        self._save_json(self.users_file, users_dict)
    
    def load_accounts(self):
        """加载所有账户数据"""
        return self._load_json(self.accounts_file)
    
    def save_accounts(self, accounts_dict):
        """保存所有账户数据"""
        self._save_json(self.accounts_file, accounts_dict)
    
    def add_user(self, user_dict):
        """添加用户"""
        users = self.load_users()
        users[user_dict['username']] = user_dict
        self.save_users(users)
    
    def update_user(self, username, user_dict):
        """更新用户信息"""
        users = self.load_users()
        if username in users:
            users[username] = user_dict
            self.save_users(users)
            return True
        return False
    
    def get_user(self, username):
        """获取用户"""
        users = self.load_users()
        return users.get(username)
    
    def user_exists(self, username):
        """检查用户是否存在"""
        users = self.load_users()
        return username in users
    
    def add_account(self, account_dict):
        """添加账户"""
        accounts = self.load_accounts()
        accounts[account_dict['card_number']] = account_dict
        self.save_accounts(accounts)
    
    def update_account(self, card_number, account_dict):
        """更新账户信息"""
        accounts = self.load_accounts()
        if card_number in accounts:
            accounts[card_number] = account_dict
            self.save_accounts(accounts)
            return True
        return False
    
    def get_account(self, card_number):
        """获取账户"""
        accounts = self.load_accounts()
        return accounts.get(card_number)
    
    def get_accounts_by_username(self, username):
        """获取用户的所有账户"""
        accounts = self.load_accounts()
        return [acc for acc in accounts.values() if acc['username'] == username]
    
    def delete_account(self, card_number):
        """删除账户"""
        accounts = self.load_accounts()
        if card_number in accounts:
            del accounts[card_number]
            self.save_accounts(accounts)
            return True
        return False

