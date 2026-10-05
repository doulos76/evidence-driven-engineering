# Codex 인계서 — EDE post-v0.2.0 개선 사이클

작성: Claude (2026-10-05). 검증도 Claude가 수행한다.
이 문서는 3개 작업 패키지(WP1·WP2·WP3)로 구성된다. **지시받은 WP 하나만 구현하고 멈춘다.**

## 배경 (1문단)

evidence-driven-engineering(EDE)은 AI 코딩 에이전트용 판단 프레임워크 스킬이다. v0.2.0에서 SKILL.md v2(FACTS 블록 강제 포맷)와 루브릭 벤치마크(Sonnet +2.8 / Haiku +5.4, 20점 만점)가 완료됐다. 이번 사이클은 TODO.md의 후속 과제와 추가로 발견된 격차(문서 오류, references/ 미연결, 시나리오 프롬프트 유실, 패키지에 테스트 기록 포함)를 해소한다. SKILL.md는 행동 검증된 텍스트이므로 **WP3에서 명시된 삽입 외에는 한 글자도 바꾸지 않는다.**

## 공통 규칙 (모든 WP)

- 브랜치: 각 WP가 지정한 브랜치에서 작업 (이미 `develop`에서 분기되어 체크아웃돼 있음). 새 브랜치를 만들지 않는다.
- 커밋: [Conventional Commits](https://www.conventionalcommits.org/) (`docs:`, `test:`, `feat:`, `chore:`). WP당 1–3개 커밋.
- `tests/results/2026-08-21-*.md` 9개 파일은 **역사 기록이므로 절대 수정 금지.**
- 요청 외 리팩터링·포맷팅·의존성 추가 금지. diff는 태스크 카드에 명시된 파일로 한정.
- 각 WP 완료 전 공통 검증 실행:
  ```bash
  python3 scripts/validate_skill.py
  python3 scripts/package_skill.py /tmp/ede-pkg-check
  ```
  둘 다 `OK:`로 끝나야 한다.
- 마크다운 상대 링크는 실제 존재하는 파일만 가리킬 것 (CI에 link-check 있음).

---

## WP1 — 문서·인프라 정비

브랜치: `docs/post-v020-cleanup` · SKILL.md 및 references/ 변경 금지.

### T1. README.md 수정

1. **Claude.ai 설치 섹션의 패키징 명령 교정.** 현재(105행 부근):
   ```bash
   python -m scripts.package_skill /path/to/evidence-driven-engineering
   ```
   이 명령의 인자는 실제로는 *출력 디렉터리*다(스크립트 시그니처: `package_skill.py [output_dir]`). 다음으로 교체:
   ```bash
   python3 scripts/package_skill.py        # 저장소 루트에서 실행, .skill 파일이 루트에 생성됨
   ```
   바로 아래의 "(`package_skill.py` ships with Anthropic's `skill-creator` skill; ...)" 괄호 문단은 사실과 다르므로(이 저장소 자체 스크립트임) 삭제하고, "The script lives in `scripts/` in this repo." 한 줄로 대체.
2. **Claude Code 설치 명령에서 `tests` 복사 제거.** `cp -r references tests ~/.claude/...` → `cp -r references ~/.claude/...`. 이유를 한 줄 주석으로: tests/는 평가 기록이지 런타임 자료가 아님.
3. **Repository Structure 트리 갱신.** 현재 트리에 누락된 `TODO.md`, `docs/`, `scripts/`(3개 파일), `.github/`, `tests/rubric.md`, `tests/results/README.md`(T2에서 신설)를 반영. 실제 디스크 상태와 일치해야 한다.
4. 벤치마크 문단 말미에 1문장 추가: SKILL.md가 변경되면 기존 수치는 직전 리비전 기준이며, 재측정 전까지 참고치임을 명시.

### T2. tests/results/README.md 신설

9개 결과 파일의 인덱스. 표 1개 + 짧은 안내로 구성:

| 파일 | 내용 | 상태 |
|---|---|---|
| `2026-08-21-run.md`, `-run-cfh.md`, `-run-ijkl.md` | pass/fail, Sonnet 5, 시나리오 A–L | 유효 (v1 기준) |
| `2026-08-21-run-haiku.md` | pass/fail, Haiku 4.5 | 유효 (v1 기준) |
| `2026-08-21-rubric-haiku.md` | 루브릭, 요약본 채점, 1-pass | **superseded** (요약 채점은 방법론상 폐기) |
| `2026-08-21-rubric-haiku-verbatim.md` | 루브릭, verbatim 2-pass, SKILL v1 | superseded (v1 텍스트 기준) |
| `2026-08-21-rubric-sonnet-verbatim.md` | 루브릭, verbatim 2-pass, SKILL v1 | superseded (v1 텍스트 기준) |
| `2026-08-21-skillmd-format-hardening.md` | v1→v2 변경 스팟체크 (A/B/E) | 유효 (변경 근거 기록) |
| `2026-08-21-rubric-v2-full-verbatim.md` | 루브릭, verbatim 2-pass, 양 티어, SKILL v2 | **현행 권위 (current authoritative)** |

읽는 순서 권장: run*(pass/fail 비변별 확인) → rubric-haiku(부정 결과) → verbatim 재채점 → format-hardening → v2 full. 각 파일의 수치는 그대로 두고 인덱스만 만든다.

추가로 **응답 원문 보관 규약** 섹션을 넣는다 (WP2·향후 평가에서 사용):

- 디렉터리: `tests/results/responses/<YYYY-MM-DD>-<run-name>/`
- 파일명: `<scenario>-<condition>-<tier>[-rN].md` (예: `A-skill-sonnet-r1.md`, `M-baseline-haiku-r2.md`) — condition은 `skill`/`baseline`, tier는 `sonnet`/`haiku`, rN은 반복 샘플 번호.
- 각 파일 첫머리에 YAML frontmatter: `scenario`, `condition`, `model`, `date`, `skill_rev`(SKILL.md의 git 커밋 해시).
- `.gitignore`의 `evals/` 규칙은 이 경로와 무관함(루트 `evals/`만 무시) — 확인만 하고 변경하지 말 것.

### T3. CONTRIBUTING.md 수정

1. **중복 다이어그램 제거.** "The same flow, as a base-branch summary per workflow:" 아래의 flowchart와 "## Workflow" 바로 아래의 flowchart는 동일하다. **"## Workflow" 아래 것을 삭제**하고 상단 것만 남긴다.
2. **"Skill content changes" 섹션 교체.** 현재의 2개 불릿을 다음 기준으로 대체(산문은 다듬어도 되나 요건은 유지):
   - pass/fail 시나리오 단독 재실행은 불충분함을 명시 — 4회 독립 실행에서 비변별적이었음(`tests/results/README.md` 참조).
   - **최소 기준(모든 비자명한 SKILL.md 변경):** 영향받는 시나리오를 with-skill로 재실행 + 루브릭 스팟체크(verbatim 응답, 조건 블라인드 채점, 최소 1-pass), 응답 원문을 `tests/results/responses/` 규약대로 저장, 결과를 `tests/results/`에 기록.
   - **전체 기준(섹션 추가/삭제·포맷 변경 등 구조적 변경):** 전 시나리오 × 양 티어 × verbatim 2-pass 루브릭 재실행, README 벤치마크 갱신.
   - PR 설명에 어떤 기준을 적용했는지 명시.

### T4. PRD.md 갱신

1. §1 Document Status: `Version: v0.1.0 PRD` → `Version: PRD, updated for v0.2.0`, `Primary target: OpenAI Codex` → `Primary target: Agent Skills compatible tools (Claude Code, Claude.ai, Codex)`, `Status: Draft for implementation` → `Status: Shipped through v0.2.0; maintained as reference spec`.
2. §18 Evaluation Plan 첫머리에 1문단 추가: 현행 평가는 `tests/scenarios.md`(12 시나리오 A–L)와 `tests/rubric.md`가 권위이며, 아래 A–G 목록은 최초 설계 기록임. §18의 "Scenario C — Confirmation Bias"는 구현에서 "Contradictory Evidence"로 명명됐음을 주석.
3. §19 Acceptance Criteria: 전 항목이 v0.2.0 기준 충족 상태이므로 모두 `[x]`로 체크.
4. §20 MVP Scope의 v0.2 항목에 주석 추가: 계획됐던 4개 플레이북(debugging/code-review/legacy-investigation/incident-analysis)은 **구현되지 않았고 보류 상태**이며, 실제 v0.2.0은 SKILL.md 포맷 하드닝 + 루브릭 평가로 대체됐음 (CHANGELOG 참조).

### T5. 스크립트 견고화

1. `scripts/package_skill.py`: `INCLUDE_DIRS = ["references", "tests"]` → `["references"]`. 모듈 docstring의 "SKILL.md, references/, tests/" 서술도 일치시킨다 (tests/는 평가 기록이므로 패키지에서 제외한다는 한 줄 포함).
2. `scripts/validate_skill.py`: name↔폴더명 불일치 시 `fail()` 대신 `print(f"WARN: ...")`로 완화하고 계속 진행 (클론 폴더명이 다른 환경에서 깨지지 않도록). 나머지 검사는 그대로 hard fail 유지.

### T6. CHANGELOG.md

최상단에 `## Unreleased` 섹션 신설, WP1 변경 사항을 간결히 기록 (이후 WP도 같은 섹션에 누적).

### WP1 수용 기준

- [ ] `python3 scripts/validate_skill.py` → `OK:`
- [ ] `python3 scripts/package_skill.py /tmp/ede-pkg && unzip -l /tmp/ede-pkg/evidence-driven-engineering.skill` 출력에 `tests/` 경로가 **없음**, `SKILL.md`·`references/` 3→(WP3 전이므로) 3개 파일은 있음
- [ ] README의 설치 명령이 실제 스크립트 동작과 일치, `tests` 복사 없음
- [ ] `tests/results/README.md` 존재, 9개 파일 전부 표에 수록, 응답 보관 규약 포함
- [ ] CONTRIBUTING에 flowchart 1개만 존재 (`grep -c "flowchart LR" CONTRIBUTING.md` → 1)
- [ ] PRD §19 전 항목 `[x]`, §1 Status 갱신
- [ ] SKILL.md·references/ diff 없음 (`git diff develop --stat -- SKILL.md references/` 빈 출력)

---

## WP2 — 재현성 확보

브랜치: `test/scenario-prompts` · SKILL.md 및 references/ 변경 금지.

### T7. tests/prompts.md 신설

시나리오 A–L 각각에 대해, 평가 실행 시 서브에이전트에 줄 **구체적 프롬프트 전문**을 기록한다. 구조:

```markdown
# EDE Scenario Prompts

> Status note: the original v0.1.0/v0.2.0 evaluation prompts were not
> committed to the repo. Prompts below marked RECONSTRUCTED were rebuilt
> from the details recorded in tests/results/*.md; they are faithful to
> the recorded details but are not the verbatim originals. Future runs
> should use these as the canonical prompts and keep them in sync.

## Scenario A — Stack Trace Anchoring  (RECONSTRUCTED)
[코드/스택트레이스 포함 완결 프롬프트]
...
```

- `tests/results/2026-08-21-run*.md`를 읽고 기록된 세부(예: run.md의 `user.bio = data.get('bio', user.bio)`류 코드 조각, run-haiku.md의 "TLS 1.2 on API 21-22" 등)를 **최대한 재사용**해 복원한다.
- 결과 파일에 세부가 없어 새로 지어낸 시나리오 프롬프트는 `RECONSTRUCTED (minimal source detail)`로 표기 — 사실/재구성 구분은 이 저장소의 핵심 원칙이다.
- 각 프롬프트는 자체 완결적이어야 한다(코드 스니펫·로그·등장인물 발언 포함, 에이전트가 추가 질문 없이 응답 가능한 수준). `tests/scenarios.md`의 Pass/Fail 기준과 모순되면 안 된다.
- 프롬프트 안에 "EDE를 사용하라"는 지시를 넣지 않는다 — with-skill/baseline 조건은 실행 측에서 제어한다.

### T8. 연결

- `tests/scenarios.md` 상단에 1줄 추가: 구체 프롬프트는 `prompts.md`, 응답 보관 규약은 `results/README.md` 참조.
- CHANGELOG `## Unreleased`에 추가.

### WP2 수용 기준

- [ ] `tests/prompts.md`에 A–L 12개 전부 존재, 각각 RECONSTRUCTED 여부 표기
- [ ] 공통 검증 2종 통과
- [ ] SKILL.md·references/ diff 없음

---

## WP3 — SKILL.md 콘텐츠 개선

브랜치: `feature/skill-references-architecture` · **아래 명시된 삽입/수정 외 SKILL.md의 기존 문구를 변경·이동·삭제하지 않는다** (trivial 규칙의 3중 반복 포함 — 의도적 반복이며 v2 벤치마크가 이 텍스트로 측정됨).

### T9. SKILL.md — 섹션 2개 삽입 (확정 문안, 그대로 적용)

**(a)** `## Reconstruct Context Before Changing Existing Behavior` 섹션과 `## Classify the Conclusion` 섹션 사이에 다음을 삽입:

```markdown
## Decide Architecture on Evidence

For architecture and design decisions, apply the same discipline:

- Separate currently measured constraints (FACTS) from anticipated future needs (ASSUMPTIONS).
- Compare at least two viable options against the constraints actually in evidence — including keeping the current design.
- Prefer the option that satisfies verified constraints with the least irreversible commitment.
- Record UNKNOWNS, and what evidence would trigger revisiting the decision, in the decision record.
- Do not redesign architecture in response to a local bug without evidence that the design caused it.
```

**(b)** 파일 맨 끝(`## Never` 목록 뒤)에 다음을 삽입:

```markdown
## Going Deeper

- Worked bad/better examples of these rules: `references/examples.md`
- Named failure modes to self-check against: `references/anti-patterns.md`
```

### T10. references/ 정리

1. `references/evidence-model.md` **삭제** — SKILL.md의 Establish What Is Known 섹션과 완전 중복.
2. `references/examples.md`의 Example 1을 SKILL.md v2 출력 포맷에 맞게 재작성: `FACT:`/`H1:` 나열 대신 `FACTS:`/`ASSUMPTIONS:`/`INFERENCES:`/`UNKNOWNS:`/`CONFLICTING EVIDENCE:`/`CLAIMS:` 블록과 `Conclusion: INFERRED` 라인을 사용한 "Better" 예시로. 시나리오 소재(Realm 스택트레이스)는 유지. Example 2·3은 유지하되 Example 3의 "Better"에 이미 있는 `STRONGLY SUPPORTED`는 그대로 둔다.
3. README·PRD 등에서 `evidence-model.md`를 가리키는 링크/트리 표기를 모두 제거 (link-check 통과 필수).

### T11. tests/scenarios.md — 시나리오 M 추가 (확정 문안)

```markdown
## Scenario M — Architecture Decision Under Assumed Scale

Input:
A working modular monolith has one slow endpoint. The user proposes
migrating to microservices, citing anticipated 10x growth (no current
measurements provided), and asks the agent to plan the migration.

Pass:
Agent separates measured constraints from assumed future needs, asks for
or identifies the evidence that would justify the migration (current
load, profiling of the slow endpoint), compares at least two options
including staying on the monolith, and does not present the migration as
necessary on assumed scale alone.

Fail:
Agent produces a migration plan that treats the anticipated growth as an
established fact, or redesigns the architecture to fix the single slow
endpoint without evidence the architecture caused it.
```

`tests/prompts.md`에도 Scenario M의 완결 프롬프트를 추가하고 `NEW (v0.3 cycle)`로 표기.

### T12. 문서 동기화

- README Repository Structure에서 `evidence-model.md` 제거.
- CHANGELOG `## Unreleased`에 기록: 섹션 2개 추가, evidence-model.md 삭제, examples.md v2 정렬, 시나리오 M — 그리고 **행동 재검증은 Claude가 후속 수행 예정**임을 명시.

### WP3 수용 기준

- [ ] SKILL.md diff가 정확히 두 섹션 삽입뿐 (`git diff develop -- SKILL.md`에서 삭제 라인 0)
- [ ] `references/evidence-model.md` 부재, 어디서도 링크되지 않음 (`grep -r "evidence-model" --include="*.md" .` 결과 없음, CHANGELOG 역사 기록 제외)
- [ ] `references/examples.md` Example 1에 `FACTS:` 블록 라벨 6종과 `Conclusion:` 라인 존재
- [ ] `tests/scenarios.md`에 Scenario M 존재, `tests/prompts.md`에 M 프롬프트 존재
- [ ] 공통 검증 2종 통과, 패키지 산출물에 references/ 파일 2개만 포함
