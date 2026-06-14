# iOS / SwiftUI 함정 체크리스트 (client-ios 필독)

빌드는 통과하지만 **런타임에서 깨지는** 반복 함정 모음. 화면·입력·표시(presentation)를 다룰 때 구현 전·후로 점검한다. (MANUAL.md §9와 함께.)

---

## 1. presentation 모디파이어 (.sheet / .fullScreenCover / .alert / .confirmationDialog)

**증상 사례:** 시트가 뜨자마자 즉시 닫힘 / 두 번째 진입에야 뜸 / 삭제 확인 다이얼로그 대신 엉뚱한 시트가 뜸.

규칙:
- **Form/List의 Row(Section) 안에 presentation 모디파이어를 붙이지 말 것.** Row는 스크롤·재구성으로 재식별되어 `isPresented` 토글이 즉시 리셋 → 시트가 바로 닫힌다. presentation은 **List/Form/NavigationStack 등 안정적인 컨테이너 레벨(또는 그 바깥 뷰)** 에 1개만 부착한다.
- presentation을 트리거하는 `@State Bool`/`item`이 **부모 리렌더로 리셋되지 않게** 한다(@ObservedObject 관찰 뷰의 잦은 리렌더 주의 → §2).
- **한 뷰에 여러 presentation 상태가 공존하면 충돌**한다. 각 상태는 별도 모디파이어로, 동시에 두 개가 true가 되지 않게 상호배타로 관리. 가능하면 `enum`(예: `enum ActiveSheet: Identifiable { case email, delete }` + `.sheet(item:)`)으로 단일화.
- 확인/경고는 `.alert` 또는 `.confirmationDialog` — **시트로 대체하지 말 것**. 버튼 액션이 올바른 상태만 켜는지 확인(삭제 버튼이 시트 Bool을 켜는 실수 흔함).
- 시트는 별도 presentation 컨텍스트라 **그 내부 입력은 Form 리렌더 영향을 받지 않는다** — 다단계 입력(이메일→코드 등)은 시트로 묶는 게 안전.

자가 점검: 시트 첫 진입에 바로 뜨는가? 즉시 닫히지 않는가? 같은 화면의 다른 버튼(삭제 등)이 의도한 dialog/sheet를 정확히 띄우는가?

---

## 2. 상태/바인딩 유실 (특히 입력 폼·CJK/IME)

**증상 사례:** TextField에 입력했는데 저장 시 빈 값/0자 / 한글이 조합 중 사라짐.

규칙:
- **싱글톤 `@ObservedObject`(예: `AuthManager.shared`)를 관찰하는 뷰**는 그 객체가 `@Published`를 방출할 때마다 통째로 리렌더된다. 이 뷰 안의 `TextField` 입력 중 리렌더가 일어나면, 특히 **한글/일본어/중국어 IME 조합(marked text)이 커밋 전에 날아간다.**
- **입력 폼은 격리된 자식 뷰로 분리**한다: 자식은 자기 `@State text`만 갖고 **상위 ObservableObject를 관찰하지 않으며**, 결과는 **콜백(클로저)** 으로 부모에 전달. 부모의 잦은 리렌더가 입력칸을 건드리지 못하게.
- 매 키 입력마다 부모 `@State`를 바꾸는 `.onChange`(예: 가용성 리셋)는 부모 리렌더를 유발 → 입력칸이 자식 안에 있게 하고 그 처리도 자식 로컬 상태로.
- TextField에 변하는 `.id()`를 주지 말 것(재식별 → 입력 유실).
- 비동기 호출 직전 **값을 지역 상수로 캡처**(`let v = text`)해 await 중 상태 변화의 영향을 차단.

자가 점검: 입력 후(빈 값/연속 입력/한글) 실제로 전송·저장되는 값이 입력값과 같은가? 전송 본문을 로그/네트워크로 한 번 의심해보라.

---

## 3. "빌드 성공"으로 못 잡는 것 — 반드시 별도 확인
- **다국어/IME 입력**(한글), **빈 입력/경계값**(0자, 최대 길이), **재진입·취소·연속 탭**, **네트워크 실패 응답 처리**, **권한/인증 상태별 분기**, **SwiftData 마이그레이션**(optional/default만, 디바이스 실기 기동), **CloudKit 컨테이너/엔타이틀먼트 일치**.
- supabase-swift 등 SDK: **비-2xx 응답은 throw**되어 `{ok:false,reason}` 바디를 직접 못 읽을 수 있다 → 에러 객체의 응답 data에서 reason을 파싱하거나, 서버가 비즈니스 실패를 200+{ok:false}로 주도록 합의.

---

## 4. 마이그레이션/스키마 (SwiftData)
- 신규 필드는 **optional 또는 explicit default**만(라이트웨이트). 명시 migrationPlan의 잘못된 버전 스냅샷이 스플래시 크래시를 유발한 전력 — 검증 안 된 migrationPlan 도입 금지, 실패 시 로컬 스토어 복구 폴백 유지.
- 단위테스트(inMemory)는 통과해도 **디바이스의 기존 로컬 스토어 마이그레이션**은 별개 — 실기 기동 확인.

---

## 5. 디자인 토큰/시스템
- 색·폰트·간격은 디자인 시스템 토큰만(`Color.brand`, `Font.*`, `DS.*`). 하드코딩 금지.
- Form Section 위 `overlay` 토스트는 레이아웃이 깨진다 — 토스트는 컨테이너 레벨/별도 표시, 또는 `.alert` 사용.

---

## 구현 직전 30초 셀프체크
1. 이 화면에 presentation(sheet/alert/dialog)을 Row가 아니라 안정 컨테이너에 붙였나? 여러 개면 충돌 안 하나?
2. 입력 폼이 싱글톤 관찰 뷰 안에서 리렌더로 유실되지 않나? (필요하면 자식 뷰로 격리)
3. 한글/빈값/재진입/취소/연속탭/네트워크 실패를 따져봤나?
4. 직전에 고친 동일 계열 버그가 이 코드에도 숨어있지 않나?
5. 보고에 "검증함 / 검증 못 함"을 분리해 적었나?
