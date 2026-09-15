import gradio as gr
from agent import agent

def plan_trip(user_input):
    """用户输入需求，返回 Agent 生成的行程"""
    if not user_input.strip():
        return "请输入你的旅行需求，比如：天津玩两天，预算500，喜欢历史建筑和美食"

    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    return result["messages"][-1].content

# 创建界面
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
            submit_btn = gr.Button("生成行程", variant="primary")

        with gr.Column():
            output = gr.Textbox(label="生成的行程", lines=20)

    submit_btn.click(fn=plan_trip, inputs=user_input, outputs=output)

if __name__ == "__main__":
    app.launch()