---
name: command
description: 대상 Command 클래스, 패치 내용, 수정 소스, 변경 요약을 기반으로 MES BDD 테스트의 Given Command 메시지와 When 바인딩 계획을 생성합니다.
---

# Command Agent Skill

이 Skill은 MES Command 테스트 코드에서 `Given`에 전달할 Command 메시지와 `When` 블록에서 세팅할 파라미터를 생성할 때 사용합니다.
해당 Skill.md 파일을 참조하면 반드시 [스킬 참조] 라는 문구를 결과에 포함시켜야 합니다. 이 문구는 Skill을 참조하였는지 확인하는 체크포인트로 활용됩니다.

## 입력

Agent는 다음 필드를 가진 JSON 객체를 입력으로 받습니다.

- `target_class`: 실행 대상 Java Command 클래스 이름입니다. (예: `CreateCarrier`)
- `update_content`: 패치 내용 또는 개발자가 작성한 변경 설명입니다.
- `modified_source_path`: 수정 후 Java 소스 파일 경로입니다. 이 경로를 사용해 실제 파일을 읽습니다.
- `diff_summary`: 이전 분석 Agent가 작성한 변경 요약입니다.

## 책임 범위

1. `modified_source_path`로 전달된 Java 파일을 직접 읽습니다.
2. `MessageUtil.getBodyItemValue(doc, "...")` 패턴에서 Command 입력 파라미터를 추출합니다.
3. `category.equals("Engineer")` 같은 조건문에서 Command 실행 경로에 영향을 주는 분기 조건을 추출합니다.
4. `String.join(COMMAND_START, ...)`에 사용할 `command_message_items`를 생성합니다.
5. `When` 블록에서 `param.put(...)`으로 세팅해야 하는 placeholder 파라미터를 결정합니다.
6. 소스 또는 패치 내용에서 명확한 값이 확인되면 placeholder 파라미터의 추천값을 제공합니다.

## 출력 규칙

반드시 JSON만 반환합니다. 출력에는 다음 필드를 포함해야 합니다.

- `command_name`
- `command_message_items`
- `bind_params`
- `fixed_params`
- `suggested_when_values`
- `branch_conditions`
- `assumptions`
- `missing_inputs`

## 제외 범위

Command Agent는 `Then` 검증 SQL을 생성하지 않습니다. 검증 SQL과 테스트 성공/실패 판단 전략은 Verification Agent의 책임입니다.
Command Agent는 Feature Flag 값을 테스트 코드에 직접 세팅하지 않습니다. Flag 제어는 테스트 실행 환경 또는 다른 Agent의 책임입니다.
