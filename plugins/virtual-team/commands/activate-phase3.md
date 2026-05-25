---
description: 특정 제품에 대해 Phase 3(테스트·배포·모니터링·장애관리)를 활성화한다.
argument-hint: <product-slug>
---

운영자가 제품 **$ARGUMENTS** 에 대해 Phase 3(운영) 단계를 활성화했다. 이제 아래 휴면 에이전트를 워크플로우에 편입할 수 있다.

## 활성화되는 파트
- **tester-client / tester-api** — 테스트 설계·실행·회귀
- **deploy-ios / deploy-android / deploy-web / deploy-server / deploy-db** — 배포 파이프라인
- **incident-server / incident-client / incident-feedback** — 모니터링·장애 대응·고객 반응

## 진행 지침
1. 현재 `records/$ARGUMENTS/`의 상태(기획·개발 산출물)를 확인한다.
2. 우선 **테스트** 파트로 품질 게이트를 세운다(테스트 작성=sonnet, 실패 분석=opus).
3. **배포** 파트로 파이프라인을 구성한다. **실제 배포·prod 변경·스토어 제출·DB 적용은 반드시 운영자 승인** 후 진행(파이프라인 구성/드라이런까지는 자율).
4. **모니터링/장애** 파트로 SLI/SLO·알람을 세우고, 인시던트 트리아지(opus)·postmortem을 `records/$ARGUMENTS/incidents/`에 남긴다.
5. 각 단계 결과와 승인이 필요한 항목을 운영자에게 보고한다.

## 규칙
- 모델: 실행=sonnet, 분석·트리아지=opus, 수집=haiku.
- 모든 배포/운영 위험 작업은 §6 자율성 규칙에 따라 운영자 승인 게이트를 거친다.
