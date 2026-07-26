# Translation File Templates

所有文件使用UTF-8 Markdown。日期使用 `YYYY-MM-DD`。

## `01_draft.md`

```markdown
---
segment_id: ODY-B01-S01
language: en
stage: DRAFTED
source: source/segments/ODY-B01-S01_SOURCE.md
model: GPT-5.5
harness: project/COMMON_RULES.md
created: YYYY-MM-DD
---

# Translation

[完整初译]

# Proposed Decisions

- None.
```

## `02_review.md`

```markdown
---
segment_id: ODY-B01-S01
language: en
stage: REVIEWED
source: source/segments/ODY-B01-S01_SOURCE.md
reviewed_file: 01_draft.md
model: GPT-5.6-Sol-High
created: YYYY-MM-DD
result: PASS | REVISION_REQUIRED
---

# Review Summary

[简要结论]

# Issues

## ISSUE-01

- severity: CRITICAL | MAJOR | MINOR
- category: FACT | AGENCY | INFORMATION | VALUE | AMBIGUITY | OMISSION | ADDITION | STYLE | CONTINUITY
- greek_lines: 1.1–1.3
- target_passage: [相关译文]
- finding: [问题]
- required_change: [需要怎样修改]
- human_decision_required: yes | no

# Decisions to Record

- None.
```

## `03_revised.md`

```markdown
---
segment_id: ODY-B01-S01
language: en
stage: REVISED
source: source/segments/ODY-B01-S01_SOURCE.md
based_on: 01_draft.md
review: 02_review.md
model: GPT-5.5
created: YYYY-MM-DD
revision_note: changes_applied | no_changes_required
---

# Translation

[完整修订稿]

# Issue Resolution

- ISSUE-01: resolved — [简短说明]

# Proposed Decisions

- None.
```

## `04_final_review.md`

```markdown
---
segment_id: ODY-B01-S01
language: en
stage: FINAL_REVIEWED
source: source/segments/ODY-B01-S01_SOURCE.md
reviewed_file: 03_revised.md
model: GPT-5.6-Sol-High
created: YYYY-MM-DD
result: PASS | PASS_WITH_MINOR_FIXES | FAIL
---

# Final Review

[最终结论]

# Remaining Issues

- None.

# Acceptance Condition

- Approved for `05_final.md`.
```

## `05_final.md`

```markdown
---
segment_id: ODY-B01-S01
language: en
stage: FINAL
source: source/segments/ODY-B01-S01_SOURCE.md
based_on: 03_revised.md
final_review: 04_final_review.md
created: YYYY-MM-DD
version: 1.0
---

# Translation

[通过验收的完整正式译文]
```

## 规则

- 五个文件都保留，不互相覆盖。
- `05_final.md` 只能在 `04_final_review.md` 为 `PASS` 后生成。
- 若最终审核要求小修，先更新 `03_revised.md`，再重新生成 `04_final_review.md`；不要直接在 `05_final.md` 中修。
- 后续发现实质错误时，修改相关阶段文件并通过Git提交历史记录，不创建随意命名的新文件。