#!/usr/bin/env python3
"""
DeepSeek 交互式聊天模块
支持prompt微调、few shot学习和实时流式对话
"""
import os
import sys
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from deepseek_llm import DeepSeekLLM


@dataclass
class ChatMessage:
    """聊天消息类"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass 
class FewShotExample:
    """Few Shot示例类"""
    user_input: str
    assistant_response: str
    description: str = ""


class DeepSeekInteractiveChat:
    """DeepSeek交互式聊天类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化交互式聊天"""
        self.llm = DeepSeekLLM(api_key=api_key)
        self.conversation_history: List[ChatMessage] = []
        self.system_prompt = self._get_default_system_prompt()
        self.few_shot_examples = self._get_default_few_shot_examples()
        self.max_history_length = 20  # 保留最近20条对话
        
    def _get_default_system_prompt(self) -> str:
        """获取默认系统提示词（可在此处修改）"""
        return """你是一个专业的AI助手，具有以下特点：
1. 友好、耐心、专业
2. 能够理解上下文，提供准确的回答
3. 善于解释复杂概念，使用简洁明了的语言
4. 会根据用户需求调整回答的详细程度
5. 遇到不确定的问题时，会诚实地说明不确定性

请始终保持礼貌和专业，为用户提供最佳的帮助体验。"""
    
    def _get_default_few_shot_examples(self) -> List[FewShotExample]:
        """获取默认的Few Shot示例（可在此处修改，最多3个）"""
        return [
            FewShotExample(
                user_input="如何提高工作效率？",
                assistant_response="提高工作效率的几个关键方法：\n1. **时间管理**：使用番茄钟技术，专注25分钟后休息5分钟\n2. **优先级排序**：按重要性和紧急程度排列任务\n3. **减少干扰**：关闭不必要的通知，创造专注环境\n4. **工具辅助**：使用项目管理工具如Trello或Notion\n5. **定期反思**：每周回顾，找出效率瓶颈并改进",
                description="工作效率提升建议"
            ),
            FewShotExample(
                user_input="Python中如何处理异常？",
                assistant_response="Python异常处理主要使用try-except语句：\n\n```python\ntry:\n    # 可能出错的代码\n    result = 10 / 0\nexcept ZeroDivisionError:\n    # 处理特定异常\n    print(\"除零错误\")\nexcept Exception as e:\n    # 处理其他异常\n    print(f\"发生错误: {e}\")\nelse:\n    # 没有异常时执行\n    print(\"执行成功\")\nfinally:\n    # 无论是否有异常都执行\n    print(\"清理资源\")\n```\n\n最佳实践：捕获具体异常类型，避免使用裸露的except。",
                description="Python异常处理教学"
            ),
            FewShotExample(
                user_input="解释一下区块链技术",
                assistant_response="区块链是一种**分布式账本技术**，核心特点：\n\n🔗 **链式结构**：每个区块包含前一个区块的哈希值，形成不可篡改的链\n🌐 **去中心化**：没有单一控制点，由网络节点共同维护\n🔐 **加密安全**：使用密码学确保数据完整性\n✅ **共识机制**：通过算法确保网络状态一致\n\n**应用场景**：数字货币、供应链溯源、数字身份认证等。区块链解决了数字世界中的信任问题，但也面临扩展性和能耗挑战。",
                description="区块链技术科普"
            )
        ]
    
    def update_system_prompt(self, new_prompt: str):
        """更新系统提示词"""
        self.system_prompt = new_prompt
        print(f"✅ 系统提示词已更新")
    
    def add_few_shot_example(self, example: FewShotExample):
        """添加Few Shot示例（最多3个）"""
        if len(self.few_shot_examples) >= 3:
            print("⚠️  Few Shot示例已达到最大数量(3个)，将替换最旧的示例")
            self.few_shot_examples.pop(0)
        self.few_shot_examples.append(example)
        print(f"✅ 已添加Few Shot示例: {example.description}")
    
    def get_few_shot_examples(self) -> List[FewShotExample]:
        """获取当前Few Shot示例"""
        return self.few_shot_examples
    
    def clear_few_shot_examples(self):
        """清空Few Shot示例"""
        self.few_shot_examples.clear()
        print("✅ 已清空所有Few Shot示例")
    
    def _build_prompt_with_context(self, user_input: str) -> str:
        """构建包含上下文的完整提示词"""
        # 构建完整的对话上下文
        context_parts = []
        
        # 1. 添加系统提示词
        context_parts.append(f"系统提示：\n{self.system_prompt}\n")
        
        # 2. 添加Few Shot示例
        if self.few_shot_examples:
            context_parts.append("以下是一些对话示例，请参考这种回答风格：\n")
            for i, example in enumerate(self.few_shot_examples, 1):
                context_parts.append(f"示例{i}：")
                context_parts.append(f"用户：{example.user_input}")
                context_parts.append(f"助手：{example.assistant_response}\n")
        
        # 3. 添加对话历史（最近的几轮对话）
        if self.conversation_history:
            context_parts.append("对话历史：")
            # 只保留最近的几轮对话，避免上下文过长
            recent_history = self.conversation_history[-6:]  # 最近6条消息
            for msg in recent_history:
                if msg.role == "user":
                    context_parts.append(f"用户：{msg.content}")
                elif msg.role == "assistant":
                    context_parts.append(f"助手：{msg.content}")
            context_parts.append("")
        
        # 4. 添加当前用户输入
        context_parts.append(f"现在请回答以下问题：\n用户：{user_input}\n助手：")
        
        return "\n".join(context_parts)
    
    def _add_to_history(self, role: str, content: str):
        """添加消息到对话历史"""
        message = ChatMessage(role=role, content=content)
        self.conversation_history.append(message)
        
        # 保持历史长度在合理范围内
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def chat_once(self, user_input: str) -> str:
        """进行一次对话"""
        # 构建带上下文的提示词
        full_prompt = self._build_prompt_with_context(user_input)
        
        # 调用LLM
        try:
            response = self.llm._call(full_prompt)
            
            # 添加到对话历史
            self._add_to_history("user", user_input)
            self._add_to_history("assistant", response)
            
            return response
        except Exception as e:
            error_msg = f"对话出错：{str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def chat_stream(self, user_input: str):
        """进行流式对话"""
        # 构建带上下文的提示词
        full_prompt = self._build_prompt_with_context(user_input)
        
        try:
            import requests
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.llm.api_key.get_secret_value()}"
            }
            
            data = {
                "model": self.llm.model_name,
                "messages": [{"role": "user", "content": full_prompt}],
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
                "top_p": self.llm.top_p,
                "stream": True
            }
            
            response = requests.post(
                f"{self.llm.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            # 流式处理响应
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]  # 移除 'data: ' 前缀
                        if data_str.strip() == '[DONE]':
                            break
                        
                        try:
                            data_json = json.loads(data_str)
                            if 'choices' in data_json and len(data_json['choices']) > 0:
                                delta = data_json['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    chunk = delta['content']
                                    full_response += chunk
                                    yield chunk
                        except json.JSONDecodeError:
                            continue
            
            # 添加到对话历史
            self._add_to_history("user", user_input)
            self._add_to_history("assistant", full_response)
            
        except Exception as e:
            error_msg = f"流式对话出错：{str(e)}"
            print(f"❌ {error_msg}")
            yield error_msg
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
        print("✅ 对话历史已清空")
    
    def save_conversation(self, filename: str):
        """保存对话记录"""
        try:
            conversation_data = {
                "system_prompt": self.system_prompt,
                "few_shot_examples": [
                    {
                        "user_input": ex.user_input,
                        "assistant_response": ex.assistant_response,
                        "description": ex.description
                    }
                    for ex in self.few_shot_examples
                ],
                "conversation_history": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp
                    }
                    for msg in self.conversation_history
                ]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 对话记录已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存对话记录失败：{e}")
    
    def load_conversation(self, filename: str):
        """加载对话记录"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            # 恢复系统提示词
            if "system_prompt" in conversation_data:
                self.system_prompt = conversation_data["system_prompt"]
            
            # 恢复Few Shot示例
            if "few_shot_examples" in conversation_data:
                self.few_shot_examples = [
                    FewShotExample(
                        user_input=ex["user_input"],
                        assistant_response=ex["assistant_response"],
                        description=ex.get("description", "")
                    )
                    for ex in conversation_data["few_shot_examples"]
                ]
            
            # 恢复对话历史
            if "conversation_history" in conversation_data:
                self.conversation_history = [
                    ChatMessage(
                        role=msg["role"],
                        content=msg["content"],
                        timestamp=msg.get("timestamp", time.time())
                    )
                    for msg in conversation_data["conversation_history"]
                ]
            
            print(f"✅ 对话记录已从 {filename} 加载")
        except Exception as e:
            print(f"❌ 加载对话记录失败：{e}")
    
    def show_config(self):
        """显示当前配置"""
        print("🔧 当前配置:")
        print("=" * 50)
        print(f"系统提示词: {self.system_prompt[:100]}...")
        print(f"Few Shot示例数量: {len(self.few_shot_examples)}")
        for i, example in enumerate(self.few_shot_examples, 1):
            print(f"  示例{i}: {example.description}")
        print(f"对话历史长度: {len(self.conversation_history)}")
        print(f"最大历史长度: {self.max_history_length}")


