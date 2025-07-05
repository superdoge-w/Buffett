#!/usr/bin/env python3
"""
DeepSeek LangChain 模块统一测试脚本
合并了所有测试功能：依赖检查、API测试、功能验证
"""
import os
import sys
import time
import json
import importlib
from typing import Dict, Any
import requests

class DeepSeekTester:
    """DeepSeek模块统一测试类"""
    
    def __init__(self):
        self.api_key = "sk-3ad5021f360842faa077e9f3d85103d1"
        self.base_url = "https://api.deepseek.com/v1"
    
    def test_dependencies(self) -> Dict[str, bool]:
        """测试依赖库安装状态"""
        print("🔍 检查依赖库...")
        print("=" * 50)
        
        # 核心依赖
        core_deps = [
            ('requests', 'requests (HTTP请求)', True),
            ('pydantic', 'pydantic (数据验证)', True),
            ('dotenv', 'python-dotenv (环境变量)', True),
            ('typing_extensions', 'typing-extensions (类型提示)', True),
        ]
        
        # LangChain依赖
        langchain_deps = [
            ('langchain', 'langchain (主框架)', False),
            ('langchain_core', 'langchain-core (核心组件)', False),
            ('langchain_community', 'langchain-community (社区扩展)', False),
            ('openai', 'openai (OpenAI兼容)', False),
        ]
        
        results = {}
        
        print("📦 核心依赖:")
        core_installed = 0
        for module, display, required in core_deps:
            if self._check_dependency(module, display, required):
                core_installed += 1
                results[module] = True
            else:
                results[module] = False
        
        print(f"\n核心依赖: {core_installed}/{len(core_deps)}")
        
        print("\n🔗 LangChain依赖:")
        langchain_installed = 0
        for module, display, required in langchain_deps:
            if self._check_dependency(module, display, required):
                langchain_installed += 1
                results[module] = True
            else:
                results[module] = False
        
        print(f"\nLangChain依赖: {langchain_installed}/{len(langchain_deps)}")
        
        # 总结
        results['core_complete'] = core_installed == len(core_deps)
        results['langchain_available'] = langchain_installed > 0
        
        return results
    
    def _check_dependency(self, module_name: str, display_name: str, required: bool) -> bool:
        """检查单个依赖"""
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', '未知版本')
            status = "✅" if required else "✅"
            print(f"{status} {display_name} {version}")
            return True
        except ImportError:
            status = "❌" if required else "⚠️"
            print(f"{status} {display_name} {'未安装' if required else '未安装 (可选)'}")
            return False
    
    def test_module_import(self) -> bool:
        """测试DeepSeek模块导入"""
        print("\n🧪 测试模块导入...")
        try:
            from deepseek_llm import DeepSeekLLM, DeepSeekChat, DeepSeekCode
            print("✅ DeepSeek模块导入成功")
            
            # 测试初始化
            llm = DeepSeekLLM(api_key=self.api_key)
            print("✅ DeepSeek模块初始化成功")
            return True
        except Exception as e:
            print(f"❌ DeepSeek模块测试失败: {e}")
            return False
    
    def test_api_call(self) -> bool:
        """测试API调用"""
        print("\n📡 测试API调用...")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "你好"}],
            "temperature": 0.7,
            "max_tokens": 50,
            "stream": False
        }
        
        try:
            print("🔄 发送API请求...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"📊 响应时间: {response_time:.2f}秒")
            print(f"📊 状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ API调用成功!")
                    print(f"📝 响应内容: {content}")
                    return True
            else:
                print(f"❌ API返回错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """运行所有测试"""
        print("🚀 DeepSeek模块全面测试")
        print("=" * 60)
        
        results = {}
        
        # 1. 依赖检查
        dep_results = self.test_dependencies()
        results.update(dep_results)
        
        # 2. 模块导入测试
        results['module_import'] = self.test_module_import()
        
        # 3. API调用测试
        if results.get('requests', False):
            results['api_call'] = self.test_api_call()
        else:
            print("\n❌ 跳过API测试 - requests未安装")
            results['api_call'] = False
        
        # 生成报告
        self._generate_report(results)
        
        return results
    
    def _generate_report(self, results: Dict[str, bool]):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        # 核心功能状态
        if results.get('core_complete', False):
            print("✅ 核心功能: 完全可用")
        else:
            print("❌ 核心功能: 需要安装缺失依赖")
        
        # 模块状态
        if results.get('module_import', False):
            print("✅ DeepSeek模块: 可用")
        else:
            print("❌ DeepSeek模块: 不可用")
        
        # API状态
        if results.get('api_call', False):
            print("✅ API调用: 正常")
        else:
            print("❌ API调用: 失败")
        
        # LangChain状态
        if results.get('langchain_available', False):
            print("✅ LangChain集成: 可用")
        else:
            print("❌ LangChain集成: 不可用")
        
        # 整体评估
        critical_tests = ['core_complete', 'module_import', 'api_call']
        passed_critical = sum(1 for test in critical_tests if results.get(test, False))
        
        print(f"\n📈 整体状态: {passed_critical}/{len(critical_tests)} 关键测试通过")
        
        if passed_critical == len(critical_tests):
            print("🎉 所有关键功能正常，模块可以正常使用！")
        else:
            print("⚠️ 部分功能异常，请检查上述问题")

    def run_examples(self):
        """运行使用示例"""
        print("🚀 DeepSeek使用示例")
        print("=" * 60)
        
        try:
            from deepseek_llm import DeepSeekLLM, DeepSeekChat, DeepSeekCode
            from langchain_core.prompts import PromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            
            # 基础示例
            print("\n📝 基础LLM示例:")
            llm = DeepSeekLLM(api_key=self.api_key, max_tokens=100)
            response = llm.invoke("用一句话解释什么是人工智能")
            print(f"✅ 响应: {response}")
            
            # Chat模型示例
            print("\n💬 Chat模型示例:")
            chat_llm = DeepSeekChat(api_key=self.api_key, max_tokens=80)
            response = chat_llm.invoke("你好，能简单介绍一下你自己吗？")
            print(f"✅ 响应: {response}")
            
            # LangChain链式调用示例
            print("\n🔗 LangChain链式调用示例:")
            prompt = PromptTemplate(
                input_variables=["topic"],
                template="请用一句话解释：{topic}"
            )
            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({"topic": "量子计算"})
            print(f"✅ 链式调用响应: {response}")
            
            print("\n🎉 示例运行完成!")
            
        except Exception as e:
            print(f"❌ 示例运行失败: {e}")

def main():
    """主函数"""
    tester = DeepSeekTester()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--deps-only':
            tester.test_dependencies()
        elif sys.argv[1] == '--api-only':
            tester.test_api_call()
        elif sys.argv[1] == '--examples':
            tester.run_examples()
        elif sys.argv[1] == '--help':
            print("🔧 DeepSeek测试工具使用说明:")
            print("  python test_all.py            # 完整测试")
            print("  python test_all.py --deps-only    # 仅检查依赖")
            print("  python test_all.py --api-only     # 仅测试API")
            print("  python test_all.py --examples     # 运行使用示例")
            print("  python test_all.py --help         # 显示帮助")
        else:
            print("❌ 未知参数，使用 --help 查看帮助")
    else:
        tester.run_all_tests()

if __name__ == "__main__":
    main()