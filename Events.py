import datetime
from default_config import (YUKI_STATS,YUKI_CHARACTER)

# 将所有事件触发逻辑功能添加至Events.py中，Yuki_main直接调用即可
class Trigger:
    def __init__(self,save_data):
        self.save_data = save_data

    def event_trigger(self):
        #事件解锁触发
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
        for persona in YUKI_CHARACTER["personality"]:
            if self.save_data["yuki_core"]["basic"]["current_personality"][persona]:
                continue
            if current_affection


    def diary_leak_trigger(self):#偷看日记事件触发







