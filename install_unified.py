#!/usr/bin/env python3
"""
DeepSeek LangChain 模块统一安装脚本
支持多种镜像源和安装选项
"""
import os
import sys
import subprocess
from typing import List

class DeepSeekInstaller:
    """DeepSeek模块统一安装器"""
    
    # 镜像源配置
    MIRRORS = {
        'tsinghua': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'aliyun': 'https://mirrors.aliyun.com/pypi/simple/',
        'douban': 'https://pypi.douban.com/simple/',
        'ustc': 'https://pypi.mirrors.ustc.edu.cn/simple/',
        'official': 'https://pypi.org/simple/'
    }
    
    # 依赖包分组
    PACKAGES = {
        'core': [
            'requests>=2.25.1',
            'pydantic>=2.0.0',
            'python-dotenv>=0.19.0',
            'typing-extensions>=4.0.0'
        ],
        'langchain': [
            'langchain>=0.1.0',
            'langchain-core>=0.1.0',
            'langchain-community>=0.0.10'
        ],
        'optional': [
            'openai>=1.0.0'
        ]
    }
    
    def __init__(self, mirror: str = 'tsinghua'):
        self.mirror = mirror
        self.mirror_url = self.MIRRORS.get(mirror, self.MIRRORS['tsinghua'])
    
    def install_packages(self, packages: List[str], group_name: str = "") -> bool:
        """安装包列表"""
        if not packages:
            return True
        
        print(f"📦 安装{group_name}依赖...")
        
        for package in packages:
            if not self._install_single_package(package):
                print(f"❌ {package} 安装失败")
                return False
        
        print(f"✅ {group_name}依赖安装完成")
        return True
    
    def _install_single_package(self, package: str) -> bool:
        """安装单个包"""
        cmd = [
            sys.executable, '-m', 'pip', 'install',
            package, '-i', self.mirror_url, '--quiet'
        ]
        
        try:
            print(f"🔄 安装 {package}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} 安装成功")
                return True
            else:
                print(f"❌ {package} 安装失败")
                return False
                
        except Exception as e:
            print(f"❌ {package} 安装异常: {e}")
            return False
    
    def install_core(self) -> bool:
        """安装核心依赖"""
        return self.install_packages(self.PACKAGES['core'], "核心")
    
    def install_langchain(self) -> bool:
        """安装LangChain依赖"""
        return self.install_packages(self.PACKAGES['langchain'], "LangChain")
    
    def install_all(self) -> bool:
        """安装所有依赖"""
        all_packages = []
        all_packages.extend(self.PACKAGES['core'])
        all_packages.extend(self.PACKAGES['langchain'])
        
        return self.install_packages(all_packages, "全部")

def main():
    """主函数"""
    print("🚀 DeepSeek LangChain 模块安装器")
    print("=" * 50)
    
    # 解析命令行参数
    mirror = 'tsinghua'
    install_type = 'core'
    
    if len(sys.argv) > 1:
        if '--mirror' in sys.argv:
            idx = sys.argv.index('--mirror')
            if idx + 1 < len(sys.argv):
                mirror = sys.argv[idx + 1]
        
        if '--all' in sys.argv:
            install_type = 'all'
        elif '--langchain' in sys.argv:
            install_type = 'langchain'
    
    # 创建安装器
    installer = DeepSeekInstaller(mirror=mirror)
    print(f"📦 使用镜像源: {installer.mirror_url}")
    
    # 执行安装
    success = False
    if install_type == 'all':
        success = installer.install_all()
    elif install_type == 'langchain':
        success = installer.install_langchain()
    else:
        success = installer.install_core()
    
    # 显示结果
    if success:
        print("\n🎉 安装完成!")
        print("现在可以运行: python test_all.py")
    else:
        print("\n❌ 安装失败")
        print("请尝试其他镜像源:")
        for name in DeepSeekInstaller.MIRRORS.keys():
            print(f"  python install_unified.py --mirror {name}")

if __name__ == "__main__":
    main()