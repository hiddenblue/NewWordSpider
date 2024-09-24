import unittest
from Tokenizer import filter_chinese_words


class TestFilterChineseWords(unittest.TestCase):
    def test_filter_chinese_words(self):
        # 测试数据
        words = [
            "中文", "English", "日本語", "一", "一二三", "123", "测试·词", "测试词",
            "非常长的中文词汇但是超过八位", "包含数字123的词", "包含英文的词", "包含·斜杠的词"
        ]

        # 调用待测函数
        result = filter_chinese_words(words)

        # 预期结果
        expected_result = {"中文", "日本語", "测试词"}

        # 断言
        self.assertEqual(result, expected_result)

    def test_filter_chinese_words_min_length(self):
        # 测试数据
        words = ["中", "文", "中文字"]

        # 调用待测函数，设置最小长度为3
        result = filter_chinese_words(words, min_length=3)

        # 预期结果
        expected_result = {"中文字"}

        # 断言
        self.assertEqual(result, expected_result)

    def test_filter_chinese_words_max_length(self):
        # 测试数据
        words = ["短", "中等长度的词", "非常长的词但是不超过八位"]

        # 调用待测函数，设置最大长度为5
        result = filter_chinese_words(words, max_length=5)

        # 预期结果
        expected_result = set()

        # 断言
        self.assertEqual(result, expected_result)

    def test_filter_chinese_words_punctuation(self):
        # 测试数据
        words = ["包含，的词", "包含。的词"]

        # 调用待测函数
        result = filter_chinese_words(words)

        # 预期结果
        expected_result = set()

        # 断言
        self.assertEqual(result, expected_result)


    def test_filter_chinese_words_examples(self):
        # 测试数据
        words = [
            "你好世界",  # 只包含汉字
            "Hello 世界",  # 包含非汉字字符
            "こんにちは世界",  # 包含非汉字字符
            "你好123",  # 包含非汉字字符
            "你好 world",  # 包含非汉字字符
            "你好",  # 只包含汉字
            "",  # 空字符串
            "你好，世界。",  # 包含中文标点符号
            "你好！世界？",  # 包含中文标点符号
            "你好：世界；",  # 包含中文标点符号
            "你好“世界”",  # 包含中文标点符号
            "你好（世界）",  # 包含中文标点符号
            "你好【世界】",  # 包含中文标点符号
            "你好《世界》",  # 包含中文标点符号
            "你好……",  # 包含中文标点符号
            "你好、世界",  # 包含中文标点符号
            "你好—世界",  # 包含中文标点符号
            "你好——世界",  # 包含中文标点符号
            "鸿蒙Next",  # 包含非汉字字符
            "黑神话：悟空",  # 包含中文标点符号
        ]

        # 调用待测函数
        result = filter_chinese_words(words)

        # 预期结果
        expected_result = {"你好世界", "你好"}

        # 断言
        self.assertEqual(result, expected_result)
    def test_filter_chinese_words_with_space(self):
        # 测试数据
        words = [
            "你好 世界",  # 只包含汉字
            " 你好世界",  # 包含非汉字字符
            "你好世界 ",  # 包含非汉字字符
            " 你好 世界 ",  # 包含非汉字字符
            " ",  # 包含非汉字字符
        ]

        # 调用待测函数
        result = filter_chinese_words(words)

        # 预期结果
        expected_result = {"你好世界"}

        # 断言
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
