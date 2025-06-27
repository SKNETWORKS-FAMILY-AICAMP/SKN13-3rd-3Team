# SKN13-3rd-3Team
[SK Networks Family AI Camp 13th] 3rd mini project

1. Introduce Team
💡 프로젝트명:
"_____” – 내 피부에 맞는 기초화장품을 빠르게, 똑똑하게 추천해주는 리뷰 기반 AI 챗봇

<table align=center>
  <tbody>
   <tr>
      <td align=center><b>이유나</b></td>
      <td align=center><b>이재범</b></td>
      <td align=center><b>장진슬</b></td>
      <td align=center><b>지형우</b></td>
    </tr>
    <tr>
      <td align="center">
          <img alt="Image" src="https://github.com/user-attachments/assets/45796174-9990-4019-97e7-7e25ab8be320" width="200px;" alt="이유나"/>
      </td>
      <td align="center">
          <img alt="Image" src="https://github.com/user-attachments/assets/188b8f75-4bd7-4589-8429-3b5c2c807166" width="200px;" alt="이재범"/>
      </td>
      <td align="center">
        <img alt="Image" src="https://github.com/user-attachments/assets/453997b3-74e1-4573-92d9-569968b68461" width="200px;" alt="장진슬" />
      </td>
      <td align="center">
        <img alt="Image" src="https://github.com/user-attachments/assets/dce5e0cc-c634-4689-a814-3d14ecb8e3eb" width="200px;" alt="지형우"/>
      </td>
    </tr>
    <tr>
       <td align="center">
       <a href="https://github.com/yunawawa">
         <img src="https://img.shields.io/badge/GitHub-yunawawa-FEFFAB?logo=github" alt="이유나 GitHub"/>
       </a>
       </td>
       <td align="center">
       <a href="https://github.com/iPad7">
         <img src="https://img.shields.io/badge/GitHub-iPad7-8CFF89?logo=github" alt="이재범 GitHub"/>
       </a>
       </td>
       <td align="center">
       <a href="https://github.com/Jennie-ai333">
         <img src="https://img.shields.io/badge/GitHub-Jennie--ai333-FFAFB0?logo=github" alt="장진슬 GitHub"/>
       </a>
       </td>
       <td align="center">
       <a href="https://github.com/JI0617">
         <img src="https://img.shields.io/badge/GitHub-JI0617-DFA4FF?logo=github" alt="지형우 GitHub"/>
       </a>
       </td>
    </tr>
  </tbody>
</table>
<br>
<br><br>



2. Project Overview

## ✅ 프로젝트 소개

**"생각해보지 않았지만 우리 모두의 불편함 : 내 피부에 맞는 기초 화장품 찾기가 어렵다!"**
화장품을 구매하려고 올리브영 오프라인 혹은 온라인 매장을 방문하면, 수 많은 제품들에게 압도당해 어떤 제품이 내  ㅣ부에 맞는지 판단하기 어렵습니다. 특히 새로운 제품을 시도할때 실패에 대한 불안과 기회비용, 시간의 부담이 발생합니다. <br>

많은 소비자들은 유튜브에서 '추천템'을 보고 제품을 구매하는데, 상업적, 광고성 콘텐츠가 비중이 커서 신뢰하기 어렵고, 원하는 조건의 제품을 찾기 위해서는 다수의 영상을 하나하나 시청해야하는 높은 탐색 비용이 발생합니다. <br>

<img src="img/유투버화장품추천1.png" width="300"/>
<img src="img/유투버화장품추천2.png" width="300"/>

이에 우리 팀은 올리브영 스킨케어 제품에 대한 최신 리뷰 약 100만 건을 수집하였습니다. 이를 기반으로 **LLM 기반 RAG(Retrieval-Augmented Generation)** 구조로 구현된 **기초 화장품 추천 챗봇**을 구현했습니다. <br>

이 챗봇은 사용자의 **피부타입, 피부고민, 선호제형, 민감도**등 다양한 조건을 바탕으로 사용자의 피부 조건에 맞는 제품 추천 및 리뷰 요약, 트렌드, 사용자 불만 요소까지 제공합니다. <br>

이 프로젝트는 반복적인 검색과 제품 비교로부터 소비자의 피로도를 줄이고, **신뢰할 수 있는 실제 사용자 리뷰 기반**의 추천을 통해 개인의 피부에 맞는, **더 나은 화장품 선택 경험을 제공**하는 것을 목표로 합니다. <br>

- 여기에 우리 애플리케이션 캡쳐를 넣어도 - 


## ✅ 프로젝트 목표

### 📌 기술적 목표
1. 최신 리뷰 데이터 기반 RAG 챗봇 서비스 구현
- 약 100만 건의 올리브영 스킨케어 리뷰를 크롤링하여 벡터DB를 구축하고, 이를 RAG(Retrieval-Augmented Generation) 구조에 맞춰 질의응답형 추천 챗봇으로 구성 <br><br>

