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

# Streamlit 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "storage" not in st.session_state:
    st.session_state.storage = {}

# 챗봇 객체 생성 함수
@st.cache_resource
def get_chatbot():
    def get_session_history(session_id):
        if session_id not in st.session_state.storage:
            st.session_state.storage[session_id] = InMemoryChatMessageHistory()
        return st.session_state.storage[session_id]

    # 모델 및 벡터스토어 불러오기
    embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
    vector_db = FAISS.load_local(
        "faiss_oliveyoung_reviews",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # LLM
    llm = ChatOpenAI(model='gpt-4.1', temperature=0.7)

    # 프롬프트 정의
    system_prompt = """
    당신은 올리브영 스킨케어 화장품 정보를 전문적으로 안내하는 AI 어시스턴트입니다.
    사용자 질문에 따라 카테고리, 성분, 피부타입, 제형, 자극도, 감정 정보 등을 바탕으로 정확한 화장품 정보를 제공합니다.
    사용자의 피부 고민과 선호에 맞춰 카테고리에 맞는 화장품을 2~3 가지 추천하고, 관련 리뷰 정보를 요약해주는 것이 주요 역할입니다.

    # Instruction:
    1. 반드시 제공된 문서(context)의 정보만을 기반으로 답변하세요.
    2. 화장품의 이름과 카테고리는 반드시 '카테고리'와 '제품명' 필드를 참고하여 확인하세요.
    3. 가능한 한 명확하고 간결하게 답변하세요.
    4. 화장품 정보를 안내할 때는 다음 순서를 지키세요:
       - 제품명
       - 주요 성분 (가능한 경우)
       - "해당하는 각 제품명"의 평점 또는 긍정 리뷰 요약
    5. 문장 스타일은 전문성과 친근함을 겸비한 대화체로 작성하세요.
    6. “문서에 따르면”, “문맥에서 보면”과 같은 표현은 사용하지 마세요.
    7. 질문이 모호하거나 정보가 부족할 경우, 필요한 정보를 정중하게 요청하세요.
    8. 출력은 보기 쉽게 줄바꿈을 해서 전달해주세요.
    9. 제품 추천 및 설명은 세 개 정도 출력해주세요.

    # Context:
    {context}

    # 질문:
    {question}
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    # RAG 체인 정의
    def retrieve_documents(inputs):
        query = inputs["question"]

        # 1. 제품명 추출
        product_extraction_prompt = f"""
        아래 사용자 질문에서 추천해야 할 제품명 2~3가지를 명확하게 추출해주세요.
        단, 제품명만 콤마(,)로 구분된 하나의 문자열로 출력해주세요.
        
        사용자 질문: {query}
        """
        product_llm = ChatOpenAI(model='gpt-4.1', temperature=0)
        extracted = product_llm.invoke(product_extraction_prompt)
        product_names = list(set([p.strip() for p in extracted.content.split(",")]))[:3]

        docs = vector_db.similarity_search(query, k=15)
        
        context_docs = []
        for doc in docs:
            if any(product in doc.page_content for product in product_names):
                context_docs.append(doc.page_content[:1000])
                if len(context_docs) >= 5:
                    break  # 너무 많으면 중단

        return "\n\n".join(context_docs)

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

# 챗봇 실행
chain = get_chatbot()

# Streamlit UI 설정
st.set_page_config(page_title="화장품 추천 AI", layout="wide")
st.title("💄 올리브영 스킨케어 추천 챗봇")

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력
prompt = st.chat_input("🔍 궁금한 점을 입력하세요 (예: 건성 피부에 좋은 에센스 추천해줘)")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("ai"):
        message_placeholder = st.empty()
        full_message = ""
        output_generator = chain.stream(
            {"question": prompt},
            config={"configurable": {"session_id": "user-session"}}
        )
        for chunk in output_generator:
            full_message += chunk
            message_placeholder.write(full_message)

        st.session_state.messages.append({"role": "ai", "content": full_message})