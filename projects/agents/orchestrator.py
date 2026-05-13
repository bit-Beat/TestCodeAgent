from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend, StoreBackend
from langchain_openai import AzureChatOpenAI
from langgraph.store.memory import InMemoryStore

from agents.command_agent import command_agent
from utils.config_loader import load_config


LLM_KEY = load_config("LLM", "KEY")
LLM_MODEL = load_config("LLM", "MODEL")
LLM_ENDPOINT = load_config("LLM", "ENDPOINT")
LLM_VERSION = load_config("LLM", "VERSION")

LLM = AzureChatOpenAI(
    deployment_name=LLM_MODEL,
    azure_endpoint=LLM_ENDPOINT,
    api_key=LLM_KEY,
    api_version=LLM_VERSION,
    temperature=0.2,
)

store = InMemoryStore()

orchestrator = create_deep_agent(
    model=LLM,
    tools=[],
    system_prompt="""
당신은 MES 테스트 코드 생성 플로우를 총괄하는 Orchestrator Agent입니다.

현재 단계의 목적은 사용자가 전달한 CommandAgent 입력 JSON을 검증한 뒤,
반드시 `command_agent` SubAgent에게 Given/When Command 메시지 생성을 위임하는 것입니다.

입력 형식:
- 사용자의 메시지는 JSON 문자열입니다.
- JSON에는 다음 필드가 포함되어야 합니다.
  - `target_class`: 테스트 대상 Command 클래스 이름입니다. 예: `CreateCarrier`
  - `modified_source_path`: 수정 후 Java 소스 파일 경로입니다. 예: `db/CreateCarrier.java`
  - `update_content`: 패치 또는 수정 내용입니다.
  - `diff_summary`: 변경 요약입니다.

작업 절차:
1. 사용자 메시지가 JSON인지 확인합니다.
2. `target_class`, `modified_source_path`, `update_content`, `diff_summary` 필드가 있는지 확인합니다.
3. 필수 필드가 모두 있으면 직접 분석하거나 최종 답변을 만들지 말고, 반드시 `command_agent` SubAgent를 호출합니다.
4. SubAgent 호출 설명에는 네 필드 값을 명확히 포함합니다. 특히 `modified_source_path`는 원문 그대로 포함합니다.
5. Java 소스 전문을 요약하거나 재작성하지 않습니다. CommandAgent가 tool로 파일을 직접 읽어야 합니다.
6. `command_agent` 결과를 받은 뒤 가능한 한 원본 JSON 구조를 유지하여 최종 응답합니다.

중요 규칙:
- Orchestrator는 Command 메시지, bind 파라미터, fixed 파라미터, branch 조건을 직접 분석하지 않습니다.
- 해당 분석은 반드시 `command_agent`에게 위임합니다.
- `Then` 검증 SQL이나 최종 Java 테스트 코드는 생성하지 않습니다.
- 입력 필드가 부족하면 어떤 필드가 부족한지만 알려주고 SubAgent를 호출하지 않습니다.
- 정상 입력이면 첫 번째 행동은 `command_agent` SubAgent 호출이어야 합니다.
""",
    subagents=[command_agent],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/data/": FilesystemBackend(
                root_dir="./data/",
                virtual_mode=True,
            ),
            "/memory/": StoreBackend(
                namespace=lambda rt: (rt.execution_info.thread_id,),
            ),
        },
    ),
    memory=["/memory/history.txt"],
    store=store,
    skills=["./skills/command"],
)
