import unittest
from PinyinTools import quanpin_to_xiaohe, word_get_pinyin

class TestPinyinTools(unittest.TestCase):

    def test_quanpin_to_xiaohe(self):
        # 测试长度为1的拼音
        self.assertEqual(quanpin_to_xiaohe("a"), "aa")
        self.assertEqual(quanpin_to_xiaohe("o"), "oo")

        # 测试长度为2的拼音
        self.assertEqual(quanpin_to_xiaohe("ai"), "ai")
        self.assertEqual(quanpin_to_xiaohe("ei"), "ei")

        # 测试长度为3的拼音
        self.assertEqual(quanpin_to_xiaohe("shi"), "ui")
        self.assertEqual(quanpin_to_xiaohe("chi"), "ii")
        self.assertEqual(quanpin_to_xiaohe("lve"), "lt")
        self.assertEqual(quanpin_to_xiaohe("xue"), "xt")


        # 测试长度为4的拼音
        self.assertEqual(quanpin_to_xiaohe("shuo"), "uo")
        self.assertEqual(quanpin_to_xiaohe("chui"), "iv")
        self.assertEqual(quanpin_to_xiaohe("zhan"), "vj")

        # 测试长度为5的拼音
        self.assertEqual(quanpin_to_xiaohe("shuai"), "uk")
        self.assertEqual(quanpin_to_xiaohe("chuai"), "ik")

        # 测试长度为6的拼音
        self.assertEqual(quanpin_to_xiaohe("shuang"), "ul")
        self.assertEqual(quanpin_to_xiaohe("chuang"), "il")

        # 测试非法输入
        self.assertEqual(quanpin_to_xiaohe(""), "Error: Invalid input: input should be between 1 and 5 characters long")
        self.assertEqual(quanpin_to_xiaohe("abcdef"), "Error: Invalid input: input should be a valid quanpin")
        self.assertEqual(quanpin_to_xiaohe("123"), "Error: Invalid input: input should only contain alphabetic characters and spaces")

    def test_word_get_pinyin(self):
        # 测试单个汉字
        self.assertEqual(word_get_pinyin("我"), ["wo"])
        self.assertEqual(word_get_pinyin("你"), ["ni"])


        # 测试多音字
        self.assertEqual(word_get_pinyin("重要"), ["zhong", "yao"])
        self.assertEqual(word_get_pinyin("长度"), ["chang", "du"])

        # 测试词语
        self.assertEqual(word_get_pinyin("你好"), ["ni", "hao"])
        self.assertEqual(word_get_pinyin("中国"), ["zhong", "guo"])
        self.assertEqual(word_get_pinyin("战略"), ["zhan", "lve"])

        # 测试非法输入
        self.assertEqual(word_get_pinyin("123"), [])
        self.assertEqual(word_get_pinyin(""), [])

if __name__ == "__main__":
    unittest.main()