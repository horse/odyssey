# ChatGPT Project Setup

建立三个彼此独立的 ChatGPT Project：

```text
Odyssey — English
Odyssey — Japanese
Odyssey — Traditional Chinese (Taiwan)
```

建议新建时选择 Project-only memory。

## 英语 Project

长期上传：

```text
project/COMMON_RULES.md
project/en/PROJECT_INSTRUCTIONS.md
translation/en/DECISIONS.md
translation/en/CONTINUITY.md
```

每次任务再上传一个源文，例如：

```text
source/segments/ODY-B01-S01_SOURCE.md
```

## 日语 Project

长期上传：

```text
project/COMMON_RULES.md
project/ja/PROJECT_INSTRUCTIONS.md
translation/ja/DECISIONS.md
translation/ja/CONTINUITY.md
```

每次任务再上传当前源文片段。

## 台湾繁体中文 Project

长期上传：

```text
project/COMMON_RULES.md
project/zh-hant-tw/PROJECT_INSTRUCTIONS.md
translation/zh-hant-tw/DECISIONS.md
translation/zh-hant-tw/CONTINUITY.md
```

每次任务再上传当前源文片段。

## 文件同步规则

- GitHub中的文件是正式版本。
- Project内文件只是一份工作副本。
- GitHub中的 `DECISIONS.md` 或 `CONTINUITY.md` 更新后，重新上传替换Project旧文件。
- 一个片段完成后，可以从Project删除该源文，再上传下一片。
- 不要把另一个语言的译稿上传到当前语言Project。

## 建议聊天结构

每种语言可以长期保留两个聊天：

```text
Translation
Review
```

- `Translation`：GPT-5.5执行 `/draft`、`/revise`、`/finalize`。
- `Review`：GPT-5.6 Sol High执行 `/review`、`/final-review`。

审核聊天不要包含初译时的解释过程，只提供源文和待审核文件。