2. 리뷰 임베딩 + 메타데이터 기반 하이브리드 검색 시스템 구축
- 피부타입, 고민, 자극도 등 의미 있는 속성을 메타데이터로 추출하고, 유사도 기반 벡터 검색과 함께 정밀한 필터링 제공 <br><br>

3. 감정 분석 및 키워드 태깅을 통한 리뷰 구조화 자동화
- 한국어 리뷰를 문장 단위로 분석하여 긍·부정 감정 및 주요 키워드를 자동 태깅, LLM 기반 응답의 정밀도 향상 <br><br>

4. LangChain 기반 질의 응답 파이프라인 최적화
- 사용자 쿼리에 따른 Top-K 리뷰 검색 → Prompt 삽입 → 응답 생성을 체계화하여 빠르고 일관된 응답 생성 가능 <br><br>


### 🎯 사용자 가치 목표

1. 피부 타입과 상황에 맞는 개인 맞춤형 제품, 대체제 추천 제공
- “지성 피부에 진정 효과 좋은 수분크림 추천해줘”와 같은 구체적인 요청에 적합한 제품을 빠르게 추천<br>
- “건성 피부에 보습 잘 되는 수분 크림 추천해줘” 같은 질문에 맞춤형 응답 제공 <br>
- “이 제품 트러블 난다는 리뷰가 많은데 대체 제품은 뭐야?”에 대한 응답 처리 <br><br>
  
2. 소비자의 탐색 비용을 절감하고, 신뢰할 수 있는 제품 선택 경험 제공
- 유튜브 영상, 후기 수집 등 반복적이고 비효율적인 탐색 과정을 챗봇 한 번의 질의로 대체<br><br>
  
3. 신뢰 가능한 리뷰 요약과 부정적 경험 분석 제공
- 리뷰 기반의 객관적 정보에 따라 합리적인 제품 선택을 유도 <br>
- 실제 사용자들의 집단 지성을 바탕으로 한 정보로 제품 선택 신뢰도 향상<br><br>

4. 제품 선택 실패에 대한 불안과 기회비용 감소
- 기존 제품의 문제점(예: 트러블, 끈적임 등)을 미리 파악하고, 대체 제품을 함께 제안하여 구매 리스크 완화<br><br>

--------------------------------------------
# 3. Architecture - 시스템 아키텍처 구성도

[User Input]
     ⬇  
[Natural Language Query]
     ⬇  
[Keyword + Emotion 분석]  
     ⬇  
[Retriever]
  └─  /  벡터DB
        (리뷰 텍스트 + 메타데이터 기반)
     ⬇  
[Top-K 리뷰 추출]
     ⬇  
[Prompt Template + Context Injection]
     ⬇  
[LLM (OpenAI GPT / Ko-LLM 등)]
     ⬇  
[Final Answer 생성]


--------------------------------------------

# Data Search
✅ 주요 기술 스택
데이터 수집: Selenium 기반 크롤링 (올리브영 약 2,500개 제품 + 리뷰 약 100만 건)

데이터 전처리: 정규표현식 기반 텍스트 클리닝, 제품명/브랜드 정제

감정분석: 어떻게 했는지 쓰기 

메타데이터 생성: 키워드 + 감정분석 기반 메타 태깅 (피부타입, 고민, 제형, 자극도 등)

백엔드: Chroma 벡터스토어 기반 LangChain RAG

모델: <> 기반 감정 분류 모델, SentenceTransformer 임베딩

응답 시스템: 사용자 쿼리에 따른 조건 검색 + 유사도 검색 + LLM 응답 조합


--------------------------------------------

# Preprocessing
## cleansing, outliers, and missing values
1. 결측치를 제거합니다.
2. 제품명에 들어간 불필요한 요소를 전처리합니다.
    - ‘리필’ 또는 ‘기획’이 들어간 경우 데이터 포인트 자체를 제거합니다.
    - 괄호(`[]`, `()` 등)와 괄호 안의 문자열을 제거합니다.
    - 제품명에 증정품 관련 문자열이 있는 경우 제거한 후, 사실상 같은 제품이었다고 판단되는 것들을 하나로 합칩니다.
    - ‘A사 a 로션 + 토너 50ml’의 경우 ‘ + 토너 50ml’를 제품명에서 제거합니다.
            - e.g. <예시 사진으로 넣기>
3. 리뷰가 100개 미만인 제품은 이상치로 간주하여 제거합니다.

<img src="img/올리브영(제품명).png" width="600"/>

--------------------------------------------
  
