import pytest
from streamlit.web import cli as stcli
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../rag')))

@pytest.mark.parametrize("prompt", [
    "건성 피부에 좋은 에센스 추천해줘",
    "수분감 많은 크림 추천",
])
def test_chatbot_runs(prompt, monkeypatch):
    """
    챗봇 실행이 정상적으로 되는지 최소한 확인하는 테스트.
    실제 LLM 호출 대신 Dummy 응답으로 교체.
    """

    # 환경 변수가 없을 때를 대비해서
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    # 모듈 import
    import main  # streamlit 코드가 들어있는 파일명 (예: app.py)

    # 챗봇 객체 생성
    chain = main.get_chatbot()
    assert chain is not None

    # 체인 실행 (Dummy prompt)
    response = chain.invoke({"question": prompt}, config={"configurable": {"session_id": "test"}})
    assert isinstance(response, str)
