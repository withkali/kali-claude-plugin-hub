# iOS 무료 디자인 툴박스 (SwiftUI)

> designer / client-ios 가 "상용 앱 완성도"를 낼 때 참고하는 무료 리소스·컴포넌트 카탈로그.
> 원칙: **SwiftUI/SF Symbols 내장을 뼈대로** 하고, 아래를 더해 "기본 앱 느낌"을 탈피한다.
> 외부 SPM 의존을 추가할 땐 빌드 안정성(네트워크 resolve)·라이선스·유지보수를 고려하고,
> 불확실하면 **네이티브 동등 구현 + 본 문서에 라이브러리 옵션 명시**로 간다.

## 1. 내장(무의존) — 1순위로 활용
- **SF Symbols** — 5,000+ 공식 아이콘. 가변 weight/scale, `.hierarchical`/`.palette`/`.multicolor` 렌더링, symbol effects(bounce/pulse/variableColor) 애니메이션.
- **Swift Charts**(iOS 16+) — 막대/링(SectorMark)/라인. 학습 진척 대시보드(외움/틀림/미학습 비율, 주간 추이)를 순정 앱 느낌으로.
- **AVSpeechSynthesizer**(`AVFoundation`) — 무료 네이티브 TTS. 단어 발음(미/영) 재생. 단어장 앱 필수.
- **SwiftUI 제스처/애니메이션** — `rotation3DEffect`(플래시카드 플립), `DragGesture`(틴더식 스와이프: 우=외움/좌=틀림), `matchedGeometryEffect`, spring. 외부 카드 라이브러리 없이 플래시카드 "맛" 구현 가능.
- **네이티브 컨페티** — `TimelineView`+`Canvas` 또는 간단한 파티클 뷰로 성취 이펙트(무의존).
- **머티리얼/시맨틱 컬러** — `.thinMaterial`, `.regularMaterial`, semantic colors로 깊이감.

## 2. 외부 오픈소스 (필요 시 SPM 추가 — 옵트인)
- **Lottie**(`airbnb/lottie-ios`) — LottieFiles 무료 벡터 애니메이션(.json/.lottie). 성공 체크·로딩·축하. (애니메이션 에셋 번들 필요)
- **EffectsLibrary** — SwiftUI 전용 컨페티/파티클(꽃가루·폭죽). 테스트 통과 보상.
- **플래시카드 컴포넌트** — `CardFlipster`(플립+프로그레스+통계 세트), `SwipeCardsKit`/`Shuffle`(틴더식 스와이프).
- **아이콘 팩(SF Symbols 보완)** — **Lucide**, **Phosphor**(6 weight: thin~fill/duotone), **FontAwesome Free**(브랜드 로고), **Heroicons**. SPM 또는 폰트/SVG 임포트.
- **달력/차트** — `FSCalendar`(UIKit), 커뮤니티 SwiftUI 차트.

## 3. 일러스트/3D 에셋 (빈 화면·온보딩·스플래시)
- **unDraw** — 메인 컬러 지정 → 톤 맞춘 SVG/PNG. CC0급 자유.
- **Storyset** — 스타일(Rafiki/Bro/Amico) 선택, 레이어 숨김 커스터마이즈, 웹 애니메이션.
- **Open Peeps / Humaaans / DrawKit** — 인물/장면 일러스트.
- **3D Icons(Business 3D 등)** — 말랑한 CC0 3D 아이콘(배너·포인트 UI).
- ⚠️ SVG 번들 시 래스터화 도구(rsvg/cairosvg/Inkscape) 필요. 없으면 **SwiftUI 네이티브 벡터로 동일 톤 재현**.

## 4. 타이포/컬러
- **Google Fonts** — 한글 **Pretendard**(권장)/Noto Sans KR/SUIT, 영문 Inter·Manrope. (라이선스 OFL 확인, 폰트 파일 번들 + Info.plist 등록)
- **컬러 영감** — Coolors, Radix Colors, Apple HIG 컬러.

## 5. 카테고리별 추천 조합
- **단어장/학습 앱**: SF Symbols + Swift Charts(진척 링) + AVSpeechSynthesizer(발음) + 네이티브 플립/스와이프 플래시카드 + 컨페티(완료 보상) + unDraw/Storyset(빈 화면). TTS·플래시카드·진척 대시보드가 "출시 제품" 체감의 핵심.
- **대시보드/관리**: Swift Charts + 풍부한 List/Form + 머티리얼.
- **온보딩 무드**: Lottie/Storyset + 그라디언트 + symbol effects.

## 참고
- Awesome-SwiftUI(GitHub)에서 카테고리별 검증된 컴포넌트 탐색.
- 의존성 추가 전 `git ls-remote <repo>`로 resolve 가능 여부와 최신 태그 확인.
