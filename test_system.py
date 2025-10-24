"""
系统测试脚本
用于验证银行卡管理系统的各个模块是否正常工作
"""

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("-" * 60)
    
    try:
        from models.user import User
        print("✓ models.user.User 导入成功")
    except Exception as e:
        print(f"✗ models.user.User 导入失败: {e}")
        return False
    
    try:
        from models.account import Account
        print("✓ models.account.Account 导入成功")
    except Exception as e:
        print(f"✗ models.account.Account 导入失败: {e}")
        return False
    
    try:
        from controllers.user_controller import UserController
        print("✓ controllers.user_controller.UserController 导入成功")
    except Exception as e:
        print(f"✗ controllers.user_controller.UserController 导入失败: {e}")
        return False
    
    try:
        from controllers.account_controller import AccountController
        print("✓ controllers.account_controller.AccountController 导入成功")
    except Exception as e:
        print(f"✗ controllers.account_controller.AccountController 导入失败: {e}")
        return False
    
    try:
        from views.main_view import MainView
        print("✓ views.main_view.MainView 导入成功")
    except Exception as e:
        print(f"✗ views.main_view.MainView 导入失败: {e}")
        return False
    
    try:
        from utils.data_manager import DataManager
        print("✓ utils.data_manager.DataManager 导入成功")
    except Exception as e:
        print(f"✗ utils.data_manager.DataManager 导入失败: {e}")
        return False
    
    print("-" * 60)
    print("✓ 所有模块导入成功！")
    print("=" * 60)
    return True


def test_user_model():
    """测试用户模型"""
    print("\n" + "=" * 60)
    print("测试用户模型...")
    print("-" * 60)
    
    from models.user import User
    
    # 创建用户
    user = User("testuser", "123456", "测试用户", "110101199001011234", "13800138000", "test@example.com")
    print(f"✓ 创建用户: {user}")
    
    # 测试密码验证
    assert user.verify_password("123456"), "密码验证失败"
    print("✓ 密码验证成功")
    
    assert not user.verify_password("wrong"), "密码验证应该失败"
    print("✓ 错误密码验证正确")
    
    # 测试序列化
    user_dict = user.to_dict()
    print(f"✓ 对象序列化: {user_dict['username']}")
    
    # 测试反序列化
    user2 = User.from_dict(user_dict)
    print(f"✓ 对象反序列化: {user2}")
    
    print("-" * 60)
    print("✓ 用户模型测试通过！")
    print("=" * 60)


def test_account_model():
    """测试账户模型"""
    print("\n" + "=" * 60)
    print("测试账户模型...")
    print("-" * 60)
    
    from models.account import Account
    
    # 创建账户
    account = Account("testuser", 1000.0)
    print(f"✓ 创建账户: {account.card_number}, 余额: {account.balance}")
    
    # 测试存款
    success, msg = account.deposit(500)
    assert success, "存款失败"
    assert account.balance == 1500, "余额不正确"
    print(f"✓ 存款测试通过: {msg}")
    
    # 测试取款
    success, msg = account.withdraw(300)
    assert success, "取款失败"
    assert account.balance == 1200, "余额不正确"
    print(f"✓ 取款测试通过: {msg}")
    
    # 测试余额不足
    success, msg = account.withdraw(2000)
    assert not success, "余额不足应该取款失败"
    print(f"✓ 余额不足测试通过: {msg}")
    
    # 测试冻结
    success, msg = account.freeze()
    assert success, "冻结失败"
    print(f"✓ 冻结测试通过: {msg}")
    
    # 测试冻结状态下不能存款
    success, msg = account.deposit(100)
    assert not success, "冻结状态应该不能存款"
    print(f"✓ 冻结状态限制测试通过: {msg}")
    
    # 测试解冻
    success, msg = account.unfreeze()
    assert success, "解冻失败"
    print(f"✓ 解冻测试通过: {msg}")
    
    # 测试交易历史
    history = account.get_transaction_history()
    assert len(history) > 0, "交易历史为空"
    print(f"✓ 交易历史测试通过，共{len(history)}条记录")
    
    print("-" * 60)
    print("✓ 账户模型测试通过！")
    print("=" * 60)


