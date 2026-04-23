from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore
import uuid
from langchain_openai  import AzureChatOpenAI

from agents.weather_agent import weather_agent
from utils.config_loader import load_config
from utils.common_method import log, pretty_trace

# --- [LLM 설정] ---
LLM_KEY = load_config("LLM", "KEY")
LLM_MODEL = load_config("LLM", "MODEL")
LLM_ENDPOINT = load_config("LLM", "ENDPOINT")
LLM_VERSION = load_config("LLM", "VERSION")

LLM = AzureChatOpenAI(
    deployment_name = LLM_MODEL,
    azure_endpoint = LLM_ENDPOINT,
    api_key = LLM_KEY,
    api_version= LLM_VERSION,
    temperature = 0.2
)

store = InMemoryStore()

# --- [Main Orchestrator] ---
orchestrator = create_deep_agent(
    model= LLM, #모델
    tools=[], # 도구
    system_prompt = """
너는 기상캐스터다.

반드시 다음 규칙을 지켜라:

1. 모든 데이터는 반드시 파일로 저장하고 읽어라
2. 경로는 반드시 아래를 사용한다:
   - /weather/raw.txt
   - /weather/analysis.txt
   - /weather/forecast.txt
3. 마지막에는 위 3개 파일을 모두 read_file로 읽고, **weather-report Skill**을 참조하여 종합해서 답변하라
4. 최종 결과를 /memory/history.txt에 저장하라
** 5. 이전 memory가 있으면 참고하라 **
** 반드시 SKILL을 참조하여 종합하라. **


파일을 사용하지 않으면 실패다.
""",
    subagents=[weather_agent],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/weather/": FilesystemBackend(
                root_dir="./data/weather",
                virtual_mode=True
            ),
            "/memory/" : StoreBackend(
                namespace=lambda rt: (rt.execution_info.thread_id,)
            )
        }
    ),
    memory=["/memory/history.txt"],
    store=store,
    skills=["./skills/wheather"]
    #middleware=,
    #interrupt_on={"delete_file": True, "send_email": {"allowed_decisions": ["approve", "reject"]}} # Human-in-the-loop
    #debug=True
)
