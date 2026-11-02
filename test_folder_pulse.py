import tempfile
import unittest
from pathlib import Path
from folder_pulse import scan


class ScanTests(unittest.TestCase):
    def test_nested_files_and_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / "a.TXT").write_bytes(b"hello")
            (root / "nested" / "b.txt").write_bytes(b"hi")
            (root / "LICENSE").write_bytes(b"abc")
            report = scan(root)
            self.assertEqual(report["file_count"], 3)
            self.assertEqual(report["total_bytes"], 10)
            self.assertEqual(report["extensions"], {".txt": 2, "[no extension]": 1})
            self.assertEqual(report["largest_files"][0], {"path": "a.TXT", "bytes": 5})

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(scan(directory)["file_count"], 0)

    def test_invalid_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                scan(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
