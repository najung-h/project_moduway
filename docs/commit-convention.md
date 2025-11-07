# Commit Convention Specification

<br>

## 1. 목적 (Purpose)

본 문서는 팀 내 Git 커밋 메시지 규칙(Commit Convention)을 정의하여,
 일관된 변경 이력 관리와 명확한 변경 의도 전달을 목표로 한다.

<br><br>

## 2. 기본 구조 (Structure)

모든 커밋 메시지는 다음 형식을 따른다.

```
type(scope): subject
```

- **type**: 커밋의 성격 (필수)
- **scope**: 변경 범위 또는 모듈명 (선택)
- **subject**: 변경 요약 (필수, 50자 이내)

예시:

```
feat(user-auth): 로그인 API 연동 기능 추가
fix(payment): 결제 오류 수정
```

<br>

<br>

## 3. Type 규칙

| Type      | Description                                  |
| --------- | -------------------------------------------- |
| ✨feat     | 신규 기능 추가                               |
| 🐛fix      | 버그 수정                                    |
| 📝docs     | 문서 관련 변경                               |
| ♻️refactor | 기능 변경 없는 코드 구조 개선                |
| 🚀deploy   | CI/CD 설정 변경                              |
| 🔧chore    | 기능 외 자잘한 수정 (예: 설정, 환경 파일 등) |
| ✏rename   | 파일 또는 폴더명 변경만 수행                 |
| 🗑️remove   | 불필요한 파일 또는 코드 삭제                 |

<br>

<br>

## 4. Subject 규칙

- 메시지는 간결하고 명확하게 작성한다. (50자 이내)
- 변경 내용을 한눈에 파악할 수 있게 작성한다.

<br>

<br>

## 5. Body (선택사항)

- `subject` 아래 한 줄을 띄우고, 구체적인 변경 내용을 기술한다.
-  무엇을, 왜, 어떻게 수정했는지를 중심으로 작성한다.
- 각 줄은 72자 이내로 작성 권장
- 필요 시 여러 문단으로 구분 가능

예시:

```
refactor(user): 유효성 검사 로직 분리

기존 중복된 validation 로직을 common/utils로 이동하여 재사용성을 확보함.
이로 인해 중복 코드 감소 및 유지보수 효율성이 향상됨.
```

<br><br>

## 6. Footer (선택사항)

이슈 번호 또는 주요 변경사항을 기록한다.

- `BREAKING CHANGE:` 이전 버전과 호환되지 않는 변경 시
- `Closes #이슈번호`, `Fixes #이슈번호` 형태로 작성 가능

예시:

```
fix: 잘못된 쿼리 파라미터 수정

Closes #124
```

<br><br>

## 7. 작성 규칙 요약

- 커밋은 **의미 있는 최소 단위**로 분리한다.
- **하나의 커밋에는 하나의 목적**만 포함한다.
- PR 리뷰 시 `type`과 `scope`를 통해 변경 목적을 명확히 한다.
- 팀 전체가 동일한 형식을 준수하며, 필요 시 **commitlint**로 자동 검증한다.

<br><br>

## 8. 예시 목록

```
feat: 회원가입 시 이메일 중복 검사 기능 추가
fix(auth): 토큰 만료 시 자동 로그아웃 처리
docs: README 설치 가이드 보완
refactor: userService 로직 분리 및 함수명 수정
deploy: GitHub Actions 테스트 단계 추가
chore: ESLint 설정 파일 업데이트
rename: Home.js → MainPage.js
remove: 사용하지 않는 mock 데이터 삭제
```

<br><br>