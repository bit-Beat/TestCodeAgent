/testcodeagent [dir]
 ├ ** main.py **
 ├ README.md
 ├ config.ini
 │
 ├ agents/ [dir]
 │	├ orchestrator.py
 │	├ reqdiff_agent.py
 │	├ asset_retrieval_agent.py
 │	├ command_agent.py
 │	├ verification_agent.py
 │	├ code_gen_agent.py
 │	├ code_run_agent.py
 │
 ├ data/ [dir]
 │
 ├ skills/ [dir]
 │	├ reqdiff/SKILL.md
 │	├ asset_retrieval/SKILL.md
 │	├ command/SKILL.md
 │	├ verification/SKILL.md
 │	├ code_gen/SKILL.md
 │	├ code_run/SKILL.md
 │
 ├ tools/ [dir]
 ├ db/ [dir]
 ├ utils/ [dir]
 │	├ common_method.py
 │	└ config_loader.py
 
### 파일 설명
[/testcodeagent]
 - main.py : 최종 실행 파일 (사용자의 요청 입력을 orchestrator 에게 전달 후 결과를 출력)
 - config.ini : LLM_MODEL 정보 등 공통 설정값 세팅 파일
 
[/testcodeagent/agents/]
 - orchestratr.py : Main Agent 하위 subagent의 역할을 조정하고 관리하는 에이전트
 - reqdiff_agent.py : 요구사항/코드분석 에이전트 : 테스트 핵심 항목 추출, 코드 변경사항 추출 등
 - asset_retrieval_agent.py : BDD 패턴 테스트 코드 기본 구조 작성
 - command_agent.py : 커맨드/테스트 파라미터 데이터셋 세팅
 - verification_agent.py : then 데이터 검증 작성 에이전트
 - code_gen_agent.py : 최종 테스트 코드 생성
 - code_run_agent.py : 최종 테스트 코드 실행 (에러/테스트 케이스 실패, 성공 여부 판단)
 
[/testcodeagent/data/]
 - 각 Agent가 생성하는 Data가 있을 경우 해당 경로에 저장 예정(ex. reqdiff_agent가 file 을 생성하면 /testcodeagent/data/reqdiff/code.raw와 같은 파일 생성)
 
[/testcodeagent/skills/]
 - reqdiff/SKILL.md : reqdiff_agent의 skill파일
 - asset_retrieval/SKILL.md : asset_retrieval_agent의 skill파일
 - command/SKILL.md : command_agent의 skill파일
 - verification/SKILL.md : verification_agent의 skill파일
 - code_gen/SKILL.md : code_gen_agent의 skill파일
 - code_run/SKILL.md : code_run_agent의 skill파일
 
[/testcodeagent/tools/]
 - agent가 사용할 tool을 해당 경로에 생성 예정 ※ 해당 폴더에서는 다른 Agent도 같은 툴을 사용할 경우가 있을 수 있으므로, 모든 Agent가 공유할 수 있도록 따로 폴더 생성 필요 없음.

[/testcodeagent/utils/]
 - common_method.py : 모든 파일에서 공통적으로 사용할 수 있는 유틸리티 기능들을 작성
 - config_loader.py : config.ini 파일을 읽어와서 리턴해주는 함수.
 
[/testcodeagent/db/]
 - Agent가 필요한 사전 파일들을 저장할 로컬 저장소 (ex. ppt패치내역, table정의서, 자바소스 등)
 
 