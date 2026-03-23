import datetime
from default_config import (PERSONALITY_PROMPTS, RULES)


class DiarySystem:
    def __init__(self, save_data,ai_client):
        self.save_data = save_data
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.ai_client = ai_client
        self.unlock_event_name = "解锁查看<日记>功能"

    def check_diary_unlocked(self):
        unlocked_events = self.save_data["yuki_core"]["stats"]["unlocked_events"]
        return unlocked_events["解锁查看<日记>功能"]  # 这个返回True or False，在日记主功能中if判断即可

    def show_diary(self):
        #if not self.check_diary_unlocked():
            #return "日记功能未解锁"

        diary_list = self.save_data["content"]["diary_list"]
        if not diary_list:
            return "暂无日记记录"

        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_diary = [d for d in diary_list if d["date"] == yesterday]
        if not yesterday_diary:
            return "昨天没有写日记呢"
        return f"Yuki的日记\n【{yesterday}】\n{yesterday_diary[0]['content']} "

    def generate_diary_content(self):
        # 删除伪AI生成，采用AI生成
        chat_history = self.save_data["interactions"].get("chat_history", [])

        # 提取今天的对话
        today_chats = [c for c in chat_history if c.get("time", "").startswith(self.today)]

        # 获取当前人设，好感度，信任值，心情
        current_persona = self.save_data["yuki_core"]["basic"]["current_personality"]
        # 获取激活人设
        persona_name = "default"
        for p, is_active in current_persona.items():
            if is_active:
                persona_name = p
                break
        persona_active_prompt = PERSONALITY_PROMPTS[persona_name]

        # 构建messages参数
        system_prompt = f'''
        你的人设信息:{persona_active_prompt}
        用户信息: 姓名：{self.save_data["player_info"]["name"]},关系:{self.save_data["player_info"]["gender"]},身份:{self.save_data["player_info"]["identity"]},生日:{self.save_data["player_info"]["birthday"]}
        当前好感度:{self.save_data["yuki_core"]["stats"]["affection"]}
        当前信任值:{self.save_data["yuki_core"]["stats"]["trust"]}
        输出规则:{RULES[persona_name]["diary_rules"]}
        你是Yuki，请根据你的人设，当前好感度，当前信任值，输出一篇妹妹第一人称视角下的日记,字数在500字左右
        日记风格要符合你的人设，体现当下的情绪。
        不要出现'聊天记录'、'对话'等打破第四面墙的词汇，要像是在私下记录心事。
        '''

        if not today_chats:
            return "今天哥哥没有和我对话呢"

        # 获取对话内容
        chat_content = ""
        for c in today_chats[-10:]:
            user_input = c.get("user_input", "")
            yuki_reply = c.get("yuki_reply", "")
            chat_content += f"{self.save_data['player_info']['name']}:{user_input}\nYuki:{yuki_reply}\n"

        user_prompt = f'''
        今天是{self.today}\n,
        互动对话是{chat_content}\n
        请开始写日记：'''

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 尝试调用AI openai SDK
        try:
            if self.ai_client:  # 存在AI代理实例
                response = self.ai_client.chat(messages)
                return response.strip()
            else:
                return self._get_mock_content("has_chat", today_chats[-1])
        except Exception as e:
            print(f"[DiarySystem生成日记失败]{e}")
            return self._get_mock_content("error")

    # 伪AI输出兜底函数
    def _get_mock_content(self, scenario, last_chat=None):
        if scenario == "no_chat":
            return "今天哥哥一直没有来找我，房间里好安静...我都在想哥哥在忙什么呢？(´• ω •`) "
        elif scenario == "has_chat" and last_chat:
            return f"今天最好和哥哥聊了: \"{last_chat['user_input']}\"，我回答了 \"{last_chat['yuki_reply']}\"。好感度:{self.save_data['yuki_core']['stats']['affection']}，开心！"
        else:
            return "今天发生了一些事，我都记在心里啦。"

    def save_diary(self):
        """生成并保存日记，重构版"""
        # 1. 前置检查：如果没解锁，直接在这里返回，后面代码都不执行
        #if not self.check_diary_unlocked():
            #return False, "查看日记功能未解锁"

        # 2. 获取或初始化列表
        diary_list = self.save_data["content"].setdefault("diary_list", [])

        # 3. 检查今天是否已写
        for entry in diary_list:
            if entry.get("date") == self.today:
                return False, "今天的日记写好了"

        # 4. 生成内容
        content = self.generate_diary_content()

        # --- 关键修改点开始 ---
        # 我们不再分两行写 (append 然后 return)，而是直接在一个逻辑块里完成
        # 这样即使缩进有点小问题，也不会报 "unindent" 错误，因为没有独立的 return 行需要去匹配

        try:
            # 直接执行写入
            diary_list.append({"date": self.today, "content": content})

            # 立即返回成功信息 (确保这行和 append 在同一视觉层级)
            return True, "日记已生成"
        except Exception as e:
            # 如果上面出错，捕获异常并返回错误信息，避免程序崩溃
            return False, f"保存失败: {str(e)}"
        # --- 关键修改点结束 ---


def check_eggs(self):
    # ... 原有逻辑保持不变 ...
    if not self.check_diary_unlocked():
        return None
    diary_list = self.save_data["content"].get("diary_list", [])
    if not diary_list:
        return None
    # 这里可以继续写彩蛋逻辑
    return None
