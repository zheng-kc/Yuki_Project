import requests
from dotenv import load_dotenv
import os
from openai import OpenAI,APIError,APITimeoutError
import re

# 初始化设置
# 1.加载环境变量
load_dotenv()

# 2.AI配置模式，(1)本地大模型，(2)在线API，(3) 伪AI输出

"""接入线上和本地大模型，本地用于测试AI代码逻辑(正则，好感度输出数值等)
线上大模型用于将来修正Prompts"""

class AIClient:
    def __init__(self,mode="local"):
        self.mode = mode
        #线上API调用
        self.deepseek_api_key = os.getenv("OPENAI_API_KEY")
        self.online_client = OpenAI(
            api_key = self.deepseek_api_key,
            base_url = "https://api.deepseek.com/v1",
            timeout = 60
        ) if self.deepseek_api_key else None
        # 本地大模型调用(复用Openai的SDK)
        self.local_client = OpenAI(
            api_key = "ollama",
            base_url = "http://localhost:11434/v1",
            timeout = 120
        )


    def change_mode(self,mode):
        """切换本地/线上模式"""
        if mode == "online" and not self.deepseek_api_key:
            return "Error occurs,deepseek api key was not found"
        self.mode = mode
        return f"已切换到{'本地模式' if mode == 'local' else '线上模式'}"

    # 使用正则化去除<think>,</think>字段,非流式处理
    def clean_think_tags(self,text : str) -> str:
        # 内部辅助方法：去除 think 标签
        if not text:
            return ""
        # 使用非贪婪匹配去除 <think>...</think>
        pattern = r"<think>.*?</think>"
        cleaned = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
        return cleaned.strip()

    def chat(self,messages,model = None, stream = False):
        """聊天接口统一"""
        client = self.local_client if self.mode == "local" else self.online_client
        model = model or ("deepseek-r1:7b" if self.mode == "local" else "deepseek-chat")

        try:
            response = client.chat.completions.create(
                model = model,
                messages = messages,
                stream = stream,
                temperature = 0.7
            )
            # 流式处理,实现打字机效果
            if stream:
                def stream_gen():# 定义生成器函数
                    in_think_block = False
                    for chunk in response:
                        content = None

                        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                            if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                                content = chunk.choices[0].delta.content
                        if not content:
                            continue

                        if "<think>" in content:
                            in_think_block = True
                            content = content.split("<think>")[0]

                        if in_think_block:
                            # 检查是否结束思考
                            if "</think>" in content:
                                in_think_block = False
                                # 截取 </think> 之后的内容
                                content = content.split("</think>")[-1]
                            else:
                                # 还在思考中，直接丢弃整个 chunk
                                continue
                            if content and content.strip():
                                yield content

                return stream_gen()
            else:
                return self.clean_think_tags(response.choices[0].message.content)

        except APITimeoutError:
            return "请求超时"
        except APIError as e:
            return f"API错误:{e.message}"
        except Exception as e:
            return f"错误:{str(e)}"

    '''def mock_chat(self):
        # 测试函数，先使用伪AI回复，测试JSON读写是否正常
        """
            接收用户输入，返回Yuki的回复 + 数值变化
            （先写简化版，后续替换成真实AI接口）
            """
        # 1. 定义简单的关键词匹配（模拟AI逻辑）
        if "可爱" in user_input or "好看" in user_input:
            reply = "谢谢哥哥的夸奖😘，Yuki超开心的！"
            affection_change = YUKI_STATS["change_rule"]["praise"]  # 从配置读+5
            mood_change = 3
            trust_change = 5
        elif "其他女生" in user_input or "别的妹妹" in user_input:
            reply = "呜😭...哥哥是不是不喜欢Yuki了？不准提别的女生！"
            affection_change = YUKI_STATS["change_rule"]["mention_other_girl"]  # 从配置读-10
            mood_change = -10
            trust_change = -10
        elif "吃饭" in user_input or "吃什么" in user_input:
            reply = "Yuki想和哥哥一起吃草莓蛋糕～🍰"
            affection_change = YUKI_STATS["change_rule"]["chat"]  # 从配置读+1
            mood_change = 2
            trust_change = 3
        else:
            reply = "哥哥说的话Yuki不太懂～但会乖乖听的✨"
            affection_change = YUKI_STATS["change_rule"]["chat"]  # 从配置读+1
            mood_change = 0
            trust_change = 0

        # 2. 返回回复和数值变化
        return {
            "reply": reply,
            "affection_change": affection_change,
            "mood_change": mood_change,
            "trust_change": trust_change
        }'''




