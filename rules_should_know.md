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
事件触发改为状态机,init_data中unlocked_events要改,DiarySystem中的check代码要改
# 关于复杂人设触发  
采用白名单机制，我默认认为这个人是合格的（is_match = True）。除非我发现他违反了某条明确的规则，那我就把他踢出去（is_match = False）。”  
优点：代码结构清晰，每增加一条规则，只需要多写一个独立的 if 块，互不干扰。  
白名单内的人设放入白名单列表，进行优先级策略机制，创建一个优先级列表，白名单列表根据优先级列表进行排序，最后在白名单列表中取第一个人设

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
- 人设切换，在`init_data`中将所有personality加入，使用STM和白名单机制管理
- 好感度，信任值使用AI输出，正则化判断变化，心情值使用标签+数值控制，编写Prompt “心情标签 + 数值映射表”
- 关于对话的Prompt，区分chat_history和memory
chat_history存储所有对话，memory存储最后N条对话，继续对话时使用memory中的对话数据，防止prompt过长影响对话效果
将人设标签名称全部统一，防止程序无法索引

# 关于记忆系统
暂时采用一律索取chat_history的最后10条对话作为memory
以后逐渐加入滑窗机制，LTM的定期摘要 + 关键词检索

# 关于人设prompt
将输出规则放到creator_note，防止日记系统调用人设时发生冲突
为了防止对话规则和日记规则发生冲突，先添加RULES列表管理规则，将通用人设prompts留在PERSONALITY_PROMPTS

# notes
主代码中的数值类(affection,trust)需要强行int()转换  
标准的分层架构思想：  
main.py (控制层/入口)：负责“组装”和“调度”。它决定用什么模型（实例化 AIClient），什么时候触发日记生成，以及拿到结果后做什么（保存、打印）。  
DiarySystem (逻辑层/工具类)：负责“具体怎么做”。它不关心模型是哪来的，只关心“给我一个能说话的客户端，我就能写出日记”。  
这种分工让代码非常清晰，维护起来也轻松。
日记彩蛋return?
直接reformat code直接干掉缩进问题

# Next step:
~~将日记功能整合至Yuki_main.py~~  
~~更改事件触发逻辑，将原来的添加事件名改为STM管理~~  
编写RULE中的日记规则