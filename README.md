# Vibe Coding Assistant (Week 2)

## 🎯 프로젝트 개요

FastAPI 백엔드와 Streamlit 프론트엔드를 활용한 AI 챗봇 시스템입니다.
LangGraph Agent가 도구를 사용하여 사용자 질문에 지능적으로 응답합니다.

## 🚀 주요 기능

- **FastAPI 백엔드**: 고성능 REST API 서버
- **Streamlit 프론트엔드**: 직관적인 웹 인터페이스
- **LangGraph Agent**: 도구 사용이 가능한 AI 에이전트
- **Gemini LLM**: Google의 최신 언어 모델 활용
- **웹 검색 도구**: 실시간 정보 검색 기능

## 🛠️ 기술 스택

### Backend

- **FastAPI**: 현대적이고 빠른 웹 프레임워크
- **LangGraph**: AI 에이전트 오케스트레이션
- **Gemini**: Google의 생성형 AI 모델
- **DuckDuckGo Search**: 웹 검색 도구

### Frontend

- **Streamlit**: 데이터 앱 구축을 위한 프레임워크
- **Python**: 백엔드와 동일한 언어로 일관성 유지

### Development & DevOps

- **GitHub Actions**: CI/CD 자동화
- **pytest**: 테스트 프레임워크
- **Docker**: 컨테이너화 (향후 계획)

## 📁 프로젝트 구조

```
vibe_coding_w2-1/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py        # 메인 애플리케이션
│   │   ├── models.py      # 데이터 모델
│   │   └── routers/       # API 라우터
│   └── requirements.txt   # 백엔드 의존성
├── frontend/              # Streamlit 프론트엔드
│   ├── app.py            # 메인 앱
│   └── requirements.txt  # 프론트엔드 의존성
├── tests/                # 테스트 파일들
├── docs/                 # 문서
├── .github/              # GitHub Actions & 템플릿
└── .cursor/              # 개발 규칙 및 가이드
```

## 🚀 빠른 시작

### 환경 설정

1. **저장소 클론**

```bash
git clone https://github.com/smileeunsong/vibe_coding_w2-2.git
cd vibe_coding_w2-2
```

2. **가상환경 생성 및 활성화**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

3. **환경 변수 설정**

```bash
cp .env.example .env
# .env 파일에서 API 키 설정
```

### 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

서버가 http://localhost:8000 에서 실행됩니다.

### 프론트엔드 실행

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

앱이 http://localhost:8501 에서 실행됩니다.

### 편리한 실행 스크립트

```bash
# 백엔드 실행
./start_backend.sh

# 프론트엔드 실행
./start_frontend.sh
```

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest tests/ -v

# 특정 테스트 실행
pytest tests/test_chat_api.py -v

# 커버리지와 함께 실행
pytest tests/ --cov=backend --cov=frontend
```

## 📊 GitHub Actions

프로젝트는 다음과 같은 자동화된 워크플로우를 포함합니다:

### CI/CD 파이프라인

- **자동 테스트**: Push/PR 시 테스트 자동 실행
- **코드 품질**: flake8, black, bandit 등으로 품질 검사
- **테스트 커버리지**: 커버리지 리포트 자동 생성

### PR 자동화

- **자동 할당**: 브랜치명 기반 리뷰어 자동 할당
- **자동 라벨링**: 변경 내용 기반 라벨 자동 적용
- **자동 댓글**: PR 분석 및 체크리스트 자동 생성
- **코드 리뷰**: 자동 코드 품질 검사 및 리뷰

### 이슈 관리

- **자동 할당**: 이슈 유형별 담당자 자동 할당
- **자동 라벨링**: 내용 분석 기반 라벨 자동 적용
- **환영 메시지**: 이슈 유형별 자동 안내 댓글

## 📋 개발 가이드

### 브랜치 전략

- `main`: 프로덕션 브랜치
- `develop`: 개발 브랜치
- `feature/*`: 새 기능 개발
- `bugfix/*`: 버그 수정
- `hotfix/*`: 긴급 수정

### 커밋 컨벤션

```
feat: 새 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 추가/수정
chore: 빌드/설정 변경
```

### PR 생성 가이드

1. 적절한 브랜치명 사용 (`feature/`, `bugfix/` 등)
2. 명확한 PR 제목과 설명 작성
3. 관련 이슈 링크
4. 테스트 결과 포함
5. 리뷰어 지정 (자동 할당됨)

## 🔧 개발 도구

### 코드 품질

```bash
# 코드 포맷팅
black backend/ frontend/

# Import 정렬
isort backend/ frontend/

# 린팅
flake8 backend/ frontend/

# 보안 검사
bandit -r backend/
```

### 타입 체킹

```bash
mypy backend/ frontend/
```

## 📚 API 문서

백엔드 서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 주요 태스크 (Development Tasks)

| Task ID  | 제목                          | 상태      | 우선순위 |
| -------- | ----------------------------- | --------- | -------- |
| TASK-001 | 프로젝트 구조 및 환경 설정    | ✅ 완료   | High     |
| TASK-002 | FastAPI 백엔드 기본 구조 구현 | 🚧 진행중 | High     |
| TASK-003 | LangGraph Agent 구현          | ⏳ 대기   | High     |
| TASK-004 | Streamlit 프론트엔드 구현     | ⏳ 대기   | High     |

## 🆕 테스트 섹션

이 섹션은 GitHub Actions의 자동화 기능을 테스트하기 위해 추가되었습니다.

### 🧪 자동화 테스트 확인사항

- [x] PR 생성시 자동 댓글 등록
- [x] 브랜치명 기반 자동 라벨링
- [x] 자동 리뷰어 할당
- [x] 코드 품질 자동 검사
- [x] 테스트 자동 실행

### 📝 테스트 시나리오

1. `pr_test` 브랜치에서 간단한 파일 수정
2. 커밋 후 GitHub에 푸시
3. Pull Request 생성
4. 자동화 워크플로우 동작 확인

이 테스트를 통해 우리의 GitHub Actions 워크플로우가 올바르게 작동하는지 확인할 수 있습니다! 🚀

## 🤝 기여하기

1. 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'feat: Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📞 지원

문제가 발생하거나 질문이 있으시면:

1. **이슈 생성**: GitHub Issues를 통해 버그 신고나 기능 요청
2. **토론**: GitHub Discussions에서 일반적인 질문
3. **문서 확인**: `docs/` 폴더의 추가 문서들

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

**Happy Coding!** 🎉
