# 旅游攻略 Agent

基于大模型 API 与 LangChain 构建的旅游攻略 Agent。用户输入模糊需求（如"天津玩两天，预算500，喜欢历史建筑和美食"），Agent 自动完成信息搜集、路线规划与行程生成。

## 功能

- 自动查询目的地天气
- 搜索符合偏好的景点和美食
- 规划景点之间的游览路线
- 估算旅行预算
- 根据天气动态调整行程
- Gradio 网页界面

## 技术栈

Python、LangChain、智谱 GLM-4-Flash、和风天气 API、Gradio、Git

## 项目结构

- `agent.py`：Agent 核心逻辑
- `app.py`：Gradio 网页界面
- `tools.py`：五个工具函数
- `key3-public.pem`：JWT 公钥
- `README.md`：项目说明

## 运行方式

1. 安装依赖：

```bash
  pip install langchain langchain-openai langgraph requests gradio
```

2. 设置环境变量：

```bash
  set ZHIPU_API_KEY=你的智谱API_KEY
```

3. 运行网页界面：

```bash
  python app.py
```

4. 浏览器打开终端显示的地址（通常是 `http://127.0.0.1:7860`）

## 使用示例

在网页输入：

> 国庆三天，两个人在天津玩，预算1000，喜欢历史建筑和美食

Agent 会自动查天气、搜景点、搜美食、规划路线、算预算，最后输出一份完整行程。

## 五个工具

| 工具 | 作用 |
| :--- | :--- |
| `get_weather` | 查天气 |
| `search_attractions` | 搜景点 |
| `search_food` | 搜美食 |
| `plan_route` | 规划路线 |
| `calculate_budget` | 算预算 |