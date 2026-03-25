from default_config import *

#解析函数，从AI输出内容提取好感和信任值变化值，使用正则表达式

import re
import datetime

def parse_emotion_change(ai_response):
    #解析AI回复里的<好感变化:+X><信任变化:+Y><当前心情:[Z]>,返回(好感变化值，信任变化值),当前心情标签
    affection_pattern = re.compile(r'<好感变化:([+-]?\d+)>')
    trust_pattern = re.compile(r'<信任变化:([+-]?\d+)>')
    mood_context = r'<当前心情:\[(.*?)]>'

    #提取数值
    affection_change = affection_pattern.search(ai_response)
    trust_change = trust_pattern.search(ai_response)
    #提取标签
    mood_match = re.search(mood_context,ai_response)

    #转换为整数，防止生成格式错误
    try :
        aff_change = int(affection_change.group(1)) if affection_change else 0
        tru_change = int(trust_change.group(1)) if trust_change else 0
    #提取标签
        current_mood = mood_match.group(1) if mood_match else "平静"
    except :
        aff_change = 0
        tru_change = 0
        current_mood = "平静"

    #限制数值范围在[-2,2]
    aff_change = max(min(aff_change, 2), -2)
    tru_change = max(min(tru_change, 2), -2)
    return aff_change,tru_change,current_mood

# 构建AI输入参数中的messages
def build_messages(save_data,max_context = 10):
    current_persona = save_data["yuki_core"]["basic"]["current_personality"]
    # 获取激活人设,使用更简洁的代码
    persona_name = "default"
    for p, is_active in current_persona.items():
        if is_active:
            persona_name = p
            break
    system_prompt = f"""
    你的人设信息：{PERSONALITY_PROMPTS[persona_name]}
    用户信息: 姓名：{save_data["player_info"]["name"]},关系:{save_data["player_info"]["gender"]},身份:{save_data["player_info"]["identity"]},生日:{save_data["player_info"]["birthday"]}
    当前好感度:{save_data["yuki_core"]["stats"]["affection"]}
    当前信任值:{save_data["yuki_core"]["stats"]["trust"]}
    当前心情：{save_data["yuki_core"]["current_state"]["current_mood"]}
    (心情标签可以是单一心情，如[开心],也可以是混合心情,如[伤心且不安])
    输出规则：{RULES[persona_name]["chat"]}
    对话案例：
            "用户：你好烦啊"
            "Yuki：呜...哥哥是不是讨厌我了🥺<好感变化:-2><信任变化:-1><当前心情:[伤心且不安]>",

            "用户：今天带你去吃好吃的"
            "Yuki：哇！谢谢哥哥～😋<好感变化:+2><信任变化:+1><当前心情:[开心]>",

            "用户：今天天气不错"
            "Yuki：嗯嗯～和哥哥聊天，天气都变好了✨<好感变化:+1><信任变化:+0><当前心情:[平静且欣慰]>"
""".strip()
    messages = [
        {"role":"system","content":system_prompt},
]
    chat_history = save_data["interactions"]["chat_history"]
    memory = chat_history[-max_context:] if chat_history else []
    # 将memory加入messages
    for chat in memory:
        user_msg = chat["user_input"]
        yuki_msg = chat["yuki_reply"]
        messages.append({"role":"user","content":user_msg})
        messages.append({"role":"assistant","content":yuki_msg})
    return messages


# 计时功能
def calculate_total_play_time(save_data):
    # 根据聊天历史计算总游戏时间，返回格式:"X小时Y分钟"
    chat_history = save_data.get("interactions",{}).get("chat_history",[])

    #如果没有聊天记录，返回0小时0分钟
    if not chat_history:
        return "0小时0分钟"
    try:
        # 获取第一条和最后一条聊天记录的时间
        first_time_str = chat_history[0]["time"]
        last_time_str = chat_history[-1]["time"]

        # 转换为datetime对象
        first_time = datetime.datetime.strptime(first_time_str,"%Y-%m-%d %H:%M:%S")
        last_time = datetime.datetime.strptime(first_time_str,"%Y-%m-%d %H:%M:%S")

        # 计算时间差
        time_diff = last_time - first_time

        #转换为分钟
        total_minutes = int(time_diff.total_seconds()/60)

        # 计算小时和分钟
        hours = total_minutes // 60
        minutes = total_minutes % 60

        return f"{hours}小时{minutes}分钟"
    except (KeyError, ValueError, IndexError):
        return "计时失效，重置为0小时0分钟"

