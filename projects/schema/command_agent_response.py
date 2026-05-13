from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional

from schema.common_response import AgentCommonResponse


class CommandBranchCondition(BaseModel):
    """Command 실행 경로를 결정하는 소스 코드 조건."""

    param: str = Field(
        description="MES Command 파라미터 이름입니다. 예: Category, SubCategory",
    )
    operator: Literal["equals", "not_equals", "exists", "unknown"] = Field(
        default="equals",
        description="Java 소스에서 추론한 조건 연산자입니다.",
    )
    value: Optional[str] = Field(
        default=None,
        description="분기 조건을 활성화하는 기대값입니다. 알 수 없는 경우 None입니다.",
    )


class CommandAgentResponse(AgentCommonResponse):
    """MES Command Agent의 출력 스키마."""

    command_name: str = Field(
        description="Given 메시지에서 실행할 Command 클래스 이름입니다.",
        examples=["CreateCarrier"],
    )
    command_message_items: List[str] = Field(
        description=(
            "String.join(COMMAND_START, ...)에 바로 사용할 수 있는 항목 목록입니다. "
            "첫 번째 항목은 반드시 Command 이름이어야 합니다."
        ),
        examples=[
            [
                "CreateCarrier",
                "CarrierId=:CarrierId",
                "CarrierType=FOUP",
                "Category=:Category",
            ]
        ],
    )
    bind_params: List[str] = Field(
        default_factory=list,
        description="When 블록에서 param.put(...)으로 값을 세팅해야 하는 파라미터 목록입니다.",
    )
    fixed_params: Dict[str, str] = Field(
        default_factory=dict,
        description="Command 메시지에 고정값으로 포함되는 파라미터 목록입니다.",
    )
    suggested_when_values: Dict[str, str] = Field(
        default_factory=dict,
        description="소스 또는 패치 내용에서 명확한 단서가 있을 때 bind_params에 추천할 실제 값입니다.",
    )
    branch_conditions: List[CommandBranchCondition] = Field(
        default_factory=list,
        description="수정된 Java 소스에서 추론한 분기 조건 목록입니다.",
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Command 메시지를 생성할 때 사용한 가정 목록입니다.",
    )
    missing_inputs: List[str] = Field(
        default_factory=list,
        description="필요했지만 제공되지 않았거나 의미가 모호한 입력값 목록입니다.",
    )


# 기존 소문자 클래스명 사용 방식과의 호환을 위한 별칭입니다.
command_response = CommandAgentResponse


"""
[CommandAgentResponse 출력 예시]

{
  "run_id": "20260513_153000",
  "step_id": 3,
  "agent_name": "command_agent",
  "user_request": "CreateCarrier 변경 소스를 기반으로 BDD Given/When Command 메시지를 생성한다.",
  "summary": "CreateCarrier Command 실행을 위한 Given/When Command 메시지와 바인딩 파라미터를 생성했습니다.",
  "next_input": "command_message_items는 CodeGenAgent의 Given 문자열 생성에 사용하고, branch_conditions는 테스트 입력값 선정에 참고합니다.",
  "target_classes": ["CreateCarrier"],
  "status": "success",
  "command_name": "CreateCarrier",
  "command_message_items": [
    "CreateCarrier",
    "CarrierId=:CarrierId",
    "CarrierType=FOUP",
    "CarrierSpec=FOUP",
    "Category=:Category",
    "SubCategory=:SubCategory",
    "Material=Material",
    "TimeUsedLimit=1000",
    "DurationUsedLimit=3652",
    "CleanDurationUsedLimit=365",
    "CleanTimeUsedLimit=1000",
    "CleanTimeLimit=1000",
    "Operator=X0158599"
  ],
  "bind_params": [
    "CarrierId",
    "Category",
    "SubCategory"
  ],
  "fixed_params": {
    "CarrierType": "FOUP",
    "CarrierSpec": "FOUP",
    "Material": "Material",
    "TimeUsedLimit": "1000",
    "DurationUsedLimit": "3652",
    "CleanDurationUsedLimit": "365",
    "CleanTimeUsedLimit": "1000",
    "CleanTimeLimit": "1000",
    "Operator": "X0158599"
  },
  "suggested_when_values": {
    "Category": "Engineer"
  },
  "branch_conditions": [
    {
      "param": "Category",
      "operator": "equals",
      "value": "Engineer"
    }
  ],
  "assumptions": [
    "Carrier 생성에 필요한 일반 필수 파라미터는 기존 MES 테스트 기본값을 사용했습니다.",
    "변경 기능 진입 조건에 영향을 주는 파라미터는 When 바인딩 대상으로 처리했습니다."
  ],
  "missing_inputs": []
}
"""
