import unittest
from tools.build_source import Verse, apply_source_patches


class SourcePatchTests(unittest.TestCase):
    def test_restores_book_10_line_456(self):
        books = {10: [
            Verse(10, 455, 'before', False, 7),
            Verse(10, 457, 'after', False, 7),
        ]}
        patches = apply_source_patches(books)
        self.assertEqual([v.line for v in books[10]], [455, 456, 457])
        self.assertEqual(books[10][1].text, 'μηκέτι νῦν θαλερὸν γόον ὄρνυτε· οἶδα καὶ αὐτὴ')
        self.assertEqual(books[10][1].quote, 7)
        self.assertIn('PATCH-OD10-456', patches)

    def test_restores_book_16_line_101(self):
        books = {16: [
            Verse(16, 100, 'before', False, 3),
            Verse(16, 102, 'after', False, 3),
        ]}
        patches = apply_source_patches(books)
        self.assertEqual([v.line for v in books[16]], [100, 101, 102])
        self.assertEqual(books[16][1].text, 'ἔλθοι ἀλητεύων· ἔτι γὰρ καὶ ἐλπίδος αἶσα·')
        self.assertIn('PATCH-OD16-101', patches)

    def test_repairs_book_23_misnumbering_and_restores_line_48(self):
        books = {23: [
            Verse(23, 47, 'before', False, 9),
            Verse(23, 48, 'νῦν δʼ οἱ μὲν δὴ πάντες ἐπʼ αὐλείῃσι θύρῃσιν', False, 9),
            Verse(23, 50, 'after', False, 9),
        ]}
        patches = apply_source_patches(books)
        self.assertEqual([v.line for v in books[23]], [47, 48, 49, 50])
        self.assertEqual(books[23][1].text, 'αἵματι καὶ λύθρῳ πεπαλαγμένον ὥς τε λέοντα.')
        self.assertTrue(books[23][2].text.startswith('νῦν δʼ οἱ μὲν'))
        self.assertIn('PATCH-OD23-48-49', patches)


if __name__ == '__main__':
    unittest.main()
