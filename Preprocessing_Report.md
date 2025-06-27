# SKN13-3rd-3Team 전처리 결과서



## 원본 데이터

* oliveyoung_cream_*.csv

* oliveyoung_essence_*.csv

* oliveyoung_lotion.csv

* oliveyoung_mist.csv

* oliveyoung_skin.csv

## 주요 요구사항

1. 이상치 및 결측치 처리

2. 데이터 정제(불필요한 단어 및 특수문자)

3. `Document.metadata` 태깅을 위한 처리

    * 제품 **카테고리**

    * 리뷰의 **감성(Sentiment)**

## 세부 항목

### 1. preprocessing.ipynb: 토크나이징 이전 기본적인 전처리

* 불필요한 열 처리: '' 등

* '카테고리' 열 추가

* 리뷰가 100개 미만인 제품을 이상치로 간주하여 삭제

* '별점'을 정수형으로 변환

    > '5점 만점에 4점'  -> 4

* 데이터 정제: 불필요한 특수 문자 제거 및 중복되는 제품명을 하나의 제품으로 통일

---

### 2. prep.ipynb: 문장 단위 토크나이징

* `kss` 라이브러리 기반 토크나이징: `kss.split_sentences`

---

### 3. Sampling.ipynb

* 상품 카테고리 별 리뷰 비율 최대한 반영하여 총 2천 문장의 학습 표본 추출

    > 크림 600개, 에센스 600개, 로션 200개, 미스트 200개, 스킨 200개

* 데이터 라벨링: `GPT-4.1`-based Few-shot Learning

---

### 4. FullFineTuning.ipynb

* `beomi/kcbert-base` 모델에 `리뷰-감성` 샘플로 Full Fine-tuning

* HuggingFace Hub로 관리합니다.

    * [iPad7/kcbert-base-sentiment-0.1b](https://huggingface.co/iPad7/kcbert-base-sentiment-0.1b)

    * [iPad7/kcbert_full_finetuned](https://huggingface.co/iPad7/kcbert_full_finetuned)
    
* 학습 결과

    사진 첨부

---

### 5.  sentiment_prediction.ipynb

* Fine-tuned 모델 별로 전체 데이터셋의 감성을 추론

* 추론 결과를 추가한 담은 테이블 데이터를 HuggingFace Hub에 업로드

* Final Model:`iPad7/kcbert_full_finetuned`

    > 표본 내 검증 데이터셋에서 비교적 높은 오차를 보여주나, 실제 데이터셋에서 추론한 결과를 인간의 눈으로 정성 평가한 결과 해당 모델이 우수한 성능을 보임

