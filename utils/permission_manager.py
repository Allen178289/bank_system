"""
权限管理器 - Permission Manager
负责管理用户权限和角色控制
"""

from models.user import User


class PermissionManager:
    """权限管理器"""
    
    # 权限定义
    PERMISSIONS = {
        # 普通用户权限
        User.ROLE_NORMAL: {
            'view_own_accounts': True,        # 查看自己的账户
            'create_account': True,           # 创建账户
            'deposit': True,                  # 存款
            'withdraw': True,                 # 取款
            'transfer': True,                 # 转账
            'view_transaction_history': True, # 查看交易历史
            'manage_own_profile': True,       # 管理自己的资料
            'freeze_own_account': True,       # 冻结自己的账户
            'unfreeze_own_account': True,     # 解冻自己的账户
            'report_loss': True,              # 挂失
            'close_account': True,            # 销户
            # 不允许的权限
            'view_all_users': False,          # 查看所有用户
            'manage_all_users': False,        # 管理所有用户
            'view_all_accounts': False,       # 查看所有账户
            'manage_all_accounts': False,     # 管理所有账户
            'change_user_role': False,        # 修改用户角色
        },
        
        # VIP用户权限（继承普通用户，额外增加一些特权）
        User.ROLE_VIP: {
            'view_own_accounts': True,
            'create_account': True,
            'deposit': True,
            'withdraw': True,
            'transfer': True,
            'view_transaction_history': True,
            'manage_own_profile': True,
            'freeze_own_account': True,
            'unfreeze_own_account': True,
            'report_loss': True,
            'close_account': True,
            'priority_transfer': True,         # VIP专属：优先转账（未来可实现）
            'higher_transfer_limit': True,     # VIP专属：更高的转账限额
            # 不允许的权限
            'view_all_users': False,
            'manage_all_users': False,
            'view_all_accounts': False,
            'manage_all_accounts': False,
            'change_user_role': False,
        },
        
        # 管理员权限（拥有所有权限）
        User.ROLE_ADMIN: {
            'view_own_accounts': True,
            'create_account': True,
            'deposit': True,
            'withdraw': True,
            'transfer': True,
            'view_transaction_history': True,
            'manage_own_profile': True,
            'freeze_own_account': True,
            'unfreeze_own_account': True,
            'report_loss': True,
            'close_account': True,
            'view_all_users': True,           # 管理员：查看所有用户
            'manage_all_users': True,         # 管理员：管理所有用户
            'view_all_accounts': True,        # 管理员：查看所有账户
            'manage_all_accounts': True,      # 管理员：管理所有账户
            'change_user_role': True,         # 管理员：修改用户角色
            'freeze_any_account': True,       # 管理员：冻结任何账户
            'unfreeze_any_account': True,     # 管理员：解冻任何账户
            'view_all_transactions': True,    # 管理员：查看所有交易
        }
    }
    
    @classmethod
    def has_permission(cls, user, permission):
        """
        检查用户是否有某个权限
        :param user: 用户对象
        :param permission: 权限名称
        :return: True/False
        """
        if not user or not hasattr(user, 'role'):
            return False
        
        role = user.role
        if role not in cls.PERMISSIONS:
            return False
        
        return cls.PERMISSIONS[role].get(permission, False)
    
    @classmethod
    def get_role_name(cls, role):
        """
        获取角色的中文名称
        :param role: 角色代码
        :return: 角色中文名称
        """
        role_names = {
            User.ROLE_NORMAL: '普通用户',
            User.ROLE_VIP: 'VIP用户',
            User.ROLE_ADMIN: '管理员'
        }
        return role_names.get(role, '未知角色')
    
    @classmethod
    def get_all_roles(cls):
        """获取所有角色列表"""
        return [
            {'code': User.ROLE_NORMAL, 'name': '普通用户'},
            {'code': User.ROLE_VIP, 'name': 'VIP用户'},
            {'code': User.ROLE_ADMIN, 'name': '管理员'}
        ]
    
    @classmethod
    def check_role_permission(cls, user, action, target_user=None):
        """
        检查用户对特定操作的权限
        :param user: 当前用户
        :param action: 操作类型 ('view', 'edit', 'delete', etc.)
        :param target_user: 目标用户（如果是对其他用户的操作）
        :return: (允许/不允许, 消息)
        """
        # 未登录
        if not user:
            return False, "请先登录"
        
        # 管理员拥有所有权限
        if user.is_admin():
            return True, "管理员权限"
        
        # 对自己的操作
        if target_user and target_user.username == user.username:
            return True, "可以操作自己的账户"
        
        # VIP用户的特殊权限
        if user.is_vip() and action in ['view', 'edit']:
            # VIP可以查看和编辑自己的信息
            if target_user and target_user.username == user.username:
                return True, "VIP用户权限"
        
        # 普通用户只能操作自己的账户
        if user.is_normal():
            if target_user and target_user.username != user.username:
                return False, "无权操作其他用户的账户"
            return True, "可以操作自己的账户"
        
        return False, "权限不足"
    
    @classmethod
    def get_transfer_limit(cls, user):
        """
        获取用户的转账限额
        :param user: 用户对象
        :return: 单笔转账限额
        """
        if not user:
            return 0
        
        # 不同角色的转账限额
        limits = {
            User.ROLE_NORMAL: 10000,    # 普通用户：单笔10000元
            User.ROLE_VIP: 50000,       # VIP用户：单笔50000元
            User.ROLE_ADMIN: 1000000    # 管理员：单笔1000000元
        }
        
        return limits.get(user.role, 0)

