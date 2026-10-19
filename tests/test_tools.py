import json
import tempfile
import unittest
from pathlib import Path

from utility_lab.tools import (bulk_renamer, csv_summary, duplicate_finder, file_organizer,
                               password_generator as pg, text_tools as tt, todo_manager as todo,
                               unit_converter as uc)


class PasswordTests(unittest.TestCase):
    def test_length_and_classes(self):
        for _ in range(50):
            p = pg.generate_password(12)
            self.assertEqual(len(p), 12)
            self.assertTrue(any(c.isupper() for c in p))
            self.assertTrue(any(c.isdigit() for c in p))
            self.assertTrue(any(not c.isalnum() for c in p))

    def test_too_short(self):
        with self.assertRaises(ValueError):
            pg.generate_password(2)

    def test_passphrase(self):
        self.assertEqual(len(pg.generate_passphrase(5).split("-")), 5)

    def test_strength(self):
        self.assertEqual(pg.strength("abc"), "Weak")
        self.assertEqual(pg.strength("Abcdefgh123!xyz"), "Strong")


class TextTests(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(tt.to_snake_case("Hello World"), "hello_world")
        self.assertEqual(tt.to_snake_case("helloWorldFoo"), "hello_world_foo")
        self.assertEqual(tt.to_camel_case("hello big world"), "helloBigWorld")
        self.assertEqual(tt.to_title_case("hello_world"), "Hello World")

    def test_slug_and_palindrome(self):
        self.assertEqual(tt.slugify("  Héllo, World! "), "hello-world")
        self.assertTrue(tt.is_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(tt.is_palindrome("python"))
        self.assertFalse(tt.is_palindrome(""))

    def test_stats(self):
        s = tt.text_stats("the cat and the hat")
        self.assertEqual(s["words"], 5)
        self.assertEqual(s["top_words"][0], ("the", 2))


class ConverterTests(unittest.TestCase):
    def test_length(self):
        self.assertAlmostEqual(uc.convert(1, "km", "m"), 1000)
        self.assertAlmostEqual(uc.convert(1, "mi", "km"), 1.609344)

    def test_temperature(self):
        self.assertAlmostEqual(uc.convert(100, "c", "f"), 212)
        self.assertAlmostEqual(uc.convert(32, "F", "C"), 0)
        self.assertAlmostEqual(uc.convert(0, "c", "k"), 273.15)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            uc.convert(1, "kg", "km")


class FileToolTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_organizer_dry_run_then_apply(self):
        (self.dir / "a.jpg").write_text("x")
        (self.dir / "b.pdf").write_text("y")
        (self.dir / "c.unknown").write_text("z")
        preview = file_organizer.organize_directory(self.dir, dry_run=True)
        self.assertEqual(len(preview), 3)
        self.assertTrue((self.dir / "a.jpg").exists())          # nothing moved yet
        file_organizer.organize_directory(self.dir, dry_run=False)
        self.assertTrue((self.dir / "Images" / "a.jpg").exists())
        self.assertTrue((self.dir / "Documents" / "b.pdf").exists())
        self.assertTrue((self.dir / "Other" / "c.unknown").exists())

    def test_organizer_name_collision(self):
        (self.dir / "Images").mkdir()
        (self.dir / "Images" / "a.jpg").write_text("old")
        (self.dir / "a.jpg").write_text("new")
        file_organizer.organize_directory(self.dir, dry_run=False)
        self.assertTrue((self.dir / "Images" / "a (1).jpg").exists())

    def test_numbered_rename(self):
        for n in ("x.txt", "y.txt", "z.txt"):
            (self.dir / n).write_text(n)
        plan = bulk_renamer.plan_numbered(self.dir, "doc_", extension="txt")
        bulk_renamer.apply_plan(plan, dry_run=False)
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()),
                         ["doc_001.txt", "doc_002.txt", "doc_003.txt"])

    def test_replace_rename_and_overwrite_protection(self):
        (self.dir / "old_a.txt").write_text("1")
        (self.dir / "new_a.txt").write_text("2")
        plan = bulk_renamer.plan_replace(self.dir, "old", "new")
        with self.assertRaises(FileExistsError):
            bulk_renamer.apply_plan(plan, dry_run=False)

    def test_duplicates(self):
        (self.dir / "a.txt").write_text("same")
        (self.dir / "b.txt").write_text("same")
        (self.dir / "c.txt").write_text("diff")
        groups = duplicate_finder.find_duplicates(self.dir)
        self.assertEqual(len(groups), 1)
        self.assertEqual({p.name for p in groups[0]}, {"a.txt", "b.txt"})

    def test_csv_summary(self):
        f = self.dir / "d.csv"
        f.write_text("name,score\nann,10\nbob,20\nann,\n")
        s = csv_summary.summarize_csv(f)
        self.assertEqual(s["rows"], 3)
        self.assertEqual(s["columns"]["score"]["type"], "numeric")
        self.assertEqual(s["columns"]["score"]["mean"], 15)
        self.assertEqual(s["columns"]["score"]["missing"], 1)
        self.assertEqual(s["columns"]["name"]["top"][0], ("ann", 2))


class TodoTests(unittest.TestCase):
    def test_lifecycle(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "todos.json"
            a = todo.add_task("Write tests", path)
            b = todo.add_task("Ship it", path)
            self.assertEqual((a["id"], b["id"]), (1, 2))
            self.assertTrue(todo.complete_task(1, path))
            self.assertFalse(todo.complete_task(99, path))
            self.assertTrue(todo.remove_task(2, path))
            tasks = json.loads(path.read_text())
            self.assertEqual(len(tasks), 1)
            self.assertTrue(tasks[0]["done"])

    def test_empty_title(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                todo.add_task("   ", Path(d) / "t.json")


if __name__ == "__main__":
    unittest.main()
