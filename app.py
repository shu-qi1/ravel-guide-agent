import gradio as gr
import uuid
from agent import agent
import datetime

# 当前会话的 thread_id
current_thread = {"id": str(uuid.uuid4())}

def plan_trip(user_input):
    if not user_input.strip():
        return "请输入你的旅行需求。"

    today = datetime.date.today().strftime("%Y-%m-%d")
    full_input = f"今天是 {today}。用户说：{user_input}"

    config = {"configurable": {"thread_id": current_thread["id"]}}
    result = agent.invoke(
        {"messages": [{"role": "user", "content": full_input}]},
        config=config
    )
    return result["messages"][-1].content

def reset_chat():
    """清空对话，开启新会话"""
    current_thread["id"] = str(uuid.uuid4())
    return "", ""

with gr.Blocks(title="旅游攻略 Agent") as app:
    gr.Markdown("# 旅游攻略 Agent")
    gr.Markdown("输入你的旅行需求，Agent 会自动查天气、搜景点、搜美食、规划路线、算预算，最后生成一份完整行程。")

    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                label="你的旅行需求",
                placeholder="比如：天津玩两天，预算500，喜欢历史建筑和美食",
                lines=3
            )
            with gr.Row():
                submit_btn = gr.Button("发送", variant="primary")
                reset_btn = gr.Button("重新开始")

        with gr.Column():
            output = gr.Textbox(label="生成的行程", lines=20)

    submit_btn.click(fn=plan_trip, inputs=user_input, outputs=output)
    reset_btn.click(fn=reset_chat, inputs=None, outputs=[user_input, output])

if __name__ == "__main__":
    app.launch()