from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tools.build_source import Verse


def _norm(text: str) -> str:
    from tools.build_source import norm
    return norm(text)


def _insert_between(verses, *, line, text, previous_line, next_line):
    from tools.build_source import Verse
    previous = next(v for v in verses if v.line == previous_line)
    following = next(v for v in verses if v.line == next_line)
    quote = previous.quote if previous.quote == following.quote else previous.quote
    verses.append(Verse(previous.book, line, _norm(text), False, quote))
    verses.sort(key=lambda verse: verse.line)


def _repair_order(books, patches, *, book, first, second, patch_id):
    if book not in books:
        return
    verses = books[book]
    actual = [verse.line for verse in verses]
    if actual == sorted(actual):
        return
    positions = {line: actual.index(line) for line in (first, second)}
    if positions[first] > positions[second]:
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


def apply_source_patches(books):
    """Apply five explicit repairs to derived text, leaving original XML untouched."""
    from tools.build_source import Verse

    patches = {}
    _repair_order(
        books, patches, book=3, first=305, second=304,
        patch_id='PATCH-OD03-304-305-ORDER',
    )
    _repair_order(
        books, patches, book=14, first=64, second=63,
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
                text='διογενὲς Λαερτιάδη, πολυμήχανʼ Ὀδυσσεῦ,',
                previous_line=455,
                next_line=457,
            )
            patches['PATCH-OD10-456'] = {
                'book': 10,
                'line': 456,
                'action': 'insert_missing_line',
                'text': 'διογενὲς Λαερτιάδη, πολυμήχανʼ Ὀδυσσεῦ,',
                'note': (
                    'The locked Perseus XML jumps from line 455 to 457; '
                    'the missing standard line is Circe’s vocative address to Odysseus.'
                ),
                'comparison_source': 'Greek Language Centre Odyssey 10.455–460',
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
                    _norm('αἵματι καὶ λύθρῳ πεπαλαγμένον ὥς τε λέοντα.'),
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
