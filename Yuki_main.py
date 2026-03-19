# 导入依赖
import json
import datetime
from default_config import ( #初始人设
    YUKI_STATS, #数值规则
    SYSTEM_CONFIG #系统配置
)
from Events import Trigger
from utils import parse_emotion_change,build_messages
from ai_client import AIClient

#AI模块级别初始化
ai_client = AIClient(mode="local")

# 存档读写
# 1.加载存档
def load_save():
    save_path = SYSTEM_CONFIG["save_path"]
    try: #判断存档是否存在
        with open(save_path,'r',encoding='utf-8') as f:
            save_data = json.load(f) #JSON 转为 Python 字典
        return save_data
    except FileNotFoundError:
        print("正在加载初始化存档...")
        save_data = init_save()
        return save_data

# 2.定义初始化存档

def init_save():
    init_stats = YUKI_STATS["initial"]

    init_data = {
        "meta_info": {
            "save_version": "1.0.0",
            "last_save_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_play_time": "0小时0分钟",
            "save_times": 1
        },
        "player_info": {
            "name": "哥哥",
            "gender":"brother",
            "identity": "医学生",
            "birthday": "02-12",
            "total_chat_times": 0,
            "info_collected":False
        },
        "yuki_core": {
            "basic": {
                "name": "Yuki",
                "current_personality":{
                    "default":True,
                    "dilei":False,
                    "gentle":False,
                    "disease_prone":False,
                    "low":False,
                    "medium":False}
            },
            "stats": {
                "affection": init_stats["affection"],
                "trust": init_stats["trust"],
                "unlocked_events": []
            },
            "current_state": {
                "mood": init_stats["mood"],
                "mood_tag": "happy",
                "action_tag": "idle"
            }
        },
        "interaction": {
            "chat_history": [],
            "date_history": {
                "cafe": 0,
                "park": 0,
                "restaurant": 0,
                "beach": 0
            }
        },
        "content": {
            "diary_list": [],
            "memories": []
        },
        "system": {
            "settings": {
                "tts_volume": 0.8,
                "auto_save": True
            }
        }
    }




    save_save(init_data)
    return init_data

def save_save(save_data):
    save_path = SYSTEM_CONFIG["save_path"]
    # 先更新元信息
    if "meta_info" not in save_data:
        save_data["meta_info"] = {}
    save_data["meta_info"]["last_save_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data["meta_info"]["save_times"] = save_data["meta_info"].get("save_times", 0) + 1

    # 写入文件
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)
    print("存档已成功写入：", save_path)


def collect_user_information(save_data):
    print("\n 首次见面,让Yuki认识一下你吧~")
    while True:
        user_info_name=input("请输入你的名字：").strip()
        if user_info_name:
            break
        print("名字不能为空")
    while True:
        user_info_gender=input("请输入你的性别：brother or sister").strip().lower()
        if user_info_gender in ["brother","sister"]:
            break
        print("输入错误，只能输入brother或sister")

    while True:
        user_info_identity = input("请输入你的身份(比如医学生，程序员等)").strip()
        if user_info_identity :
            break
        print("身份不能为空")

    while True:
        user_info_birthday = input("请输入你的生日(月-日)")
        if "-" in user_info_birthday:
            break
        print("格式不正确")
    save_data["player_info"]["name"] = user_info_name
    save_data["player_info"]["gender"] = user_info_gender
    save_data["player_info"]["identity"] = user_info_identity
    save_data["player_info"]["birthday"] = user_info_birthday
    save_data["player_info"]["info_collected"] = True


    with open(SYSTEM_CONFIG["save_path"], "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)
    print(f"\n欢迎你{user_info_name}哥哥! Yuki已经记住你的信息了")


# 核心功能函数，生成回复
def get_yuki_reply(user_input,save_data):
    messages = build_messages(save_data)
    messages.append({"role":"user","content":user_input})
    response = ai_client.chat(messages)
    return response




#定义聊天主逻辑,核心运行函数
def chat_with_yuki():
    print("===== 欢迎和Yuki聊天～输入「退出」结束对话 =====")
    #1.加载存档
    save_data = load_save()

    #检查是否需要采集用户数据
    if not save_data["player_info"]["info_collected"] :
        collect_user_information(save_data)
        #重新加载存档
        save_data = load_save()


    while True:
        #2.获取用户输入
        user_input = input("\n 你:").strip()




        if user_input == "退出":
            print("Yuki：哥哥下次要早点回来陪我哦～🥺")
            save_save(save_data)
            break

        # 3.生成回复和数值变化
        yuki_response = get_yuki_reply(user_input,save_data)
        aff_change,tru_change = parse_emotion_change(yuki_response)

        # 4.更新数值
        # 4.1 好感度(数值改变，变化范围)
        save_data["yuki_core"]["stats"]["affection"] += aff_change
        save_data["yuki_core"]["stats"]["affection"] = max(0,min(save_data["yuki_core"]["stats"]["affection"],YUKI_STATS["limit"]["affection_max"]))
        #max(0下限,min(input,limits上限))
        # 4.2 心情值(0-10)
        '''save_data["yuki_core"]["current_state"]["mood"] += mood_change'''
        save_data["yuki_core"]["current_state"]["mood"] = max(0,min(save_data["yuki_core"]["stats"]["mood"],100))
        # 4.3 信任值(最大100)
        save_data['yuki_core']["stats"]["trust"] +=tru_change
        save_data["yuki_core"]["stats"]["trust"]= min(save_data["yuki_core"]["stats"]["trust"],100)


        # 5.添加聊天记录到存档
        new_chat = {
            "time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_input":user_input,
            "yuki_reply":yuki_response,
            "stats_change":{
                "affection":aff_change,
                "trust":tru_change
            }
        }
        save_data["interaction"]["chat_history"].append(new_chat)
        # 6.更新总聊天次数
        save_data["player_info"]["total_chat_times"] +=1
        # 7.打印Yuki回复
        print(f'Yuki:{yuki_response}')
        print(f"<好感度{aff_change:+d}>,当前好感度:{save_data["yuki_core"]["stats"]["affection"]}")
        '''print(f"<心情{mood_change:+d}>,当前心情:{save_data["yuki_core"]["current_state"]["mood"]}")'''
        print(f"<信任度{tru_change:+d}>,当前信任度:{save_data["yuki_core"]["stats"]["trust"]}")

        Trigger.event_trigger(save_data)
        # 自动存档
        if SYSTEM_CONFIG["auto_save"]:
            save_save(save_data)

# 测试：加载初始存档
if __name__ == "__main__":
    save_data = load_save()
    current_affection = save_data["yuki_core"]["stats"]["affection"]
    print(f'Yuki current affection:{current_affection}')
    chat_with_yuki()
