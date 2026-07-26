# AGENTS.md

This repository is the complete working record for a three-language translation of Homer’s *Odyssey*.

## What this repository contains

- `source/` — locked, cleaned and segmented Ancient Greek source.
- `project/` — all files that must be uploaded manually to the three ChatGPT Projects.
- `translation/` — workflow state, templates, intermediate versions, final versions, language decisions and continuity records.

## Read in this order

1. `README.md`
2. `project/README.md`
3. `project/COMMON_RULES.md`
4. the target language file:
   - `project/en/PROJECT_INSTRUCTIONS.md`
   - `project/ja/PROJECT_INSTRUCTIONS.md`
   - `project/zh-hant-tw/PROJECT_INSTRUCTIONS.md`
5. the target language records:
   - `translation/<language>/DECISIONS.md`
   - `translation/<language>/CONTINUITY.md`
6. `translation/STATUS.tsv`
7. the requested Greek segment in `source/segments/`

## Core workflow

Every segment passes through five persisted files:

```text
01_draft.md
02_review.md
03_revised.md
04_final_review.md
05_final.md
```

Repository path:

```text
translation/<language>/book-XX/<SEGMENT_ID>/
```

Stages:

```text
SOURCE_READY
DRAFTED
REVIEWED
REVISED
FINAL_REVIEWED
FINAL
```

## Model roles

- GPT-5.5: `/draft`, `/revise`, `/finalize`
- GPT-5.6 Sol High: `/review`, `/final-review`

Translation and review must be performed in separate chats.

## Authority rules

- GitHub files are the official record.
- ChatGPT Project files are working copies.
- Do not use one target-language translation as the source for another language.
- Translate only from the Greek segment plus the uploaded rules and approved language records.
- Preserve source facts, agency, information state, value intensity and ambiguity.
- Do not add psychology, moral judgment, dramatic amplification or modern ideological correction.

## ChatGPT Project upload files

### English

```text
project/COMMON_RULES.md
project/en/PROJECT_INSTRUCTIONS.md
translation/en/DECISIONS.md
translation/en/CONTINUITY.md
source/segments/<CURRENT_SEGMENT>_SOURCE.md
```

### Japanese

```text
project/COMMON_RULES.md
project/ja/PROJECT_INSTRUCTIONS.md
translation/ja/DECISIONS.md
translation/ja/CONTINUITY.md
source/segments/<CURRENT_SEGMENT>_SOURCE.md
```

### Traditional Chinese (Taiwan)

```text
project/COMMON_RULES.md
project/zh-hant-tw/PROJECT_INSTRUCTIONS.md
translation/zh-hant-tw/DECISIONS.md
translation/zh-hant-tw/CONTINUITY.md
source/segments/<CURRENT_SEGMENT>_SOURCE.md
```

## Before doing any work

Check `translation/STATUS.tsv` and continue from the recorded stage. Never overwrite or skip an intermediate stage. If a permanent decision is made, update `DECISIONS.md`; if it affects cross-segment knowledge, identity, chronology or repeated events, update `CONTINUITY.md`.
