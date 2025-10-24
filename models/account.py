"""
账户模型 - Account Model
负责银行账户数据的定义和基本操作
"""
import random
from datetime import datetime


class Account:
    """银行账户类"""
    
    # 账户状态
    STATUS_NORMAL = "正常"
    STATUS_FROZEN = "冻结"
    STATUS_LOST = "挂失"
    STATUS_CLOSED = "销户"
    
    def __init__(self, username, initial_balance=0.0):
        """
        初始化账户对象
        :param username: 关联的用户名
        :param initial_balance: 初始余额
        """
        self.card_number = self._generate_card_number()
        self.username = username
        self.balance = initial_balance
        self.status = self.STATUS_NORMAL
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history = []
    
    @staticmethod
    def _generate_card_number():
        """生成16位银行卡号"""
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    
    def deposit(self, amount):
        """
        存款
        :param amount: 存款金额
        :return: 成功返回True，失败返回False及错误信息
        """
        if amount <= 0:
            return False, "存款金额必须大于0"
        
        if self.status != self.STATUS_NORMAL:
            return False, f"账户状态为{self.status}，无法进行存款操作"
        
        self.balance += amount
        self._add_transaction("存款", amount, self.balance)
        return True, f"存款成功，当前余额：{self.balance}元"
    
    def withdraw(self, amount):
        """
        取款
        :param amount: 取款金额
        :return: 成功返回True，失败返回False及错误信息
        """
        if amount <= 0:
            return False, "取款金额必须大于0"
        
        if self.status != self.STATUS_NORMAL:
            return False, f"账户状态为{self.status}，无法进行取款操作"
        
        if self.balance < amount:
            return False, f"余额不足，当前余额：{self.balance}元"
        
        self.balance -= amount
        self._add_transaction("取款", amount, self.balance)
        return True, f"取款成功，当前余额：{self.balance}元"
    
    def get_balance(self):
        """查询余额"""
        return self.balance
    
    def freeze(self):
        """冻结账户"""
        if self.status == self.STATUS_CLOSED:
            return False, "账户已销户，无法冻结"
        self.status = self.STATUS_FROZEN
        self._add_transaction("冻结", 0, self.balance)
        return True, "账户冻结成功"
    
    def unfreeze(self):
        """解冻账户"""
        if self.status == self.STATUS_FROZEN:
            self.status = self.STATUS_NORMAL
            self._add_transaction("解冻", 0, self.balance)
            return True, "账户解冻成功"
        return False, f"当前账户状态为{self.status}，无法解冻"
    
    def report_loss(self):
        """挂失"""
        if self.status == self.STATUS_CLOSED:
            return False, "账户已销户，无法挂失"
        self.status = self.STATUS_LOST
        self._add_transaction("挂失", 0, self.balance)
        return True, "账户挂失成功"
    
    def cancel_loss(self):
        """解除挂失"""
        if self.status == self.STATUS_LOST:
            self.status = self.STATUS_NORMAL
            self._add_transaction("解除挂失", 0, self.balance)
            return True, "解除挂失成功"
        return False, f"当前账户状态为{self.status}，无法解除挂失"
    
    def close_account(self):
        """销户"""
        if self.status == self.STATUS_CLOSED:
            return False, "账户已销户"
        
        if self.balance > 0:
            return False, f"账户还有余额{self.balance}元，请先取出"
        
        self.status = self.STATUS_CLOSED
        self._add_transaction("销户", 0, self.balance)
        return True, "销户成功"
    
    def _add_transaction(self, trans_type, amount, balance_after):
        """添加交易记录"""
        transaction = {
            'type': trans_type,
            'amount': amount,
            'balance_after': balance_after,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transaction_history.append(transaction)
    
    def get_transaction_history(self):
        """获取交易历史"""
        return self.transaction_history
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'card_number': self.card_number,
            'username': self.username,
            'balance': self.balance,
            'status': self.status,
            'created_at': self.created_at,
            'transaction_history': self.transaction_history
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建账户对象"""
        account = cls.__new__(cls)
        account.card_number = data['card_number']
        account.username = data['username']
        account.balance = data['balance']
        account.status = data['status']
        account.created_at = data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        account.transaction_history = data.get('transaction_history', [])
        return account
    
    def __str__(self):
        """字符串表示"""
        return f"Account({self.card_number}, {self.username}, 余额:{self.balance}, 状态:{self.status})"

