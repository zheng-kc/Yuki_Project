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
