# Odyssey Greek Translation Source

This repository is configured to generate a cleaned and segmented Ancient Greek text of Homer’s *Odyssey* for direct use in ChatGPT Projects.

## Build status

The cleaner and GitHub Actions workflow are installed. The generated `source/` directory will appear after the workflow is allowed to run once.

## One-time GitHub setup

1. Open **Settings → Actions → General**.
2. Under **Actions permissions**, allow GitHub Actions.
3. Under **Workflow permissions**, select **Read and write permissions**.
4. Open **Actions → Build cleaned Odyssey Greek source**.
5. Click **Run workflow → Run workflow**.

The workflow downloads the locked Perseus source, verifies its Git blob SHA, validates 24 books and 12,110 lines, cleans the XML, segments the Greek, and commits the generated files back to this repository.

## Generated structure

- `source/books/` — 24 cleaned book files
- `source/lines/` — line-preserving TSV files
- `source/segments/` — upload-ready translation segments
- `source/manifest.tsv` — exact segment boundaries and character counts
- `source/source_build.json` — validation and reproducibility record
- `source/original/` — untouched source XML

## Production source

- PerseusDL `tlg0012.tlg002.perseus-grc2`
- A. T. Murray, 1919
- Expected Git blob SHA: `f38f5f238d665eafb9c6878b11283822ed418a07`

## Segmentation

- target: about 6,200 Greek characters, excluding whitespace
- normal range: 3,500–8,200 characters
- speeches and paragraph units are preserved where possible
- no segment crosses a book boundary

For translation, upload only the current book’s files from `source/segments/` into the relevant ChatGPT Project.
