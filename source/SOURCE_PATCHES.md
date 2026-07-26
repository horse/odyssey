# Source patches

The downloaded Perseus XML is preserved unchanged in `original/`. The clean
derived text applies the following explicit repairs so the translation source
has continuous standard verse order and 12,110 numbered lines.

## PATCH-OD03-304-305-ORDER

- Book: 3
- Action: `restore_xml_element_order_by_line_number`
- Note: The locked Perseus XML places line 305 before line 304; the derived clean text restores ascending verse order without changing wording.
- Comparison source: Perseus XML line identifiers and standard verse order

## PATCH-OD14-63-64-ORDER

- Book: 14
- Action: `restore_xml_element_order_by_line_number`
- Note: The locked Perseus XML places line 64 before line 63; the derived clean text restores ascending verse order without changing wording.
- Comparison source: Perseus XML line identifiers and standard verse order

## PATCH-OD10-456

- Book: 10
- Action: `insert_missing_line`
- Note: The locked Perseus XML jumps from line 455 to 457.
- Comparison source: Scaife ATLAS Homer Odyssey 10.456

```grc
μηκέτι νῦν θαλερὸν γόον ὄρνυτε· οἶδα καὶ αὐτὴ
```

## PATCH-OD16-101

- Book: 16
- Action: `insert_missing_line`
- Note: The locked Perseus XML jumps from line 100 to 102. This transmitted line is restored for continuous standard numbering; some modern editors question or omit it.
- Comparison source: Greek Language Centre Odyssey 16.101
- Textual status: `disputed_in_some_modern_editions`

```grc
ἔλθοι ἀλητεύων· ἔτι γὰρ καὶ ἐλπίδος αἶσα·
```

## PATCH-OD23-48-49

- Book: 23
- Action: `insert_line_48_and_renumber_mislabeled_line_48_as_49`
- Note: The locked Perseus XML labels the standard line 23.49 as 23.48 and omits the actual standard line 23.48.
- Comparison source: Dickinson College Commentaries Odyssey 23.1–48

Inserted 23.48:

```grc
αἵματι καὶ λύθρῳ πεπαλαγμένον ὥς τε λέοντα.
```

Existing XML line renumbered as 23.49:

```grc
νῦν δʼ οἱ μὲν δὴ πάντες ἐπʼ αὐλείῃσι θύρῃσιν
```