def test_data_manager():
    """测试数据管理器"""
    print("\n" + "=" * 60)
    print("测试数据管理器...")
    print("-" * 60)
    
    from utils.data_manager import DataManager
    import os
    import shutil
    
    # 使用测试目录
    test_dir = "test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    dm = DataManager(test_dir)
    print(f"✓ 创建数据管理器，数据目录: {test_dir}")
    
    # 测试用户数据
    test_user = {
        'username': 'testuser',
        'password': 'hashedpwd',
        'real_name': '测试',
        'id_card': '123456789012345678',
        'phone': '13800138000',
        'email': 'test@test.com'
    }
    
    dm.add_user(test_user)
    print("✓ 添加用户数据")
    
    loaded_user = dm.get_user('testuser')
    assert loaded_user is not None, "用户数据加载失败"
    assert loaded_user['username'] == 'testuser', "用户数据不匹配"
    print("✓ 加载用户数据成功")
    
    # 清理测试数据
    shutil.rmtree(test_dir)
    print("✓ 清理测试数据")
    
    print("-" * 60)
    print("✓ 数据管理器测试通过！")
    print("=" * 60)


def test_controllers():
    """测试控制器"""
    print("\n" + "=" * 60)
    print("测试控制器...")
    print("-" * 60)
    
    from controllers.user_controller import UserController
    from controllers.account_controller import AccountController
    import os
    import shutil
    
    # 使用测试目录
    test_dir = "test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # 切换数据目录
    import utils.data_manager as dm_module
    original_init = dm_module.DataManager.__init__
    
    def new_init(self, data_dir='test_data'):
        original_init(self, data_dir)
    
    dm_module.DataManager.__init__ = new_init
    
    try:
        # 测试用户控制器
        uc = UserController()
        print("✓ 创建用户控制器")
        
        # 测试注册
        success, msg = uc.register("testuser", "123456", "测试用户", "110101199001011234", "13800138000")
        assert success, f"注册失败: {msg}"
        print(f"✓ 用户注册成功: {msg}")
        
        # 测试登录
        success, msg = uc.login("testuser", "123456")
        assert success, f"登录失败: {msg}"
        print(f"✓ 用户登录成功: {msg}")
        
        # 测试账户控制器
        ac = AccountController(uc)
        print("✓ 创建账户控制器")
        
        # 测试开户
        success, msg, card_number = ac.create_account(1000)
        assert success, f"开户失败: {msg}"
        print(f"✓ 开户成功: {msg}")
        
        # 测试存款
        success, msg = ac.deposit(card_number, 500)
        assert success, f"存款失败: {msg}"
        print(f"✓ 存款成功: {msg}")
        
        # 测试查询余额
        success, balance = ac.check_balance(card_number)
        assert success, "查询余额失败"
        assert balance == 1500, f"余额不正确，期望1500，实际{balance}"
        print(f"✓ 查询余额成功: {balance}")
        
    finally:
        # 恢复原始init
        dm_module.DataManager.__init__ = original_init
        
        # 清理测试数据
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        print("✓ 清理测试数据")
    
    print("-" * 60)
    print("✓ 控制器测试通过！")
    print("=" * 60)


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "银行卡管理系统 - 系统测试".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        # 测试导入
        if not test_imports():
            print("\n✗ 模块导入测试失败，请检查项目结构")
            return
        
        # 测试模型
        test_user_model()
        test_account_model()
        
        # 测试工具类
        test_data_manager()
        
        # 测试控制器
        test_controllers()
        
        # 全部通过
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "✓ 所有测试通过！系统运行正常！".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")
        print("现在可以运行主程序了：")
        print("  python main.py")
        print("\n")
        
    except Exception as e:
        print("\n")
        print("✗ 测试过程中出现错误:")
        print(f"  {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

