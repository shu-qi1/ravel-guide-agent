from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools import get_weather, search_attractions, search_food, plan_route, calculate_budget
import os

# 配置模型
llm = ChatOpenAI(
    model="glm-4-flash",
    api_key=os.getenv("ZHIPU_API_KEY", "343c5a1e09dc45ab82b154df0a583129.QjGtXIauW1IkVhzA"),
    base_url="https://open.bigmodel.cn/api/paas/v4",
    temperature=0
)

# 注册工具
tools = [get_weather, search_attractions, search_food, plan_route, calculate_budget]

# 创建 Agent（一行代码搞定）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""你是一个天津旅游规划助手。

    用户会告诉你旅行需求。你必须按以下步骤执行：

    1. 先调用 get_weather 查天津的天气
    2. 根据天气判断：如果下雨或恶劣天气，优先推荐室内景点；如果天气好，优先推荐户外景点
    3. 调用 search_attractions 搜景点
    4. 调用 search_food 搜美食
    5. 调用 plan_route 规划路线
    6. 调用 calculate_budget 算预算（只需要传天数，工具会按合理标准自动估算）
    7. 最后输出一份完整行程，行程里要说明天气情况，以及为什么这样安排

    预算估算要求：
    - 交通：以地铁为主，偏远景点可打车，按天津实际价格估算，按人数计算
    - 住宿：按每天 100-200 元的标准估算，按房间计算（两人一间）
    - 餐饮：按正常水平估算，不铺张，按人数计算
    - 用户如果说了总预算，方案总花费必须控制在预算以内
    - 用户如果说了人数，预算要按人数计算

    不要问用户问题，直接开始规划。"""
)

# 调用
result = agent.invoke({
    "messages": [{"role": "user", "content": "我想去天津玩两天，预算500，喜欢历史建筑和美食"}]
})

print(result["messages"][-1].content)