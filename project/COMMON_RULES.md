# Common Project Rules

本文件由英语、日语、台湾繁体中文三个 ChatGPT Project 共用。

## 版本目标

制作完整、当代、故事本位的散文新译：

- 符合当代一般读者的阅读习惯；
- 适度保留古典距离，但不使用伪古语；
- 不追求格律、诗行、套语或术语的机械复现；
- 追求全书内部一致、叙事清楚和相对紧凑；
- 使用约1990—2000年代主流报刊与一般书籍的成熟书面语；
- 原作有偏见时保留偏见，原作中立时不得擅自增加评价；
- 不夸张、不婉饰、不替人物辩护或定罪。

## 权威输入

每次只使用：

1. 当前 `source/segments/ODY-..._SOURCE.md`；
2. 本文件；
3. 当前语言的 `PROJECT_INSTRUCTIONS.md`；
4. 当前语言的 `DECISIONS.md`；
5. 当前语言的 `CONTINUITY.md`；
6. 用户在当前任务中明确提供的已批准材料。

不得把另一个目标语言的译文作为输入。不得模仿记忆中的现代译本。

## 忠实度顺序

1. 事件、动作、物件和结果；
2. 行动主体、命令者、执行者和承受者；
3. 人物知道什么、不知道什么；
4. 事实、谎言、传闻、记忆、预言和推测的区别；
5. 原文的褒贬、暴力、情绪和确定程度；
6. 原文含混性；
7. 全书内部一致；
8. 当代目标语言的自然可读性。

## 禁止事项

不得添加原文没有的：

- 心理解释、动机或象征；
- 羞耻、创伤、爱情互惠、同意或强迫；
- 悬疑、高潮、煽情或影视化节奏；
- 道德评论、现代权利语言或现代法律概念；
- 更强的侮辱、赞美、暴力或确定性。

不得淡化原文中的暴力、阶级、奴隶制、父权关系、神的介入或古代偏见。

## 五阶段工作流

### 1. `/draft SEGMENT_ID`

模型：GPT-5.5。

根据当前希腊文片段生成完整初译。只输出 `01_draft.md` 的文件内容，不解释过程。

### 2. `/review SEGMENT_ID`

模型：GPT-5.6 Sol High。必须在独立审核聊天中执行。

对照希腊文和初稿，只输出 `02_review.md`。审核问题分为：

- `FACT`
- `AGENCY`
- `INFORMATION`
- `VALUE`
- `AMBIGUITY`
- `OMISSION`
- `ADDITION`
- `STYLE`
- `CONTINUITY`

审核阶段不重写全文。

### 3. `/revise SEGMENT_ID`

模型：GPT-5.5。

根据已确认的审核意见生成 `03_revised.md`。未被审核指出的内容尽量保持不动。若审核为直接通过，仍输出完整文件，并在元数据中写 `revision_note: no_changes_required`。

### 4. `/final-review SEGMENT_ID`

模型：GPT-5.6 Sol High。

对修订稿进行最终验收，输出 `04_final_review.md`。结果只能为：

- `PASS`
- `PASS_WITH_MINOR_FIXES`
- `FAIL`

### 5. `/finalize SEGMENT_ID`

只有最终审核为 `PASS` 后执行。输出 `05_final.md`，不得再作未经审核的文学润色。

## GitHub路径

每个片段固定为：

```text
translation/<language>/book-XX/<SEGMENT_ID>/01_draft.md
translation/<language>/book-XX/<SEGMENT_ID>/02_review.md
translation/<language>/book-XX/<SEGMENT_ID>/03_revised.md
translation/<language>/book-XX/<SEGMENT_ID>/04_final_review.md
translation/<language>/book-XX/<SEGMENT_ID>/05_final.md
```

语言目录：

- `en`
- `ja`
- `zh-hant-tw`

## 状态更新

每保存一步，更新 `translation/STATUS.tsv` 中对应语言的状态：

```text
SOURCE_READY
DRAFTED
REVIEWED
REVISED
FINAL_REVIEWED
FINAL
```

## 决定与连续性

- 新的永久译名、称谓或语义决定，写入该语言的 `DECISIONS.md`。
- 影响人物知识、事件重复、虚构身世、物件或前后呼应的事项，写入 `CONTINUITY.md`。
- Project中的聊天记忆不是正式记录；只有GitHub文件是正式记录。