# DeepSeek LangChain Integration

一个简洁高效的DeepSeek API与LangChain集成模块。

## 功能特性

- 🚀 **完整的LangChain集成**：支持标准的LLM接口
- 🎯 **多模型支持**：包括DeepSeek Chat和Code模型  
- 🔄 **流式输出**：支持实时响应流
- 🛠️ **统一工具**：集成安装、测试、示例功能
- 📦 **开箱即用**：一键安装和测试

## 快速开始

### 方式一：使用统一工具（推荐）

```bash
# 显示帮助
python main.py help

# 安装依赖
python main.py install

# 完整测试
python main.py test

# 运行示例
python main.py examples
```

### 方式二：直接使用

```bash
# 安装依赖
python install_unified.py

# 测试功能
python test_all.py

# 运行示例
python test_all.py --examples
```

## 快速开始

### 基础用法

```python
from deepseek_llm import DeepSeekLLM

# 初始化模型
llm = DeepSeekLLM(
    api_key="your-api-key",
    temperature=0.7,
    max_tokens=1024
)

# 生成响应
response = llm.invoke("解释一下什么是机器学习？")
print(response)
```

### 聊天模型

```python
from deepseek_llm import DeepSeekChat

# 初始化聊天模型
chat_llm = DeepSeekChat(
    api_key="your-api-key",
    temperature=0.5
)

response = chat_llm.invoke("你好，请介绍一下你自己")
print(response)
```

### 代码生成

```python
from deepseek_llm import DeepSeekCode

# 初始化代码模型
code_llm = DeepSeekCode(
    api_key="your-api-key",
    temperature=0.2
)

response = code_llm.invoke("请写一个Python函数来计算斐波那契数列")
print(response)
```

### LangChain链式调用

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from deepseek_llm import DeepSeekLLM

# 创建LLM和提示模板
llm = DeepSeekLLM(api_key="your-api-key")
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请用简洁的语言解释以下概念：{topic}"
)

# 创建链
chain = prompt | llm | StrOutputParser()

# 执行链
response = chain.invoke({"topic": "区块链技术"})
print(response)
```

### 流式输出

```python
from deepseek_llm import DeepSeekLLM

llm = DeepSeekLLM(api_key="your-api-key")

# 流式生成
for chunk in llm.stream("请写一首关于春天的诗"):
    print(chunk.text, end="", flush=True)
```

## 配置说明

### API密钥设置

有多种方式设置API密钥：

1. **直接传参**（推荐用于测试）：
```python
llm = DeepSeekLLM(api_key="your-api-key")
```

2. **环境变量**：
```bash
export DEEPSEEK_API_KEY="your-api-key"
```

3. **配置类**：
```python
from deepseek_llm import DeepSeekConfig

# 查看当前配置
print(DeepSeekConfig.get_api_key())
print(DeepSeekConfig.get_base_url())
```

### 模型参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `temperature` | 0.7 | 控制输出随机性 (0-1) |
| `max_tokens` | 1024 | 最大输出token数 |
| `top_p` | 0.95 | 核采样参数 |
| `model_name` | "deepseek-chat" | 模型名称 |

### 可用模型

- `deepseek-chat`: 通用对话模型
- `deepseek-coder`: 代码生成模型

## 运行示例

```bash
# 使用统一工具
python main.py examples

# 或直接使用测试工具
python test_all.py --examples
```

示例代码包含：
- 基础LLM调用
- 聊天模型使用
- LangChain链式调用
- 完整的测试验证

## 错误处理

模块包含完整的错误处理机制：

```python
try:
    response = llm.invoke("你的问题")
    print(response)
except RuntimeError as e:
    print(f"API调用错误: {e}")
```

## 项目结构

```
deepseek/
├── main.py                # 统一入口文件
├── deepseek_llm.py        # 核心模块（包含配置）
├── install_unified.py     # 安装工具
├── test_all.py           # 测试工具（包含示例）
├── requirements.txt      # 依赖清单
├── setup.py             # 包安装脚本
├── __init__.py          # 模块初始化
└── README.md            # 文档
```

## 工具命令

### 统一工具 (main.py)

```bash
# 基础功能
python main.py install                    # 安装核心依赖
python main.py install --all              # 安装所有依赖
python main.py install --mirror aliyun    # 使用阿里云镜像

python main.py test                       # 完整测试
python main.py test --deps-only           # 仅检查依赖
python main.py test --api-only            # 仅测试API

python main.py examples                   # 运行示例
python main.py chat                       # 启动交互式聊天
python main.py help                       # 显示帮助
```

### 独立工具

```bash
# 安装工具
python install_unified.py                 # 核心依赖
python install_unified.py --all           # 所有依赖
python install_unified.py --mirror tsinghua   # 清华镜像

# 测试工具
python test_all.py                        # 完整测试
python test_all.py --deps-only            # 仅检查依赖
python test_all.py --api-only             # 仅测试API
python test_all.py --examples             # 运行示例
```

## 注意事项

1. 确保API密钥有效且有足够的配额
2. 网络连接稳定，API调用可能需要时间
3. 流式输出需要逐chunk处理
4. 建议在生产环境中使用环境变量管理API密钥

## 🔥 新增功能

### 交互式聊天
```bash
python main.py chat
```

支持以下功能：
- 🎯 **Prompt微调**：内置可修改的系统提示词
- 📚 **Few Shot学习**：支持最多3个示例来微调模型行为
- 💬 **实时流式对话**：支持流式输出和实时显示
- 📝 **对话历史管理**：自动保存和管理对话上下文
- 🔧 **配置管理**：可保存和加载对话配置

### 特色功能

1. **智能提示词构建**：自动将系统提示词、Few Shot示例和对话历史组合成完整的上下文
2. **流式输出**：实时显示AI响应，提供更好的用户体验
3. **命令系统**：支持`/help`、`/config`、`/clear`等命令
4. **会话管理**：可以保存和加载对话记录

## 🔧 如何上传到GitHub

详细的GitHub上传指南请参考：[GitHub上传指南](github_upload_guide.md)

### 快速上传步骤

1. 安装Git：从 https://git-scm.com/download/win 下载
2. 配置Git用户信息：
   ```bash
   git config --global user.name "你的姓名"
   git config --global user.email "你的邮箱"
   ```
3. 初始化并上传：
   ```bash
   git init
   git add .
   git commit -m "Initial commit: DeepSeek LangChain Integration"
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

## 许可证

本项目仅用于学习和演示目的。请遵守DeepSeek API的使用条款。 