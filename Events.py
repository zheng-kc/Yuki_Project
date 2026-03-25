import datetime
from default_config import (YUKI_STATS,YUKI_CHARACTER)

# 将所有事件触发逻辑功能添加至Events.py中，Yuki_main直接调用即可
class Trigger:
    def __init__(self,save_data):
        self.save_data = save_data

    def event_trigger(self):
        #事件解锁触发,STM规则
        # 4.4 事件解锁
        current_affection = self.save_data["yuki_core"]["stats"]["affection"]
        current_trust = self.save_data["yuki_core"]["stats"]["trust"]
        for event in YUKI_STATS["event_trigger"]:
            event_name = event["event_name"]
            # 跳过已解锁的事件
            if self.save_data["yuki_core"]["stats"]["unlocked_events"][event_name]:
                continue
            #检查是否满足条件
            if current_affection >= event["affection_min"] and current_trust >= event["trust_min"]:
                self.save_data["yuki_core"]["stats"]["unlocked_events"][event_name] = True
                print(f'\n解锁新事件:{event_name}')

    def persona_trigger(self):#人设personality触发
        current_affection = self.save_data["yuki_core"]["stats"]["affection"]
        current_trust = self.save_data["yuki_core"]["stats"]["trust"]
        trigger_personality = []
        current_personality = self.save_data["yuki_core"]["basic"]["current_personality"]
        for persona,conditions in YUKI_STATS["personality_trigger"].items():
            if self.save_data["yuki_core"]["basic"]["current_personality"].get(persona,False):
                continue
            #[条件检查],小开关,白名单机制
            is_match = True

            # 检查下限(affection_min,trust_min)
            if "affection_min" in conditions:
                if current_affection < conditions["affection_min"]:
                    is_match = False
            if "trust_min" in conditions:
                if current_trust < conditions["trust_min"]:
                    is_match = False

            #检查上限
            if "affection_max" in conditions:
                if current_affection >= conditions["affection_max"]:
                    is_match = False
            if "trust_max" in conditions:
                if current_trust >= conditions["trust_max"]:
                    is_match = False

            if is_match:
                trigger_personality.append(persona)

        # 2. 处理触发逻辑 (互斥核心)
        new_persona_active = None

        if trigger_personality:
            # 【优先级策略】：列表中的第一个人设为最高优先级
            # 如果你的配置字典是无序的，建议在这里根据“稀有度”或“数值要求”排序
            # 这里简单取第一个匹配到的
            priority_order = ["disease_prone","dilei","gentle","medium","low","default"]
            trigger_personality.sort(key=lambda x: priority_order.index(x) if x in priority_order else 999)
            new_persona_active = trigger_personality[0]

            print(f"✨ 触发妹妹的新人设：[{new_persona_active}] (好感:{current_affection}, 信任:{current_trust})")

            # 【互斥操作】：关闭所有其他人设
            for p_key in current_personality.keys():
                current_personality[p_key] = False

            # 激活选中的人设
            current_personality[new_persona_active] = True

        else:
            # 【保底逻辑】：如果没有触发任何特殊人设
            # 检查当前是否没有任何人设被激活（包括 default）
            if not any(current_personality.values()):
                # 强制激活 default
                current_personality["default"] = True
                print("未满足特殊人设条件，重置为 [default] 人设")

            # 如果当前已经是某个特殊人设，但不再满足条件了，要不要切回 default？
            # 如果需要“一旦触发就永久保留直到满足更低条件”，则不需要下面的逻辑
            # 如果需要“实时动态切换”，则解开下面注释：
            """
            current_active = [k for k, v in current_personality.items() if v and k != 'default']
            if current_active:
                # 曾经激活的特殊人设现在不满足了，切回 default
                for p_key in current_personality.keys():
                    current_personality[p_key] = False
                current_personality["default"] = True
                print("⚠️ 特殊人设条件不再满足，降级为 [default]")
            """







    '''def diary_leak_trigger(self):#偷看日记事件触发'''








