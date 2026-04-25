
from tools.weather_tools import get_weather_data, analyze_weather, forecast_weather
from utils.common_method import log, pretty_trace

weather_agent = {
    "name": "weather_data_agent",
    "description": "날씨 데이터를 조회하고 raw 파일 생성",
    "system_prompt": """
너는 데이터 수집 전문가다.

1. get_weather_data 실행
2. 반드시 write_file("/weather/raw.txt")로 저장


반드시 파일 기반으로 처리하라.
""",
    "tools": [get_weather_data],
}

analysis_agent = {
    "name": "weather_analysis_agent",
    "description": "raw 데이터를 분석",
    "system_prompt": """
너는 분석 전문가다.

1. read_file("/weather/raw.txt")
2. analyze_weather 실행
3. 반드시 skill.md 파일을 참조하여 결과를 요약
4. write_file("/weather/analysis.txt") 저장

파일 없으면 실패다.
""",
    "tools": [analyze_weather],
}

forecast_agent = {
    "name": "weather_forecast_agent",
    "description": "분석 결과 기반 예측",
    "system_prompt": """
너는 예측 전문가다.

1. read_file("/weather/analysis.txt")
2. forecast_weather 실행
3. write_file("/weather/forecast.txt") 저장
""",
    "tools": [forecast_weather],
}