## Sentiment Analysis
1. 학습 표본(X_train)을 추출합니다(총 n개의 문장. 2천 개 정도면 되려나요?)
2. 표본에서 학습에 활용할 ground truth label(y_train)을 생성합니다.
    - `gpt-4.1` 을 활용하여 LLM-based Few-shot Learning을 수행합니다.
    - `gpt-4.1`에 전달할 프롬프트가 굉장히 중요할 것 같습니다.
3. HuggingFace Hub Pre-trained Sentiment Analysis 모델을 미세조정합니다.
    - `beomi/kcbert-base`, `klue/roberta-large`, `tabularisai/multilingual-semtiment-analysis` , etc.
    - LoRA(Low-Rank Adaptation)
4. 전체 데이터의 label을 예측합니다.



--------------------------------------------
# Vector DB




--------------------------------------------
# RAG - Chain 



--------------------------------------------
# RAG-based QA Chatbot 구현 




--------------------------------------------
### How to Use
💻 사용자 인터페이스 <화면 캡쳐>

Step 1. 질문 입력
ex) “복합성 피부에 진정 잘 되는 크림 5개 추천해줘”  
ex) “트러블 나지 않는 수분크림 중 인기 많은 거 있어?”

Step 2. 후속 질문 (내부검색 Memory)
ex) "이 제품들 중 '보습력'을 가장 긍정적으로 평가한 제품은 뭐야?”
ex) "해당 제품 리뷰에서 트러블을 언급한 비율은 몇 %야?" 

Step 3. 답변 생성
- 제품명 + 간단한 설명 + 긍/부정 요약
- 비슷한 제품, 대체제 등 추가 정보 포함


5. Query - Answer Examples
🧪 예시 1 — 피부 고민 기반 추천
Q: “건성 피부에 잘 맞는 순한 에센스 추천해줘”
A: “사용자 리뷰에서 건성 피부와 관련된 ‘보습’, ‘촉촉해요’, ‘순해요’ 등의 키워드를 기반으로 필터링된 결과입니다.”
[에센스 A]: 흡수 빠르고 유분기 없음. 보습력 우수
[에센스 B]: 민감성 피부에도 자극 없음. 무향 무색소

🧪 예시 2 — 제품 불만 요약 + 대체 제품 제안
Q: “요즘 ‘피부 뒤집어졌어요’ 이런 말 많은 제품 있어?”
A: “‘크림 X’ 제품에서 ‘트러블’, ‘뾰루지’, ‘따갑다’ 등의 부정적 감정 표현이 높은 빈도로 나타납니다.”
🔄 대체 추천: ‘크림 Y’, ‘크림 Z’ (순한 성분 + 피부 진정 키워드 다수)


--------------------------------------------


# 확장 가능성 및 향후 활용 방향
본 프로젝트에서 구축한 리뷰 기반 RAG(Retrieval-Augmented Generation) 시스템은 특정 도메인(올리브영 스킨케어)에 한정되지 않고, 다양한 제품군 및 플랫폼으로의 확장이 가능합니다.<br>

우선, 올리브영 내 다른 카테고리(바디케어, 헤어케어, 색조 화장품 등)로의 확장은 데이터 구조와 메타데이터 스키마를 동일하게 적용할 수 있어, 기술적 난이도가 비교적 낮습니다. 동일한 리뷰 기반 추천 구조를 바탕으로 사용자의 다양한 니즈에 대응할 수 있습니다.<br>

더 나아가, 본 시스템은 화장품 카테고리를 넘어 패션, 생필품, 전자기기 등 다양한 소비재 전반으로도 확장 가능합니다. 각 도메인에 맞는 키워드 사전과 메타데이터 정의 체계만 구축된다면,<br>

* 사용자 리뷰에 기반한 질의응답,<br>
* 제품 추천,<br>
* 사용 후기 요약 및 부정적 반응 감지 등<br>
의 기능을 손쉽게 이식할 수 있습니다.<br>

특히 온라인 쇼핑몰에서 제공하는 리뷰는 대부분 비정형 텍스트 + 사용자 메타 정보 형태로 존재하기 때문에, 본 프로젝트의 처리 방식(자연어 임베딩, 감성 분석, 키워드 태깅)은 범용적인 적용이 가능합니다. 또한 챗봇 인터페이스를 통해 검색 과정의 불편을 줄이고, 사용자 중심의 인터랙티브 쇼핑 경험을 제공할 수 있어 실질적인 서비스 개선 효과도 기대할 수 있습니다.<br>

향후에는 제품 리뷰뿐 아니라 유튜브 자막, 블로그 콘텐츠, SNS 텍스트 등 다양한 외부 데이터 소스와 결합하여, 보다 입체적인 멀티모달 리뷰 기반 추천 시스템으로 발전시킬 수 있으며, 이는 전자상거래 플랫폼, 브랜드 마케팅, 소비자 리서치 등 다양한 분야에서 활용될 수 있습니다.<br>
