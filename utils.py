from default_config import *

#解析函数，从AI输出内容提取好感和信任值变化值，使用正则表达式

import re

def parse_emotion_change(ai_response):
    #解析AI回复里的<好感变化:+X><信任变化:+Y>,返回(好感变化值，信任变化值)
    affection_pattern = re.compile(r'<好感变化:([+-]?\d+)>')
    trust_pattern = re.compile(r'<信任变化:([+-]?\d+)>')

    #提取数值
    affection_change = affection_pattern.search(ai_response)
    trust_change = trust_pattern.search(ai_response)

    #转换为整数，防止生成格式错误
    try :
        aff_change = int(affection_change.group(1)) if affection_change else 0
        tru_change = int(trust_change.group(1)) if trust_change else 0
    except :
        aff_change = 0
        tru_change = 0

    #限制数值范围在[-2,2]
    aff_change = max(min(aff_change, 2), -2)
    tru_change = max(min(tru_change, 2), -2)
    return aff_change,tru_change

# 构建AI输入参数中的messages
def build_messages(save_data,max_context = 10):
    for persona in YUKI_CHARACTER["personality"]:
        if save_data["yuki_core"]["basic"]["current_personality"][persona]:
            current_personality = persona
    system_prompt = f"""
    你的人设信息：{PERSONALITY_PROMPTS[current_personality]}
    当前好感度:{save_data["yuki_core"]["stats"]["affection"]}
    当前信任值:{save_data["yuki_core"]["stats"]["trust"]}
    当前心情：{save_data["yuki_core"]["current_state"]["mood_tag"]},心情数值为{save_data["yuki_core"]["stats"]["mood"]}
    (心情数值说明:心情数值0-10，比如当心情数值为3，心情标签为happy，表示有点开心，
    当心情数值为9，心情标签为happy,表示非常开心，通过心情标签和心情数值共同调整说话语气)
    输出规则：参考人设信息中的”create_notes"
    对话案例：
            "用户：你好烦啊"
            "Yuki：呜...哥哥是不是讨厌我了🥺<好感变化:-2><信任变化:-1>",

            "用户：今天带你去吃好吃的"
            "Yuki：哇！谢谢哥哥～😋<好感变化:+2><信任变化:+1>",

            "用户：今天天气不错"
            "Yuki：嗯嗯～和哥哥聊天，天气都变好了✨<好感变化:+1><信任变化:+0>"
""".strip()
    messages = [
        {"role":"system","content":system_prompt},
    ]
