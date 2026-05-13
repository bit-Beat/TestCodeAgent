from agents.orchestrator import orchestrator
from utils.common_method import log, pretty_trace, read_text_with_fallback
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent

thread_id = "test-thread" 

command_agent_input = {
    "target_class": "CreateCarrier",
    "update_content": read_text_with_fallback(project_root / "db" / "Update_content.txt"),
    "modified_source_path": "db/CreateCarrier.java",
    "diff_summary": (
        "CreateCarrier command에 신규 Engt FOUP 구분 관리를 위한 로직이 추가되었다. "
        "FabUseYN flag AD_20250827_NewEngtFoupAttributeManage가 ON이면 createNewEngtFoup(doc)를 수행한다. "
        "createNewEngtFoup는 Category가 Engineer이고 MES_COMMONTYP_DET에서 COMMON_TYP=NEW_ENGT_FOUP, "
        "TYP_VAL=SubCategory, DEFAULT_YN=Y 조건을 만족할 때 Durable attribute 생성 경로로 진입한다."
    ),
}

user_query = json.dumps(command_agent_input, ensure_ascii=False, indent=2)

#result = orchestrator.invoke({
for chunk in orchestrator.stream({
    "messages": [
        {"role": "user", "content": user_query}
    ]},
    config={"configurable": {"thread_id": thread_id}},
    stream_mode = "updates",
    subgraphs=True,
    version="v2",
):
    log(chunk)
    #if chunk["type"] == "updates":
    #    if chunk["ns"]:
    #        log(f"[subagent: {chunk['ns']}]")
    #    else :
    #        log("[Main Agent]")
        
#log(result, "warning")
#pretty_trace(result)
