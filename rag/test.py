import os
import pickle
from huggingface_hub import hf_hub_download
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

def get_chatbot(faiss_path: str = None, pkl_path: str = None):
    def get_session_history(session_id):
        # 테스트에서는 메모리 기반 히스토리만 사용
        return InMemoryChatMessageHistory()

    # 인덱스 파일 없으면 다운로드
    if faiss_path is None:
        faiss_path = hf_hub_download(
            repo_id="user5810830/faiss_oliveyoung_reviews",
            filename="index.faiss",
            repo_type="dataset",
            local_dir="./tmp",
            local_dir_use_symlinks=False,
            token=os.getenv("HUGGINGFACE_API_KEY")
        )
    if pkl_path is None:
        pkl_path = hf_hub_download(
            repo_id="user5810830/faiss_oliveyoung_reviews",
            filename="index.pkl",
            repo_type="dataset",
            local_dir="./tmp",
            local_dir_use_symlinks=False,
            token=os.getenv("HUGGINGFACE_API_KEY")
        )

    with open(pkl_path, "rb") as f:
        index = pickle.load(f)

    vector_db = FAISS.load_local(
        folder_path=os.path.dirname(faiss_path),
        embeddings=index.embeddings,
        allow_dangerous_deserialization=True
    )

    llm = ChatOpenAI(model='gpt-4.1', temperature=0.7)

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

    def retrieve_documents(inputs):
        query = inputs["question"]

        # 제품명 추출 프롬프트
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
                    break

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