"""
用户模型 - User Model
负责用户数据的定义和基本操作
"""
import hashlib
from datetime import datetime


class User:
    """用户类"""
    
    def __init__(self, username, password, real_name, id_card, phone, email=""):
        """
        初始化用户对象
        :param username: 用户名
        :param password: 密码
        :param real_name: 真实姓名
        :param id_card: 身份证号
        :param phone: 手机号
        :param email: 邮箱
        """
        self.username = username
        self.password = self._hash_password(password)
        self.real_name = real_name
        self.id_card = id_card
        self.phone = phone
        self.email = email
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = True
    
    @staticmethod
    def _hash_password(password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """验证密码"""
        return self.password == self._hash_password(password)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'username': self.username,
            'password': self.password,
            'real_name': self.real_name,
            'id_card': self.id_card,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建用户对象"""
        user = cls.__new__(cls)
        user.username = data['username']
        user.password = data['password']
        user.real_name = data['real_name']
        user.id_card = data['id_card']
        user.phone = data['phone']
        user.email = data.get('email', '')
        user.created_at = data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user.is_active = data.get('is_active', True)
        return user
    
    def __str__(self):
        """字符串表示"""
        return f"User({self.username}, {self.real_name}, {self.phone})"