def start_interactive_chat():
    """启动交互式聊天"""
    print("🚀 DeepSeek 交互式聊天")
    print("=" * 60)
    
    # 初始化聊天实例
    chat = DeepSeekInteractiveChat()
    
    # 显示初始配置
    chat.show_config()
    
    print("\n✅ 模型微调完成！")
    print("💡 输入 '/help' 查看可用命令")
    print("💡 输入 '/quit' 退出程序")
    print("💡 直接输入消息开始对话")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n👤 用户: ").strip()
            
            if not user_input:
                continue
                
            # 处理特殊命令
            if user_input.startswith('/'):
                if user_input == '/quit':
                    print("👋 再见！")
                    break
                elif user_input == '/help':
                    show_help()
                elif user_input == '/config':
                    chat.show_config()
                elif user_input == '/clear':
                    chat.clear_history()
                elif user_input.startswith('/save '):
                    filename = user_input[6:].strip()
                    if filename:
                        chat.save_conversation(filename)
                    else:
                        print("❌ 请指定文件名：/save filename.json")
                elif user_input.startswith('/load '):
                    filename = user_input[6:].strip()
                    if filename:
                        chat.load_conversation(filename)
                    else:
                        print("❌ 请指定文件名：/load filename.json")
                else:
                    print("❌ 未知命令，输入 '/help' 查看帮助")
                continue
            
            # 进行流式对话
            print("\n🤖 DeepSeek: ", end="", flush=True)
            
            response_chunks = []
            for chunk in chat.chat_stream(user_input):
                print(chunk, end="", flush=True)
                response_chunks.append(chunk)
            
            print()  # 换行
            
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")


def show_help():
    """显示帮助信息"""
    print("\n📚 可用命令:")
    print("  /help     - 显示此帮助信息")
    print("  /config   - 显示当前配置")
    print("  /clear    - 清空对话历史")
    print("  /save <filename> - 保存对话记录")
    print("  /load <filename> - 加载对话记录")
    print("  /quit     - 退出程序")
    print("\n💡 提示：直接输入消息即可开始对话")


if __name__ == "__main__":
    start_interactive_chat() 