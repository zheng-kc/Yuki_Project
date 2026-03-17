# 存档
存档需要把整个游戏中的可变参数写入，在init_data中要将存档所有内容全部写入，只有文字内容可以留空  
# STM(状态机)
事件触发，人设改变等可以影响游戏进程的参数应该通过STM机制改变  
{yuki_core:{current_personality:{"default":true,"gentle":false.....}}}
# 关于数值变化
通过提示词，将数值变化交给AI，让AI判断好感度是加还是减  
通过正则解析匹配定位数值变化 utils.py
关于心情，采用数值控制强度，标签判断类型
关于心情输出，让AI输出标签和数值？
是否取消mood_change,改为直接输出数值？

# 关于事件和功能
将事件触发代码写入Event.py中的Trigger类中，将Yuki_main.py中的事件触发代码移入，
将save中的unlocked_events改为字典，即状态触发，主代码调用Trigger代码  
事件代码和功能代码分开  
事件是指依据条件自动触发，只是一个事件解锁提示  
功能是指用户输入，用户自己触发，属于操作性代码  
功能作为底层，事件作触发  
例如日记功能，解锁日记功能，偷看日记属于事件代码  
执行日记功能，属于功能代码 


# 关于事件触发规则
mood数值（0-10）不控制事件触发，只通过数值和标签用提示词控制说话语气

# 关于大模型调用
1. 本地大模型调用，用于测试代码和prompt
2. 在线API调用，设置接口，可以随时更改，将用户API密钥储存至`default.py`中的API_CONFIG，
3. 输入大模型的messages构成：
``` messages = [
{"role" : "system","content" : "人设，规则，好感，心情，当前状态"},
{"role" : "user","content" : user_input},
{"role" : "assistant","content" : AI输出}
] 
```
人设信息+好感度+心情+信任值+输出规则+memory+输出例子 

# 编写原则和顺序
1. 对话和人设系统
- 对话基本规则已完成，现在要创建AI接口，编写`ai_client.py`代码，使用本地大模型(deepseek-r1:7b)进行测试
创建env文件储存API密钥
- 人设切换，在`init_data`中将所有personality加入，使用STM管理
- 好感度，信任值使用AI输出，正则化判断变化，心情值使用标签+数值控制，编写Prompt “心情标签 + 数值映射表”
- 关于对话的Prompt，区分chat_history和memory
chat_history存储所有对话，memory存储最后N条对话，继续对话时使用memory中的对话数据，防止prompt过长影响对话效果
将人设标签名称全部统一，防止程序无法索引


