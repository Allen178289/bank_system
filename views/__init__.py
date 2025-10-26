"""
Views模块初始化文件
包含命令行视图和GUI视图
"""

# 命令行视图
from .main_view import MainView

# GUI视图（仅在安装PyQt5时可用）
try:
    from .login_window import LoginWindow
    from .register_window import RegisterWindow
    from .main_window import MainWindow
    from . import dialogs
    
    __all__ = [
        'MainView',          # 命令行视图
        'LoginWindow',       # GUI登录窗口
        'RegisterWindow',    # GUI注册窗口
        'MainWindow',        # GUI主窗口
        'dialogs'            # GUI对话框模块
    ]
except ImportError:
    # 如果PyQt5未安装，只导出命令行视图
    __all__ = ['MainView']
