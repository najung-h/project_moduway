# AI 강좌분석 아키텍쳐

<br>

## 1. 개요

Comparisons 앱은

사용자가 입력한 `학습 목표(자연어)`/`가용시간`/`학습 결정 요인의 중요도`/`비교 대상강좌`를 토대로,

AI와 규칙 기반의 로직을 결합하여

강좌를 비교분석해주는 백엔드 로직을 포함하고 있습니다.

---

<br>

# 2. 

[특이사항]

- Django REST Framework 기반

- LLM + 전통적인 비즈니스 로직 혼합 구조

- "즉시 생성"과 "사전 생성" 데이터를 명확히 분리하여 성능과 확장성 고려

  | 구분          | 설명                       | 저장 여부    |
  | ------------- | -------------------------- | ------------ |
  | **사전 생성** | 강좌 자체의 고정적 특성    | DB 저장      |
  | **즉시 생성** | 사용자 맥락·리뷰 변화 반영 | 요청 시 생성 |

  - LLM 강좌 분석은 사전 생성후 DB에 저장하여 호출함
    - 강좌의 데이터는 가끔 바뀌기 때문
  - LLM 리뷰 분석은 사용자의 요청시점에 따라 그때까지 달린 최신 30개 댓글을 실시간으로 분석함
    - 리뷰 데이터는 최신성이 중요하기 때문



[주의사항]

MVP 서비스이므로, 일단은 DB에 사용자가 입력한 학습 목표, 가용시간, 분석 대상 강의, 학습 결정 요인의 중요도를 저장하지 않는다.

---

## 3. 전체 아키텍처

```
                     ┌─────────────────────┐
                     │    Frontend (Vue)   │
                     │   - 강좌 비교 UI      │
                     │   - 결과 시각화        │
                     └──────────┬──────────┘
                                │ RESTful API (JSON)
                                ▼
         ┌──────────────────────────────────────────────┐
         │         Django REST Framework                │
         │                                              │
         │  ┌─────────────────────────────────────────┐ │
         │  │     API Layer (Views + Serializers)     │ │
         │  │          - 요청 검증                      │ │
         │  │          - 응답 직렬화                     │ │
         │  │          - 에러 처리                       │ │
         │  └────────────┬────────────────────────────┘ │
         │               ▼                              │
         │  ┌─────────────────────────────────────────┐ │
         │  │      Service Layer (비즈니스 로직)          │ │
         │  │     ┌──────────┐  ┌──────────┐           │ │
         │  │     │   LLM    │  │ Sentiment│           │ │
         │  │     │  Service │  │  Service │           │ │
         │  │     └──────────┘  └──────────┘           │ │
         │  │     ┌──────────┐  ┌──────────┐           │ │
         │  │     │ Timeline │  │  Score   │           │ │
         │  │     │  Service │  │  Service │           │ │
         │  │     └──────────┘  └──────────┘           │ │
         │  └────────────┬────────────────────────────┘ │
         │               ▼                              │
         │  ┌─────────────────────────────────────────┐ │
         │  │     Data Access Layer (ORM Models)      │ │
         │  │             - Course                    │ │
         │  │             - CourseAIReview            │ │
         │  │             - CourseReview              │ │
         │  └──────────────────┬──────────────────────┘ │
         └─────────────────────┼────────────────────────┘
                               ▼
                     ┌───────────────────────┐
                     │  PostgreSQL + pgvector│
                     └───────────────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   GMS API (OpenAI)    │
                     │   - gpt-4o-mini       │
                     └───────────────────────┘
    
                
                             [Future]
                     - Redis Cache (응답 / 임베딩)
                     - Celery + Async LLM 호출
```

<br>

------

## 4. API 구성

### 4.1 Endpoints

```
- POST  /api/v1/comparisons/analyze/                                 - 강좌 비교 분석
- GET   /api/v1/comparisons/courses/<int:course_id>/ai-review/       - AI 평가 조회
- GET   /api/v1/comparisons/courses/<int:course_id>/review-summary/  - 강좌 리뷰 요약 조회
```

### 4.2 URL 구조

```
/api/v1/comparisons/
├── analyze/                      # 강좌 비교 분석
└── courses/
    └── {course_id}/
        ├── ai-review/            # AI 평가 조회
        └── review-summary/       # 리뷰 요약 조회
```

------

<br>

## 5. Serializers 구성

```
0. 사용자 입력 검증
0.1  UserPreferencesSerializer             | 사용자 선호도 입력 검증

1. AI 코멘트
1.1  PersonalizedCommentSerializer          | AI 맞춤 코멘트 응답 직렬화
1.2.1  ReviewContentSerializer              | 리뷰 요약 응답 직렬화 (1.2 간단)
1.2.2  ReviewSummarySerializer              | 리뷰 요약 응답 직렬화 (1.2 상세)

2. 강좌 관련
2.1  SimpleCourseSerializer                |  강좌 비교 분석 결과에서 강좌 기본 정보 제공

3. AI 평가 관련
3.1 CourseAIReviewSerializer               | LLM이 기생성한 강좌 평가 정보 제공
3.2 CourseAIReviewDetailSerializer         | 특정 강좌의 AI 평가 상세 조회용

4. 부가 Serializer
4.1  SentimentResultSerializer             | 감성분석 결과 직렬화
4.2  TimelineResultSerializer              | 타임라인 시뮬레이션 결과 직렬화

5. 강좌 비교 분석 Request/Response
5.1  ComparisonAnalyzeRequestSerializer    | 강좌 비교 분석 요청 검증
5.2  ComparisonResultSerializer            | 강좌별 비교 분석 결과 직렬화
5.3  ComparisonAnalyzeResponseSerializer   | 강좌 비교 분석 최종 응답 직렬화
```

------

<br>

## 6. Views 구성

```
1. 강좌 비교 분석
1.1 ComparisonAnalyzeView      | 강좌 비교 분석 API

2. 강좌 AI 평가 조회
2.1 CourseAIReviewDetailView   | 강좌 AI 평가 조회 API

3. 리뷰 요약 생성
3.1 CourseReviewSummaryView    | 강좌 리뷰 요약 생성 API
```



---

<br>
