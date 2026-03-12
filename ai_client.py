import os
import requests
from dotenv import load_dotenv

# 初始化设置
# 1.加载环境变量
load_dotenv()

# 2.AI配置模式，(1)本地大模型，(2)在线API，(3) 伪AI输出
USE_LOCAL_LLM = True
USE_ONLINE_API = False
# 本地大模型调用
LOCAL_LLM = os.getenv("USE_LOCAL_LLM", False).lower() == "true"
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost/api/chat")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "deepseek-r1:7b")

# 在线API调用
def get_user_api_key():
    print("\n === 在线API配置 ===")
    key = input("请输入你的api key: ").strip()
    url = input("请输入API地址:").strip()
    model = input("请输入模型名:").strip()
    return key, url,model

def call_online_api(user_input,api_key,api_url,model_name):


