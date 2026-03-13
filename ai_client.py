import requests
from dotenv import load_dotenv
import os
from openai import OpenAI,APIError,APITimeoutError

# 初始化设置
# 1.加载环境变量
load_dotenv()

# 2.AI配置模式，(1)本地大模型，(2)在线API，(3) 伪AI输出

"""接入线上和本地大模型，本地用于测试AI代码逻辑(正则，好感度输出数值等)
线上大模型用于将来修正Prompts"""

class AIClient:
    def __init__(self,mode="local"):
        #本地大模型调用
        self.mode = mode
        self.ollama_url = "http://localhost:11434"
        self.ollama_model = "deepseek-r1:7b"
        #线上API调用
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.online_client = OpenAI(
            api_key = self.deepseek_api_key,
            base_url = "https://api.deepseek.com",
            timeout = 60
        ) if self.deepseek_api_key else None

    def change_mode(self,mode):
        """切换本地/线上模式"""
        if mode == "online" and not self.deepseek_api_key:
            return "Error occurs,deepseek api key was not found"
        self.mode = mode
        return f"已切换到{'本地模式' if mode == 'local' else '线上模式'}"

    def chat(self,messages,model = None, stream = False):
        """聊天接口统一"""
        if self.mode == "local":
            return self.call_local(messages,model,stream)
        else:
            return self.call_online(messages,model,stream)

    def call_local(self,messages,model='deepseek-r1:7b',stream=False):
        """调用本地模型Ollama"""
        """ollama的HTTP请求体Payload"""
        try:
            payload = {
                "model":model,
                "messages":messages,
                "stream":stream
            }
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result['message']['content']
        except requests.exceptions.ConnectionError:
            return "本地部署未启动，运行Ollama serve"
        except Exception as e:
            return f"本地模型错误:{str(e)}"

    def call_online(self, messages, model="deepseek-chat", stream=False):
        """调用线上 DeepSeek（推荐用 SDK）"""
        if not self.online_client:





