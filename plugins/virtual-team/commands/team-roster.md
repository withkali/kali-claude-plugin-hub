---
description: 가상 개발팀의 역할 로스터와 모델/단계 정책을 출력한다.
---

가상 개발팀(`virtual-team`)의 구성을 운영자에게 정리해 보여줘라. 아래 내용을 표로 제시한다.

## 활성 (Phase 1-2)
- **planner** (opus) — 기획자: 기획서 작성/보강
- **designer** (opus) — UX/UI 설계, 디자인 스펙
- **client-ios** (sonnet) — iOS(Swift/SwiftUI)
- **client-android** (sonnet) — Android(Kotlin/Compose)
- **client-crossplatform** (sonnet) — RN/Flutter
- **web-ui** (sonnet) — CSS 기반 UI 구현
- **web-frontend** (sonnet) — React/Next 프론트
- **server-dba** (sonnet) — DBA/코어, 스키마 설계는 opus
- **server-api** (sonnet) — 서비스 API/비즈니스, 계약 설계는 opus
- **infra-config** (sonnet) — 인프라 구성(IaC)
- **infra-monitoring** (sonnet) — 관측가능성/알람
- **researcher** (haiku) — 웹 검색·fetch 전담

## 휴면 (Phase 3 — /activate-phase3로 활성화)
- **tester-client / tester-api** (sonnet)
- **deploy-ios / deploy-android / deploy-web / deploy-server / deploy-db** (sonnet)
- **incident-server / incident-client** (opus) / **incident-feedback** (opus)

## 정책 요약
- 모델: 검색=haiku, 실행=sonnet, 기획·설계·분석=opus (작업 유형 기준, 호출 시 오버라이드)
- 보안: 시크릿 하드코딩 금지 + secret-scan 훅 자동 차단
- 자율성: 로컬·가역 자동 / 원격·배포·prod·시크릿은 운영자 승인
- 새 서비스 시작: `/new-service <아이디어>`
