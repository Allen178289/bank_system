"""
用户控制器 - User Controller
负责用户相关业务逻辑的处理
"""
from models.user import User
from utils.data_manager import DataManager


class UserController:
    """用户控制器类"""
    
    def __init__(self):
        """初始化用户控制器"""
        self.data_manager = DataManager()
        self.current_user = None
    
    def register(self, username, password, real_name, id_card, phone, email=""):
        """
        用户注册
        :return: (成功标志, 消息)
        """
        # 检查用户名是否已存在
        if self.data_manager.user_exists(username):
            return False, "用户名已存在"
        
        # 验证输入
        if not username or not password or not real_name or not id_card or not phone:
            return False, "所有必填字段不能为空"
        
        if len(username) < 3:
            return False, "用户名长度至少3个字符"
        
        if len(password) < 6:
            return False, "密码长度至少6个字符"
        
        if len(id_card) != 18:
            return False, "身份证号必须为18位"
        
        if len(phone) != 11:
            return False, "手机号必须为11位"
        
        # 创建用户对象
        user = User(username, password, real_name, id_card, phone, email)
        
        # 保存到数据库
        self.data_manager.add_user(user.to_dict())
        
        return True, "注册成功！"
    
    def login(self, username, password):
        """
        用户登录
        :return: (成功标志, 消息)
        """
        # 获取用户数据
        user_data = self.data_manager.get_user(username)
        
        if not user_data:
            return False, "用户不存在"
        
        # 创建用户对象并验证密码
        user = User.from_dict(user_data)
        
        if not user.verify_password(password):
            return False, "密码错误"
        
        if not user.is_active:
            return False, "账户已被禁用"
        
        # 设置当前登录用户
        self.current_user = user
        
        return True, f"欢迎回来，{user.real_name}！"
    
    def logout(self):
        """用户登出"""
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            return True, f"用户 {username} 已退出登录"
        return False, "当前没有登录的用户"
    
    def is_logged_in(self):
        """检查是否已登录"""
        return self.current_user is not None
    
    def get_current_user(self):
        """获取当前登录用户"""
        return self.current_user
    
    def update_user_info(self, phone=None, email=None):
        """
        更新用户信息
        :return: (成功标志, 消息)
        """
        if not self.current_user:
            return False, "请先登录"
        
        # 更新信息
        if phone:
            if len(phone) != 11:
                return False, "手机号必须为11位"
            self.current_user.phone = phone
        
        if email:
            self.current_user.email = email
        
        # 保存到数据库
        self.data_manager.update_user(
            self.current_user.username,
            self.current_user.to_dict()
        )
        
        return True, "用户信息更新成功"
    
    def get_user_info(self):
        """获取用户信息"""
        if not self.current_user:
            return None
        
        return {
            '用户名': self.current_user.username,
            '真实姓名': self.current_user.real_name,
            '身份证号': self.current_user.id_card,
            '手机号': self.current_user.phone,
            '邮箱': self.current_user.email,
            '注册时间': self.current_user.created_at,
            '账户状态': '正常' if self.current_user.is_active else '禁用'
        }
    
    def change_password(self, old_password, new_password):
        """
        修改密码
        :return: (成功标志, 消息)
        """
        if not self.current_user:
            return False, "请先登录"
        
        # 验证旧密码
        if not self.current_user.verify_password(old_password):
            return False, "旧密码错误"
        
        # 验证新密码
        if len(new_password) < 6:
            return False, "新密码长度至少6个字符"
        
        # 更新密码
        import hashlib
        self.current_user.password = hashlib.sha256(new_password.encode()).hexdigest()
        
        # 保存到数据库
        self.data_manager.update_user(
            self.current_user.username,
            self.current_user.to_dict()
        )
        
        return True, "密码修改成功"

