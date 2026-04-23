from langchain.tools import tool

## Tool 생성
@tool
def get_weather_data(location: str) -> str:
    """특정 지역의 현재 날씨 데이터를 조회한다."""
    return f"{location} 현재 날씨: 맑음, 18도, 습도 40%"*500

@tool
def analyze_weather(data: str) -> str:
    """날씨 데이터를 분석하여 상태를 해석한다."""
    return "기온이 적당하고 습도가 낮아 쾌적한 날씨"

@tool
def forecast_weather(data: str) -> str:
    """현재 날씨를 기반으로 향후 날씨를 예측한다."""
    return "내일도 맑은 날씨가 지속될 가능성이 높음"

