# Translation Workspace

本目录保存英语、日语、台湾繁体中文三种译本的全部中间版本和正式结果。

## 语言目录

```text
en/
ja/
zh-hant-tw/
```

## 固定目录结构

每个片段按照以下结构保存：

```text
translation/<language>/book-XX/<SEGMENT_ID>/
├── 01_draft.md
├── 02_review.md
├── 03_revised.md
├── 04_final_review.md
└── 05_final.md
```

例如：

```text
translation/ja/book-01/ODY-B01-S01/03_revised.md
```

## 为什么保存全部中间版本

- 可以检查GPT-5.5初译与GPT-5.6审核之间发生了什么；
- 可以发现审核是否引入新的问题；
- 可以比较不同模型或不同规则版本；
- 可以从任何阶段恢复；
- Git提交历史与五个固定文件共同构成完整审计记录。

## 文件关系

```text
source/segments/ODY-Bxx-Sxx_SOURCE.md
                 ↓
01_draft.md
                 ↓
02_review.md
                 ↓
03_revised.md
                 ↓
04_final_review.md
                 ↓
05_final.md
```

每个文件必须在元数据中指向前一阶段文件和源文路径。

## 状态表

`STATUS.tsv` 是全书三语工作队列。

允许的状态：

```text
SOURCE_READY
DRAFTED
REVIEWED
REVISED
FINAL_REVIEWED
FINAL
```

每次将一个阶段文件推送到GitHub后，立即更新对应状态。

## 决定与连续性

每种语言保留两个累计文件：

```text
translation/<language>/DECISIONS.md
translation/<language>/CONTINUITY.md
```

`DECISIONS.md` 保存永久译名、称谓、语言选择和语义决定。

`CONTINUITY.md` 保存人物知识状态、虚构身世、重复事件、重要物件、前后照应和跨片段问题。

它们更新后要重新上传到对应ChatGPT Project。