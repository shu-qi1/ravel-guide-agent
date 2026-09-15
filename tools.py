import requests
from langchain_core.tools import tool

# ========== 配置 ==========
API_KEY = "ef10a8d03a5c409a913211499a247141"
API_HOST = "https://mj5ctxf8e3.re.qweatherapi.com"

TIANJIN_CODE = "101030100"

@tool
def get_weather(city: str = "天津", days: int = 7) -> list:
    """查询指定城市未来几天的天气。输入城市名和天数（3或7），返回天气列表。"""
    if days not in [3, 7]:
        days = 7

    # 第一步：用 GeoAPI 查城市代码
    geo_url = f"{API_HOST}/geo/v2/city/lookup"
    geo_params = {"location": city, "key": API_KEY}
    geo_response = requests.get(geo_url, params=geo_params)

    try:
        geo_data = geo_response.json()
    except Exception:
        return {"error": f"城市查询失败，状态码 {geo_response.status_code}"}

    if geo_data.get("code") != "200" or not geo_data.get("location"):
        return {"error": f"找不到城市：{city}"}

    city_code = geo_data["location"][0]["id"]

    # 第二步：查天气
    url = f"{API_HOST}/v7/weather/{days}d"
    params = {"location": city_code, "key": API_KEY}
    response = requests.get(url, params=params)

    try:
        data = response.json()
    except Exception:
        return {"error": f"天气接口返回异常，状态码 {response.status_code}"}

    if data.get("code") != "200":
        return {"error": f"查询失败，错误码：{data.get('code')}"}

    result = []
    for day in data["daily"]:
        result.append({
            "date": day["fxDate"],
            "temp_min": day["tempMin"],
            "temp_max": day["tempMax"],
            "text_day": day["textDay"],
            "text_night": day["textNight"],
            "precip": day["precip"],
            "uv_index": day["uvIndex"]
        })
    return result

import json
import os
import requests
from langchain_core.tools import tool

# 智谱配置
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "343c5a1e09dc45ab82b154df0a583129.QjGtXIauW1IkVhzA")
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


@tool
def search_attractions(city: str, preference: str) -> list:
    """搜索指定城市的景点。输入城市名和用户偏好，返回符合条件的景点列表。"""
    prompt = f"""请推荐{city}的{preference}类景点，返回JSON数组格式，每个景点包含：
- name: 景点名称
- type: 景点类型
- desc: 一句话描述

只返回JSON数组，不要其他内容。最多返回6个景点。

示例格式：
[{{"name": "五大道", "type": "历史建筑", "desc": "天津著名的欧式建筑群"}}]
"""

    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(ZHIPU_URL, headers=headers, json=payload)
    data = response.json()
    print("智谱返回:", data)

    content = data["choices"][0]["message"]["content"].strip()

    # 容错：去掉 Markdown 代码块
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    # 容错：提取 JSON 数组部分
    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1:
        content = content[start:end+1]

    return json.loads(content)

@tool
def search_food(city: str, preference: str) -> list:
    """搜索指定城市的美食。输入城市名和用户偏好，返回符合条件的美食列表。"""
    prompt = f"""请推荐{city}的{preference}类美食，返回JSON数组格式，每个美食包含：
- name: 美食或餐厅名称
- type: 类型（如小吃、正餐、甜品）
- desc: 一句话描述

只返回JSON数组，不要其他内容。最多返回6个。

示例格式：
[{{"name": "狗不理包子", "type": "小吃", "desc": "天津传统名点"}}]
"""

    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(ZHIPU_URL, headers=headers, json=payload)
    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    # 容错：去掉 Markdown 代码块
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    # 容错：提取 JSON 数组部分
    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1:
        content = content[start:end+1]

    return json.loads(content)

@tool
def calculate_budget(days: int, people: int = 1, transport_per_day: float = 30, food_per_day: float = 80, hotel_per_day: float = 150) -> dict:
    """按天数和人数估算旅行预算。输入天数、人数，返回交通、餐饮、住宿和总花费。
    默认标准：交通30元/人/天，餐饮80元/人/天，住宿150元/间/天。"""
    transport = transport_per_day * days * people
    food = food_per_day * days * people
    hotel = hotel_per_day * days  # 住宿按房间算，不乘人数
    total = transport + food + hotel
    return {
        "days": days,
        "people": people,
        "transport": transport,
        "food": food,
        "hotel": hotel,
        "total": total
    }

@tool
def plan_route(attractions: list, city: str = "天津") -> str:
    """规划景点之间的路线。输入景点列表和城市名，返回推荐的游览顺序和交通方式。"""
    spots = "、".join(attractions)
    prompt = f"""我有以下几个{city}的景点要去：{spots}

请帮我规划一个合理的游览顺序，并说明每个景点之间怎么走（步行、地铁、打车）。
考虑距离和游览效率，返回一段简洁的文字说明。"""

    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(ZHIPU_URL, headers=headers, json=payload)
    data = response.json()
    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    result = get_weather.invoke({"city_code": "101030100", "days": 3})
    for day in result:
        print(day)

    result = search_attractions.invoke({"city": "天津", "preference": "历史建筑"})
    print(result)

    result = search_food.invoke({"city": "天津", "preference": "小吃"})
    print(result)

    result = calculate_budget.invoke({"transport": 100, "tickets": 50, "food": 150, "hotel": 200})
    print(result)

    result = plan_route.invoke({"attractions": ["五大道", "天津之眼", "古文化街"]})
    print(result)