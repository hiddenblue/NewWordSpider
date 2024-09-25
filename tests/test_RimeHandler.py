import unittest
from pathlib import Path
from RimeHandler import RimeFileHandler, RimeSQLiteHandler, RimeEntry

class TestRimeFileHandler(unittest.TestCase):

    def setUp(self):
        self.test_file_path = Path("test_rime_user_dict.txt")
        self.file_handler = RimeFileHandler(self.test_file_path)

    def tearDown(self):
        if self.test_file_path.exists():
            self.test_file_path.unlink()

    def test_read_dict(self):
        # 创建一个测试文件
        with self.test_file_path.open("w", encoding="utf-8") as f:
            f.write("词条1\tcode1\t100\n")
            f.write("词条2\tcode2\n")

        user_dict = self.file_handler.read_dict()
        expected_dict = {
            "词条1": RimeEntry("code1", "100"),
            "词条2": RimeEntry("code2", None),
        }
        self.assertEqual(user_dict, expected_dict)

    def test_write_dict(self):
        user_dict = {
            "词条1": RimeEntry("code1", "100"),
            "词条2": RimeEntry("code2", None),
        }
        success = self.file_handler.write_dict(user_dict)
        self.assertTrue(success)

        # 读取文件内容并验证
        with self.test_file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        expected_content = "词条1\tcode1\t100\n词条2\tcode2\n"
        self.assertEqual(content, expected_content)

    def test_append_dict(self):
        # 创建一个测试文件
        with self.test_file_path.open("w", encoding="utf-8") as f:
            f.write("词条1\tcode1\t100\n")

        new_entries = {
            "新词条1": RimeEntry("xin1ci2tiao3", "100"),
            "新词条2": RimeEntry("xin1ci2tiao3", None),
        }
        success = self.file_handler.append_dict(new_entries, add_date_comment=True)
        self.assertTrue(success)

        # 读取文件内容并验证
        with self.test_file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("新词条1\txin1ci2tiao3\t100", content)
        self.assertIn("新词条2\txin1ci2tiao3", content)
        self.assertIn("# Added on", content)


class TestRimeSQLiteHandler(unittest.TestCase):

    def setUp(self):
        self.test_db_path = Path("test_rime_user_dict.db")
        self.sqlite_handler = RimeSQLiteHandler(self.test_db_path)

    def tearDown(self):
        if self.test_db_path.exists():
            self.test_db_path.unlink()

    def test_save_sqlite(self):
        user_dict = {
            "词条1": RimeEntry("code1", "100"),
            "词条2": RimeEntry("code2", None),
        }
        success = self.sqlite_handler.save_sqlite(user_dict)
        self.assertTrue(success)

        # 验证数据库内容
        loaded_dict = self.sqlite_handler.load_sqlite()
        self.assertEqual(loaded_dict, user_dict)

    def test_load_sqlite(self):
        user_dict = {
            "词条1": RimeEntry("code1", "100"),
            "词条2": RimeEntry("code2", None),
        }
        self.sqlite_handler.save_sqlite(user_dict)

        # 验证数据库内容
        loaded_dict = self.sqlite_handler.load_sqlite()
        self.assertEqual(loaded_dict, user_dict)

if __name__ == "__main__":
    unittest.main()