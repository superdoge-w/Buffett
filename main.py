#!/usr/bin/env python3
"""
DeepSeek LangChain Integration - 统一入口
提供安装、测试、示例等所有功能的统一入口点
"""
import sys
import os

def show_help():
    """显示帮助信息"""
    print("🚀 DeepSeek LangChain Integration 统一工具")
    print("=" * 60)
    print("功能模块:")
    print("  install    - 安装依赖库")
    print("  test       - 测试功能")
    print("  examples   - 运行示例")
    print("  chat       - 启动交互式聊天")
    print("  help       - 显示帮助")
    print()
    print("使用方法:")
    print("  python main.py install [--all|--mirror <name>]")
    print("  python main.py test [--deps-only|--api-only|--examples]")
    print("  python main.py examples")
    print("  python main.py chat")
    print("  python main.py help")
    print()
    print("示例:")
    print("  python main.py install                    # 安装核心依赖")
    print("  python main.py install --all              # 安装所有依赖")
    print("  python main.py install --mirror aliyun    # 使用阿里云镜像")
    print("  python main.py test                       # 完整测试")
    print("  python main.py test --deps-only           # 仅检查依赖")
    print("  python main.py examples                   # 运行示例")
    print("  python main.py chat                       # 启动交互式聊天")

def run_install():
    """运行安装功能"""
    from install_unified import main as install_main
    install_main()

def run_test():
    """运行测试功能"""
    from test_all import main as test_main
    test_main()

def run_examples():
    """运行示例"""
    from test_all import DeepSeekTester
    tester = DeepSeekTester()
    tester.run_examples()

def run_chat():
    """启动交互式聊天"""
    from interactive_chat import start_interactive_chat
    start_interactive_chat()

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "install":
        # 重新组织参数给install_unified.py
        sys.argv = ["install_unified.py"] + sys.argv[2:]
        run_install()
    
    elif command == "test":
        # 重新组织参数给test_all.py
        if len(sys.argv) > 2:
            sys.argv = ["test_all.py"] + sys.argv[2:]
        else:
            sys.argv = ["test_all.py"]
        run_test()
    
    elif command == "examples":
        run_examples()
    
    elif command in ["chat", "interactive"]:
        run_chat()
    
    elif command in ["help", "--help", "-h"]:
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}")
        print("使用 'python main.py help' 查看帮助")
        sys.exit(1)

if __name__ == "__main__":
    main()