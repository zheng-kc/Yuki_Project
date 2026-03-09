import datetime
from default_config import (YUKI_STATS,YUKI_CHARACTER)

class DiarySystem:
    def __init__(self,save_data,character_config):
        self.save_data = save_data
        self.character_config = character_config
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.unlock_event_name = "解锁查看<日记>功能"


    def check_diary_unlocked(self):
        unlocked_events = self.save_data["yuki_core"]["stats"]["unlocked_events"]
        return self.unlock_event_name in unlocked_events #这个返回True or False，在日记主功能中if判断即可

    def show_diary(self):
        if not self.check_diary_unlocked():
            return "日记功能未解锁"

        diary_list = self.save_data["content"]["diary_list"]
        if not diary_list :
            return "暂无日记记录"

        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_diary = [d for d in diary_list if d["date"] == yesterday]
        if not diary_list:
            return "昨天没有写日记呢"
        return f"Yuki的日记\n【{yesterday}】\n{yesterday_diary[0]["content"]} "


    def generate_diary_content(self):
        chat_history = self.save_data["interactions"]["chat_history"]
        today_chats = [c for c in chat_history if c["time"].starts_with(self.today)]
        if not today_chats:
            return "今天哥哥没有和我聊天，有点孤独呢~"
        last_chat = today_chats [-1]
        affection = self.save_data["yuki_core"]["stats"]["affection"]
        return f"今天最好和哥哥聊了: {last_chat["user_input"],last_chat["yuki_reply"],affection}"

    def save_diary(self):
        if not self.check_diary_unlocked():
            return False,"查看日记功能未解锁"
        diary_list = self.save_data["content"]["diary_list"]
        # 当天只写一篇
        if any(d["date"] == self.today for d in diary_list):
            return False, "今天的日记写好了"
        diary_content = self.generate_diary_content()
        diary_list.append({"date":self.today,"content":diary_content})
        return True,"日记已生成"

    def check_eggs(self,user_input):
        if not self.check_diary_unlocked():
            return None
        diary_list = self.save_data["content"]["diary_list"]
        if not diary_list:
            return None