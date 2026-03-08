def load_save():
    save_path = SYSTEM_CONFIG["save_path"]
    try: #判断存档是否存在
        with open(save_path,'r',encoding='utf-8') as f:
            save_data = json.load(f) #JSON 转为 Python 字典
        return save_data
    except FileNotFoundError:
        print("正在加载初始化存档...")
        save_data = init_data()
        return save_data

        "player_info": {
            "name": "哥哥",
            "gender":"brother",
            "identity": "医学生",
            "birthday": "02-12",
            "total_chat_times": 0,
            "info_collected":False}

def collect_user_information(save_data):
        user_info_name=input("请输入你的名字：")
        user_info_gender=input("请输入你的性别：brother or sister")
        user_info_identity = input("请输入你的身份：")
        user_info_birthday = input("请输入你的生日:")
        save_data["player_info"]["name"] = user_info_name
        save_data["player_info"]["gender"] = user_info_gender
        save_data["player_info"]["identity"] = user_info_identity
        save_data["player_info"]["birthday"] = user_info_birthday
        save_data["player_info"]["info_collected"] = True

def chat_with_yuki():
    print("===== 欢迎和Yuki聊天～输入「退出」结束对话 =====")
    #1.加载存档
    save_data = load_save()


    while True:
        if not save_data["player_info"]["info_collected"]:
            collect_user_information(save_data)
            continue

        #2.获取用户输入
        user_input = input("\n 你:")
        ......






