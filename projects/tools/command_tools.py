import json
import re
from pathlib import Path
from typing import Any

from langchain_core.tools import tool
from utils.common_method import log


DEFAULT_PARAM_VALUES = {
    "CarrierType": "FOUP",
    "CarrierSpec": "FOUP",
    "Material": "Material",
    "TimeUsedLimit": "1000",
    "DurationUsedLimit": "3652",
    "CleanDurationUsedLimit": "365",
    "CleanTimeUsedLimit": "1000",
    "CleanTimeLimit": "1000",
    "Operator": "X0158599",
}


def _read_text_with_fallback(path: Path) -> str:
    """파일을 utf-8, cp949, euc-kr 순서로 읽고 성공한 문자열을 반환합니다."""
    for encoding in ("utf-8", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text()


def _resolve_project_path(path: str) -> Path:
    """프로젝트 루트 기준의 상대 경로를 실제 파일 경로로 변환합니다."""
    project_root = Path(__file__).resolve().parents[1]
    source_path = Path(path)
    if not source_path.is_absolute():
        source_path = project_root / source_path

    resolved_path = source_path.resolve()
    if not resolved_path.is_relative_to(project_root):
        raise ValueError(f"Path is outside project root: {path}")
    if not resolved_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {resolved_path}")
    return resolved_path


def _normalize_command_name(target_class: str) -> str:
    """파일명으로 전달된 target_class에서 .java 확장자를 제거하여 Command 이름을 반환합니다."""
    if target_class.endswith(".java"):
        return Path(target_class).stem
    return target_class


def _unique_in_order(values: list[str]) -> list[str]:
    """입력 리스트의 순서를 유지하면서 중복 값을 제거합니다."""
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _extract_doc_params(source: str) -> tuple[list[str], dict[str, str]]:
    """Java 소스에서 MessageUtil.getBodyItemValue(doc, "...")로 읽는 Command 파라미터를 추출합니다."""
    log("Extracting Command parameters from Java source...")
    assignment_pattern = re.compile(
        r"String\s+(\w+)\s*=\s*MessageUtil\.getBodyItemValue\s*"
        r"\(\s*doc\s*,\s*\"([^\"]+)\"\s*\)"
    )
    variable_to_param = {
        variable_name: param_name
        for variable_name, param_name in assignment_pattern.findall(source)
    }

    param_pattern = re.compile(
        r"MessageUtil\.getBodyItemValue\s*\(\s*doc\s*,\s*\"([^\"]+)\"\s*\)"
    )
    log(f"Found parameters1: {_unique_in_order(param_pattern.findall(source))}")
    log(f"Found parameters2: {variable_to_param}")
    return _unique_in_order(param_pattern.findall(source)), variable_to_param


def _extract_branch_conditions(
    source: str, variable_to_param: dict[str, str]
) -> list[dict[str, str]]:
    """Java 소스의 문자열 equals 조건을 Command 파라미터 기준의 분기 조건으로 변환합니다."""
    equals_pattern = re.compile(r"(\w+)\.equals\s*\(\s*\"([^\"]+)\"\s*\)")
    conditions = []
    for variable_name, expected_value in equals_pattern.findall(source):
        param_name = variable_to_param.get(variable_name)
        if param_name:
            conditions.append(
                {
                    "param": param_name,
                    "operator": "equals",
                    "value": expected_value,
                }
            )
    return conditions


def extract_command_message(
    target_class: str,
    update_content: str,
    modified_source: str,
    diff_summary: str = "",
) -> dict[str, Any]:
    """수정된 Java Command 소스를 분석하여 Given Command 메시지와 When 바인딩 정보를 생성합니다."""
    target_class = _normalize_command_name(target_class)
    params, variable_to_param = _extract_doc_params(modified_source)
    branch_conditions = _extract_branch_conditions(modified_source, variable_to_param)

    condition_params = {condition["param"] for condition in branch_conditions}
    dynamic_params = {"CarrierId"}
    dynamic_params.update(condition_params)

    for param in params:
        if "Category" in param:
            dynamic_params.add(param)
        elif param not in DEFAULT_PARAM_VALUES:
            dynamic_params.add(param)

    command_items = [target_class]
    fixed_params = {}
    bind_params = []

    for param in params:
        if param in dynamic_params:
            command_items.append(f"{param}=:{param}")
            bind_params.append(param)
        else:
            value = DEFAULT_PARAM_VALUES[param]
            command_items.append(f"{param}={value}")
            fixed_params[param] = value

    suggested_when_values = {
        condition["param"]: condition["value"] for condition in branch_conditions
    }

    result = {
        "agent_name": "command_agent",
        "summary": (
            f"Built Given/When command execution plan for {target_class} "
            f"with {len(command_items) - 1} command parameters."
        ),
        "next_input": (
            "Use command_message_items to generate the Given command string, "
            "and use bind_params and suggested_when_values to generate the When block."
        ),
        "target_classes": [target_class],
        "status": "success",
        "command_name": target_class,
        "command_message_items": command_items,
        "bind_params": bind_params,
        "fixed_params": fixed_params,
        "suggested_when_values": suggested_when_values,
        "branch_conditions": branch_conditions,
        "assumptions": [
            "Known MES carrier defaults are used for non-feature parameters.",
            "CarrierId and feature-driving parameters are emitted as When binding placeholders.",
        ],
        "missing_inputs": [],
    }
    return result


@tool
def extract_command_message_from_file(
    target_class: str,
    modified_source_path: str,
    update_content: str,
    diff_summary: str = "",
) -> str:
    """수정된 Java Command 파일을 직접 읽어 Given/When Command 실행 계획을 JSON 문자열로 반환합니다."""
    source_path = _resolve_project_path(modified_source_path)
    modified_source = _read_text_with_fallback(source_path)
    result = extract_command_message(
        target_class=target_class,
        update_content=update_content,
        modified_source=modified_source,
        diff_summary=diff_summary,
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def extract_command_message_json(
    target_class: str,
    update_content: str,
    modified_source: str,
    diff_summary: str = "",
) -> str:
    """CommandAgent가 사용할 Given/When Command 실행 계획을 JSON 문자열로 반환합니다."""
    result = extract_command_message(
        target_class=target_class,
        update_content=update_content,
        modified_source=modified_source,
        diff_summary=diff_summary,
    )
    return json.dumps(result, ensure_ascii=False, indent=2)
