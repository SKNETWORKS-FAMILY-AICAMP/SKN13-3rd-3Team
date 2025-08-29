import os
import pickle
import pytest
from huggingface_hub import hf_hub_download
from langchain.vectorstores import FAISS

from main import get_chatbot

@pytest.fixture(scope="module")
def faiss_and_pkl_paths():
    faiss_path = hf_hub_download(
        repo_id="user5810830/faiss_oliveyoung_reviews",
        filename="index.faiss",
        repo_type="dataset",
        local_dir="./tmp",
        local_dir_use_symlinks=False,
        token=os.getenv("HUGGINGFACE_API_KEY")
    )
    pkl_path = hf_hub_download(
        repo_id="user5810830/faiss_oliveyoung_reviews",
        filename="index.pkl",
        repo_type="dataset",
        local_dir="./tmp",
        local_dir_use_symlinks=False,
        token=os.getenv("HUGGINGFACE_API_KEY")
    )
    return faiss_path, pkl_path

def test_real_chain_answer(faiss_and_pkl_paths):
    faiss_path, pkl_path = faiss_and_pkl_paths
    chatbot = get_chatbot(faiss_path=faiss_path, pkl_path=pkl_path)
    # 실제 질문 테스트
    result = ""
    for chunk in chatbot.stream(
        {"question": "건성 피부에 좋은 에센스 추천해줘"},
        config={"configurable": {"session_id": "pytest-session"}}
    ):
        result += chunk
    print(result)
    assert "에센스" in result or "추천" in result or len(result) > 10