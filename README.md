# kali-claude-plugin-hub

Claude Code용 **플러그인 마켓플레이스** + 설정 가이드 사이트.

## 마켓플레이스 추가
```
/plugin marketplace add withkali/kali-claude-plugin-hub
```

## 플러그인
| 플러그인 | 설명 | 설치 |
|---|---|---|
| **virtual-team** | 22개 역할 서브에이전트로 서비스를 기획→개발→(운영)까지 자동화하는 가상 개발팀 (+ 시크릿 차단 훅, 오케스트레이션 명령) | `/plugin install virtual-team@kali-claude-plugin-hub` |

## 문서 (GitHub Pages)
https://withkali.github.io/kali-claude-plugin-hub/

- [virtual-team 가이드](https://withkali.github.io/kali-claude-plugin-hub/virtual-team.html)

## 구조
```
.claude-plugin/marketplace.json   # 마켓플레이스 매니페스트 (플러그인 목록)
plugins/
  virtual-team/                   # 플러그인 (agents, commands, hooks, MANUAL.md)
docs/                             # GitHub Pages 사이트 (index.html, virtual-team.html)
```

## 새 플러그인 추가하기
1. `plugins/<name>/` 에 플러그인 작성 (`.claude-plugin/plugin.json` + agents/commands/skills/hooks).
2. `.claude-plugin/marketplace.json` 의 `plugins` 배열에 항목 추가 (`source: ./plugins/<name>`).
3. `docs/` 에 카드/가이드 추가 후 커밋·push.
