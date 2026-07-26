#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SOURCE_URL = (
    'https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/'
    'data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml'
)
EXPECTED_SHA = 'f38f5f238d665eafb9c6878b11283822ed418a07'
EXPECTED_LINES = {
    1: 444, 2: 434, 3: 497, 4: 847, 5: 493, 6: 331,
    7: 347, 8: 586, 9: 566, 10: 574, 11: 640, 12: 453,
    13: 440, 14: 533, 15: 557, 16: 481, 17: 606, 18: 428,
    19: 604, 20: 394, 21: 434, 22: 501, 23: 372, 24: 548,
}
TEI = '{http://www.tei-c.org/ns/1.0}'
TARGET, MINIMUM, MAXIMUM = 6200, 3500, 8200


@dataclass
class Verse:
    book: int
    line: int
    text: str
    para: bool
    quote: Optional[int]


@dataclass
class Atom:
    verses: list[Verse]
    kind: str

    @property
    def chars(self) -> int:
        return count_chars(' '.join(v.text for v in self.verses))


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def norm(text: str) -> str:
    return re.sub(
        r'\s+',
        ' ',
        unicodedata.normalize('NFC', text)
        .replace('\u00a0', ' ')
        .replace('\u200b', ''),
    ).strip()


def count_chars(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def download(path: Path) -> str:
    data = urllib.request.urlopen(SOURCE_URL, timeout=120).read()
    sha = blob_sha(data)
    if sha != EXPECTED_SHA:
        raise SystemExit(f'Source SHA mismatch: expected {EXPECTED_SHA}, received {sha}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha


def parse(path: Path) -> tuple[dict[int, list[Verse]], str]:
    raw = path.read_bytes()
    root = ET.fromstring(raw)
    books: dict[int, list[Verse]] = {}
    edition = root.find(f'.//{TEI}div[@type="edition"]')
    if edition is None:
        raise ValueError('No TEI edition division found')

    for book_element in edition.findall(f'./{TEI}div[@subtype="book"]'):
        book_number = int(book_element.attrib['n'])
        quote_ids = {
            id(quote): index + 1
            for index, quote in enumerate(book_element.iter(f'{TEI}q'))
        }
        verses: list[Verse] = []

        def walk(element: ET.Element, quote_id: Optional[int] = None) -> None:
            if element.tag == f'{TEI}q':
                quote_id = quote_ids[id(element)]
            if element.tag == f'{TEI}l':
                verses.append(
                    Verse(
                        book=book_number,
                        line=int(element.attrib['n']),
                        text=norm(''.join(element.itertext())),
                        para=any(
                            child.tag == f'{TEI}milestone'
                            and child.attrib.get('unit') == 'para'
                            for child in element.iter()
                        ),
                        quote=quote_id,
                    )
                )
                return
            for child in list(element):
                walk(child, quote_id)

        walk(book_element)
        books[book_number] = verses

    return books, blob_sha(raw)


def _insert_between(
    verses: list[Verse],
    *,
    line: int,
    text: str,
    previous_line: int,
    next_line: int,
) -> None:
    previous = next(v for v in verses if v.line == previous_line)
    following = next(v for v in verses if v.line == next_line)
    quote = previous.quote if previous.quote == following.quote else previous.quote
    verses.append(Verse(previous.book, line, norm(text), False, quote))
    verses.sort(key=lambda verse: verse.line)


def _repair_order(
    books: dict[int, list[Verse]],
    patches: dict[str, dict],
    *,
    book: int,
    first: int,
    second: int,
    patch_id: str,
) -> None:
    if book not in books:
        return
    verses = books[book]
    actual = [verse.line for verse in verses]
    sorted_lines = sorted(actual)
    if actual == sorted_lines:
        return
    positions = {line: actual.index(line) for line in (first, second)}
    if positions[first] < positions[second]:
        raise ValueError(f'{patch_id}: unexpected line-order anomaly')
    verses.sort(key=lambda verse: verse.line)
    patches[patch_id] = {
        'book': book,
        'lines': [second, first],
        'action': 'restore_xml_element_order_by_line_number',
        'note': (
            f'The locked Perseus XML places line {first} before line {second}; '
            'the derived clean text restores ascending verse order without changing wording.'
        ),
        'comparison_source': 'Perseus XML line identifiers and standard verse order',
    }


def apply_source_patches(books: dict[int, list[Verse]]) -> dict[str, dict]:
    """Apply documented repairs to derived text; never alter the downloaded XML."""
    patches: dict[str, dict] = {}

    _repair_order(
        books,
        patches,
        book=3,
        first=305,
        second=304,
        patch_id='PATCH-OD03-304-305-ORDER',
    )
    _repair_order(
        books,
        patches,
        book=14,
        first=64,
        second=63,
        patch_id='PATCH-OD14-63-64-ORDER',
    )

    if 10 in books:
        verses = books[10]
        lines = {v.line for v in verses}
        if 456 not in lines:
            if not {455, 457}.issubset(lines):
                raise ValueError('Cannot apply PATCH-OD10-456: adjacent lines missing')
            _insert_between(
                verses,
                line=456,
                text='μηκέτι νῦν θαλερὸν γόον ὄρνυτε· οἶδα καὶ αὐτὴ',
                previous_line=455,
                next_line=457,
            )
            patches['PATCH-OD10-456'] = {
                'book': 10,
                'line': 456,
                'action': 'insert_missing_line',
                'text': 'μηκέτι νῦν θαλερὸν γόον ὄρνυτε· οἶδα καὶ αὐτὴ',
                'note': 'The locked Perseus XML jumps from line 455 to 457.',
                'comparison_source': 'Scaife ATLAS Homer Odyssey 10.456',
            }

    if 16 in books:
        verses = books[16]
        lines = {v.line for v in verses}
        if 101 not in lines:
            if not {100, 102}.issubset(lines):
                raise ValueError('Cannot apply PATCH-OD16-101: adjacent lines missing')
            _insert_between(
                verses,
                line=101,
                text='ἔλθοι ἀλητεύων· ἔτι γὰρ καὶ ἐλπίδος αἶσα·',
                previous_line=100,
                next_line=102,
            )
            patches['PATCH-OD16-101'] = {
                'book': 16,
                'line': 101,
                'action': 'insert_missing_line',
                'text': 'ἔλθοι ἀλητεύων· ἔτι γὰρ καὶ ἐλπίδος αἶσα·',
                'note': (
                    'The locked Perseus XML jumps from line 100 to 102. '
                    'This transmitted line is restored for continuous standard numbering; '
                    'some modern editors question or omit it.'
                ),
                'comparison_source': 'Greek Language Centre Odyssey 16.101',
                'textual_status': 'disputed_in_some_modern_editions',
            }

    if 23 in books:
        verses = books[23]
        line_48 = next((v for v in verses if v.line == 48), None)
        line_49 = next((v for v in verses if v.line == 49), None)
        if line_49 is None and line_48 is not None and line_48.text.startswith('νῦν δʼ οἱ μὲν'):
            line_48.line = 49
            verses.append(
                Verse(
                    23,
                    48,
                    norm('αἵματι καὶ λύθρῳ πεπαλαγμένον ὥς τε λέοντα.'),
                    False,
                    line_48.quote,
                )
            )
            verses.sort(key=lambda verse: verse.line)
            patches['PATCH-OD23-48-49'] = {
                'book': 23,
                'lines': [48, 49],
                'action': 'insert_line_48_and_renumber_mislabeled_line_48_as_49',
                'inserted_text': 'αἵματι καὶ λύθρῳ πεπαλαγμένον ὥς τε λέοντα.',
                'renumbered_text': 'νῦν δʼ οἱ μὲν δὴ πάντες ἐπʼ αὐλείῃσι θύρῃσιν',
                'note': (
                    'The locked Perseus XML labels the standard line 23.49 as 23.48 '
                    'and omits the actual standard line 23.48.'
                ),
                'comparison_source': 'Dickinson College Commentaries Odyssey 23.1–48',
            }

    return patches


def validate(books: dict[int, list[Verse]]) -> None:
    if sorted(books) != list(range(1, 25)):
        raise AssertionError(f'Expected books 1–24, found {sorted(books)}')
    total = sum(len(verses) for verses in books.values())
    if total != 12110:
        raise AssertionError(f'Expected 12110 lines after repair, found {total}')

    for book, verses in books.items():
        if len(verses) != EXPECTED_LINES[book]:
            raise AssertionError(
                f'Book {book}: expected {EXPECTED_LINES[book]} lines, found {len(verses)}'
            )
        expected_numbers = list(range(1, len(verses) + 1))
        actual_numbers = [verse.line for verse in verses]
        if actual_numbers != expected_numbers:
            raise AssertionError(f'Book {book}: non-continuous line numbering')
        if not all(
            verse.text
            and unicodedata.normalize('NFC', verse.text) == verse.text
            and '<' not in verse.text
            and '>' not in verse.text
            for verse in verses
        ):
            raise AssertionError(f'Book {book}: invalid cleaned verse content')


def atoms(verses: list[Verse]) -> list[Atom]:
    output: list[Atom] = []
    current: list[Verse] = []
    quote: Optional[int] = None

    def flush() -> None:
        nonlocal current
        if current:
            output.append(Atom(current, 'SPEECH' if quote else 'NARRATIVE'))
            current = []

    for verse in verses:
        if current and (verse.quote != quote or verse.para):
            flush()
        quote = verse.quote
        current.append(verse)
    flush()
    return output


def split_atom(atom: Atom) -> list[Atom]:
    if atom.chars <= MAXIMUM:
        return [atom]
    output: list[Atom] = []
    current: list[Verse] = []
    size = 0
    for verse in atom.verses:
        verse_size = count_chars(verse.text)
        if current and size + verse_size > TARGET:
            output.append(Atom(current, atom.kind + '_CONTINUED'))
            current = []
            size = 0
        current.append(verse)
        size += verse_size
    if current:
        output.append(Atom(current, atom.kind + '_CONTINUED'))
    return output


def segment(verses: list[Verse]) -> list[list[Atom]]:
    expanded: list[Atom] = []
    for atom in atoms(verses):
        expanded.extend(split_atom(atom))

    segments: list[list[Atom]] = []
    current: list[Atom] = []
    size = 0
    for atom in expanded:
        if current and size + atom.chars > MAXIMUM and size >= MINIMUM:
            segments.append(current)
            current = []
            size = 0
        current.append(atom)
        size += atom.chars
        if size >= TARGET:
            segments.append(current)
            current = []
            size = 0

    if current:
        if (
            segments
            and size < MINIMUM
            and sum(atom.chars for atom in segments[-1]) + size <= MAXIMUM + 700
        ):
            segments[-1].extend(current)
        else:
            segments.append(current)
    return segments


def patch_ids_for_range(
    patches: dict[str, dict], book: int, start: int, end: int
) -> list[str]:
    found: list[str] = []
    for patch_id, patch in patches.items():
        if patch['book'] != book:
            continue
        affected = patch.get('lines', [patch.get('line')])
        if any(line is not None and start <= line <= end for line in affected):
            found.append(patch_id)
    return found


def write_patch_records(root: Path, patches: dict[str, dict]) -> None:
    (root / 'source_patches.json').write_text(
        json.dumps(patches, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    sections = [
        '# Source patches',
        '',
        'The downloaded Perseus XML is preserved unchanged in `original/`. The clean',
        'derived text applies the following explicit repairs so the translation source',
        'has continuous standard verse order and 12,110 numbered lines.',
        '',
    ]
    for patch_id, patch in patches.items():
        sections.extend([
            f'## {patch_id}',
            '',
            f'- Book: {patch["book"]}',
            f'- Action: `{patch["action"]}`',
            f'- Note: {patch["note"]}',
            f'- Comparison source: {patch["comparison_source"]}',
        ])
        if patch.get('textual_status'):
            sections.append(f'- Textual status: `{patch["textual_status"]}`')
        if patch.get('text'):
            sections.extend(['', '```grc', patch['text'], '```'])
        if patch.get('inserted_text'):
            sections.extend([
                '', 'Inserted 23.48:', '', '```grc', patch['inserted_text'], '```'
            ])
        if patch.get('renumbered_text'):
            sections.extend([
                '', 'Existing XML line renumbered as 23.49:', '',
                '```grc', patch['renumbered_text'], '```'
            ])
        sections.append('')
    (root / 'SOURCE_PATCHES.md').write_text('\n'.join(sections), encoding='utf-8')


def main() -> None:
    root = Path('source')
    original = root / 'original' / 'odyssey_perseus_grc2.xml'
    sha = download(original)
    books, parsed_sha = parse(original)
    if sha != parsed_sha:
        raise AssertionError('Downloaded and parsed source hashes differ')

    patches = apply_source_patches(books)
    expected_patch_ids = {
        'PATCH-OD03-304-305-ORDER',
        'PATCH-OD10-456',
        'PATCH-OD14-63-64-ORDER',
        'PATCH-OD16-101',
        'PATCH-OD23-48-49',
    }
    if set(patches) != expected_patch_ids:
        raise AssertionError(
            f'Expected source patches {sorted(expected_patch_ids)}, '
            f'applied {sorted(patches)}'
        )
    validate(books)

    for directory in ['books', 'lines', 'segments']:
        (root / directory).mkdir(parents=True, exist_ok=True)
    write_patch_records(root, patches)

    manifest: list[list[object]] = []
    for book in range(1, 25):
        verses = books[book]
        (root / 'lines' / f'book_{book:02d}_lines.tsv').write_text(
            '\n'.join(f'{book}.{verse.line}\t{verse.text}' for verse in verses) + '\n',
            encoding='utf-8',
        )

        paragraphs: list[str] = []
        current: list[str] = []
        quote = verses[0].quote
        for verse in verses:
            if current and (verse.para or verse.quote != quote):
                paragraphs.append(' '.join(current))
                current = []
            current.append(verse.text)
            quote = verse.quote
        if current:
            paragraphs.append(' '.join(current))
        (root / 'books' / f'book_{book:02d}_clean.txt').write_text(
            '\n\n'.join(paragraphs) + '\n',
            encoding='utf-8',
        )

        for index, atom_group in enumerate(segment(verses), 1):
            segment_verses = [verse for atom in atom_group for verse in atom.verses]
            segment_id = f'ODY-B{book:02d}-S{index:02d}'
            chars = count_chars(' '.join(verse.text for verse in segment_verses))
            flags = '|'.join(sorted({atom.kind for atom in atom_group}))
            patch_ids = patch_ids_for_range(
                patches,
                book,
                segment_verses[0].line,
                segment_verses[-1].line,
            )
            body = '\n'.join(
                f'[{book}.{verse.line}] {verse.text}' for verse in segment_verses
            )
            text = (
                f'# {segment_id}\n\n'
                '- SOURCE_URN: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2\n'
                f'- SOURCE_GIT_BLOB_SHA: {sha}\n'
                f'- BOOK: {book}\n'
                f'- LINES: {book}.{segment_verses[0].line}–{book}.{segment_verses[-1].line}\n'
                f'- GREEK_CHARS_NO_SPACE: {chars}\n'
                f'- STRUCTURE_FLAGS: {flags}\n'
                f'- SOURCE_PATCH_IDS: {", ".join(patch_ids) if patch_ids else "none"}\n'
                '- STATUS: SOURCE_READY\n\n'
                '## Translation instruction\n\n'
                'Line numbers in square brackets are references only. Do not translate them. '
                'Translate all Greek content.\n\n'
                '## Greek source\n\n'
                f'{body}\n'
            )
            (root / 'segments' / f'{segment_id}_SOURCE.md').write_text(
                text,
                encoding='utf-8',
            )
            manifest.append([
                segment_id,
                book,
                segment_verses[0].line,
                segment_verses[-1].line,
                chars,
                flags,
                ','.join(patch_ids),
                'SOURCE_READY',
            ])

    header = [
        'segment_id', 'book', 'start_line', 'end_line',
        'greek_chars_no_space', 'flags', 'source_patch_ids', 'status',
    ]
    (root / 'manifest.tsv').write_text(
        '\t'.join(header)
        + '\n'
        + '\n'.join('\t'.join(map(str, row)) for row in manifest)
        + '\n',
        encoding='utf-8',
    )

    info = {
        'source_url': SOURCE_URL,
        'source_git_blob_sha': sha,
        'books': 24,
        'verse_lines': 12110,
        'segments': len(manifest),
        'target_chars': TARGET,
        'minimum_chars': MINIMUM,
        'maximum_chars': MAXIMUM,
        'source_patches': sorted(patches),
    }
    (root / 'source_build.json').write_text(
        json.dumps(info, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    (root / 'README.md').write_text(
        '# Ready-to-translate Greek source\n\n'
        'Validated: 24 books and 12,110 continuously numbered lines after five '
        'documented source repairs. Upload only the current book’s '
        '`segments/ODY-Bxx-*` files into a ChatGPT Project. See '
        '`SOURCE_PATCHES.md` for the repair record.\n',
        encoding='utf-8',
    )
    print(json.dumps(info, ensure_ascii=False))


if __name__ == '__main__':
    main()
