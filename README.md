# Odyssey Greek Translation Source

This repository generates and stores a cleaned, validated and segmented Ancient Greek text of Homer’s *Odyssey* for direct use in ChatGPT Projects.

## Ready-to-translate files

After the automated build on `main`, use:

- `source/segments/` — upload-ready translation segments
- `source/books/` — 24 cleaned continuous-reading files
- `source/lines/` — line-preserving TSV files
- `source/manifest.tsv` — segment boundaries, sizes and patch references
- `source/SOURCE_PATCHES.md` — transparent record of five source repairs
- `source/source_build.json` — source hash and validation record
- `source/original/` — untouched downloaded Perseus XML

For translation, upload only one book at a time from `source/segments/` into the relevant ChatGPT Project. For example, upload every `ODY-B01-*` file for Book 1.

## Validation

The build must pass all of the following gates:

- source Git blob SHA matches the locked Perseus file;
- 24 books;
- 12,110 continuously numbered verse lines after documented repairs;
- 24 cleaned book files;
- 24 line-preserving files;
- all source-repair tests pass;
- every segment has an exact book and line range.

## Production source

- PerseusDL `tlg0012.tlg002.perseus-grc2`
- edition associated with A. T. Murray, 1919
- locked Git blob SHA: `f38f5f238d665eafb9c6878b11283822ed418a07`

The original XML is never modified. Five defects in that digital file are repaired only in the derived translation source and recorded in `source/SOURCE_PATCHES.md`:

- Book 3: lines 304–305 restored to ascending XML order;
- Book 10: missing line 456 restored;
- Book 14: lines 63–64 restored to ascending XML order;
- Book 16: missing transmitted line 101 restored and marked textually disputed in some modern editions;
- Book 23: actual line 48 restored and the mislabeled XML line 48 renumbered as 49.

## Segmentation

- target: about 6,200 Greek characters, excluding whitespace;
- normal range: 3,500–8,200 characters;
- speeches and encoded paragraph units are preserved where possible;
- no segment crosses a book boundary;
- affected segments identify their source-patch IDs in metadata.

## Rebuild

The GitHub Actions workflow runs automatically when source tooling changes and can also be started manually from **Actions → Build cleaned Odyssey Greek source**.
