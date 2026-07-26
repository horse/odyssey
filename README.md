# Odyssey Translation Repository

本仓库保存《奥德赛》三语新译的全部生产资料：古希腊文底本、待办状态、Project 指令、翻译中间版本、审核记录与最终译文。

## 核心原则

- **GitHub 是唯一正式记录。**
- **ChatGPT Project 是工作环境。**
- 英语、日语、台湾繁体中文分别在三个独立 Project 中工作。
- 每次从 GitHub 取出当前源文和规则文件，手动上传到对应 Project。
- Project 产生的每个中间版本都保存回 GitHub。
- 三种目标语言互不作为彼此的翻译底本。

## 仓库结构

```text
source/                         清理、校验、分片后的古希腊文
project/                        手动上传到 ChatGPT Project 的规则文件
translation/                    三语翻译过程与状态
  STATUS.tsv                    72个片段的三语进度
  TEMPLATES.md                  五阶段结果文件格式
  en/                           英语翻译
  ja/                           日语翻译
  zh-hant-tw/                   台湾繁体中文翻译
```

## 每个片段的五个版本

一个片段的所有结果放在同一目录，例如：

```text
translation/en/book-01/ODY-B01-S01/
├── 01_draft.md
├── 02_review.md
├── 03_revised.md
├── 04_final_review.md
└── 05_final.md
```

五个文件全部保留：

1. `01_draft.md`：GPT-5.5 快速初译。
2. `02_review.md`：GPT-5.6 Sol High 对照希腊文审核。
3. `03_revised.md`：GPT-5.5 根据审核意见修订。即使无需修改，也保存一份并注明无改动。
4. `04_final_review.md`：GPT-5.6 Sol High 最终验收。
5. `05_final.md`：通过验收后的正式锁定译文。

Git 历史负责记录文件后续修改，因此不再建立 `final-final-v2` 一类文件。

## 开始一个翻译任务

以英语 `ODY-B01-S01` 为例，从仓库取出并上传到英语 Project：

```text
project/COMMON_RULES.md
project/en/PROJECT_INSTRUCTIONS.md
translation/en/DECISIONS.md
translation/en/CONTINUITY.md
source/segments/ODY-B01-S01_SOURCE.md
```

在 Project 中依次执行：

```text
/draft ODY-B01-S01
/review ODY-B01-S01
/revise ODY-B01-S01
/final-review ODY-B01-S01
/finalize ODY-B01-S01
```

每一步输出都按 `translation/TEMPLATES.md` 保存到相应 GitHub 路径，并同步更新 `translation/STATUS.tsv`。

## 语言 Project

- 英语：`project/en/PROJECT_INSTRUCTIONS.md`
- 日语：`project/ja/PROJECT_INSTRUCTIONS.md`
- 台湾繁体中文：`project/zh-hant-tw/PROJECT_INSTRUCTIONS.md`
- 三语共同规则：`project/COMMON_RULES.md`

## 古希腊文底本

- `source/segments/`：72个可直接翻译的分片
- `source/books/`：24卷连续阅读版
- `source/lines/`：保留卷号与诗行号的逐行版
- `source/manifest.tsv`：分片范围、字符数与补丁标记
- `source/SOURCE_PATCHES.md`：五处数字底本修复记录
- `source/original/`：未经修改的 Perseus XML

生产底本为 PerseusDL `tlg0012.tlg002.perseus-grc2`，固定 Git blob SHA：

```text
f38f5f238d665eafb9c6878b11283822ed418a07
```

清理后的生产文本通过24卷、12,110行、连续行号与源文修复测试。