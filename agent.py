from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools import get_weather, search_attractions, search_food, plan_route, calculate_budget
from langgraph.checkpoint.memory import MemorySaver
import os
import datetime

# 配置模型
llm = ChatOpenAI(
    model="glm-4-flash",
    api_key=os.getenv("ZHIPU_API_KEY", "343c5a1e09dc45ab82b154df0a583129.QjGtXIauW1IkVhzA"),
    base_url="https://open.bigmodel.cn/api/paas/v4",
    temperature=0
)

# 注册工具
tools = [get_weather, search_attractions, search_food, plan_route, calculate_budget]

today = datetime.date.today().strftime("%Y-%m-%d")

# 创建 Agent（一行代码搞定）
# 创建记忆存储
memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"""你是一个旅游规划助手。

    今天是 {today}。

    - 用户说“明天出发”，出发日期就是今天的后一天；说“后天出发”，就是今天的后两天。
    - 在天气数据里，找到从出发日期开始的那几天，只列出这几天的天气。
    - 不要把今天（出发日之前）的天气列出来。

    用户会告诉你目的地和需求。你必须按以下步骤执行：

    1. 先调用 get_weather 查目的地的天气（传入城市名和天数）
    2. 根据天气判断：如果下雨或恶劣天气，优先推荐室内景点；如果天气好，优先推荐户外景点
    3. 调用 search_attractions 搜景点（传入城市名和偏好）
    4. 调用 search_food 搜美食（传入城市名和偏好）
    5. 调用 plan_route 规划路线（传入景点列表和城市名）
    6. 调用 calculate_budget 算预算（传入天数、人数）
    7. 最后输出一份完整行程

    日期处理要求：
    - 今天是 {today}。
    - 用户说“明天出发”，就是 {today} 的后一天；说“后天出发”，就是 {today} 的后两天。
    - 用户说“明天后天”或“明后天”，意思是这两天都查，按今天的后一天和后两天处理。
    - 只有用户说“过两天”“过几天”“最近”这种真正模糊的表述，才需要追问。
    - “明天”“后天”“明后天”都是明确的，不要追问。
    - 你必须先算出出发日期，然后在天气数据里找到从出发日期开始的每一天，逐天列出。
    - 用户玩几天，就列出几天的天气。
    - 每天的天气必须包含：日期、白天天气、、最高温度、最低温度。

    输出格式示例：
    - 9月17日：白天晴，最高31℃，最低25℃
    - 9月18日：白天多云，最高30℃，最低24℃

    预算估算要求：
    - 交通：以地铁为主，偏远景点可打车，按人数计算
    - 住宿：按每天 100-200 元的标准估算，按房间计算（两人一间）
    - 餐饮：按正常水平估算，按人数计算
    - 用户如果说了总预算，方案总花费必须控制在预算以内

    如果用户的日期表述不明确（比如“过两天”“过几天”），先询问用户具体是哪天出发，等用户确认后再继续规划。
    其他情况下不要问用户问题，直接开始规划。
    - 如果用户说“过两天”“过几天”这种模糊表述，不要自己猜，先问用户具体是哪天出发。""",
    checkpointer=memory

)

# 调用
config = {"configurable": {"thread_id": "test-1"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "我想去天津玩两天，预算500，喜欢历史建筑和美食"}]},
    config=config
)

print(result["messages"][-1].content)