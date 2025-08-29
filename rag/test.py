import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

# 환경변수 로드
load_dotenv()

# ---------------------------
# 챗봇 객체 생성
# ---------------------------
@st.cache_resource
def get_chatbot(faiss_path: str = None, pkl_path: str = None, dummy: bool = False):
    """
    dummy=True면 테스트용 벡터 DB와 더미 LLM 사용
    """
    # 세션 히스토리 관리
    def get_session_history(session_id):
        if "storage" not in st.session_state:
            st.session_state.storage = {}
        if session_id not in st.session_state.storage:
            st.session_state.storage[session_id] = InMemoryChatMessageHistory()
        return st.session_state.storage[session_id]

    # ---------------------------
    # 벡터 DB
    # ---------------------------
    if dummy:
        class DummyDB:
            def similarity_search(self, query, k=5):
                class Doc:
                    page_content = f"더미 문서 내용: {query}"
                return [Doc() for _ in range(k)]
        vector_db = DummyDB()
    else:
        # 실제 FAISS 로드
        embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
        if faiss_path and os.path.exists(faiss_path):
            vector_db = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
        else:
            vector_db = None

    # ---------------------------
    # LLM
    # ---------------------------
    if dummy:
        class DummyLLM:
            def invoke(self, prompt):
                class Resp:
                    content = f"더미 응답: {prompt[:50]}..."
                return Resp()
        llm = DummyLLM()
    else:
        llm = ChatOpenAI(model="gpt-4.1", temperature=0.7)

    # ---------------------------
    # RAG 체인
    # ---------------------------
    system_prompt = "당신은 화장품 추천 챗봇입니다. 문서 기반으로 답변하세요."
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    def retrieve_documents(inputs):
        query = inputs["question"]
        docs = vector_db.similarity_search(query, k=5)
        context = "\n\n".join([d.page_content[:1000] for d in docs])
        return context

    rag_chain = (
        RunnablePassthrough.assign(
            context=retrieve_documents,
            question=lambda x: x["question"]
        )
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )


# ---------------------------
# Streamlit UI
# ---------------------------
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

if __name__ == "__main__":
    init_session()
    chain = get_chatbot()

    st.title("💄 화장품 추천 챗봇")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("궁금한 점을 입력하세요")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("ai"):
            message_placeholder = st.empty()
            full_message = ""
            output_generator = chain.stream({"question": prompt}, config={"configurable": {"session_id": "test-session"}})
            for chunk in output_generator:
                full_message += chunk
                message_placeholder.write(full_message)
            st.session_state.messages.append({"role": "ai", "content": full_message})
