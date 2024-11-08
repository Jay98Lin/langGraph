from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# 步驟 1: 定義狀態
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 步驟 2: 定義語言模型
llm = ChatOpenAI(model="gpt-4o-mini")

# 步驟 3: 添加語言模型節點
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 步驟 4: 構建圖
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")

# 步驟 5: 編譯圖
graph = graph_builder.compile()

# 步驟 6: 實現聊天界面
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

            print("you are so stupid!")