from agents.orchestrator import orchestrator
from utils.common_method import log, pretty_trace


thread_id = "test-thread" 
user_query = "오늘 서울 날씨 어때?."
result = orchestrator.invoke({
    "messages": [
        {"role": "user", "content": user_query}
    ]},
    config={"configurable": {"thread_id": thread_id}}
)

pretty_trace(result)
