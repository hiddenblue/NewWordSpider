import unittest
from Tokenizer import filter_chinese_words, jieba_tokenizer
from unittest.mock import patch, MagicMock
from Tokenizer import tokenize_and_filter, jieba_tokenizer, deepseek_tokenizer
import jieba

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

class TestJiebaTokenizer(unittest.TestCase):

    def test_jieba_tokenizer(self):
        sentence = "这是一个测试句子"
        expected_result = ["这是", "一个", "测试", "句子"]
        result =  jieba_tokenizer(sentence)
        self.assertEqual(result, expected_result)


class TestTokenizeAndFilter(unittest.TestCase):

    @patch('Tokenizer.jieba_tokenizer')
    def test_tokenize_and_filter_jieba(self, mock_jieba_tokenizer):
        sentence = "这是一个测试句子"
        expected_result = {"这是", "一个", "测试", "句子"}
        mock_jieba_tokenizer.return_value = ["这是", "一个", "测试", "句子"]
        result = tokenize_and_filter(sentence, jieba_tokenizer)
        self.assertEqual(result, expected_result)


class TestLLMSplitWords(unittest.TestCase):

    @patch('aiohttp.ClientSession')
    @patch('Tokenizer.tokenize_and_filter')
    def test_LLM_Split_words(self, mock_tokenize_and_filter, mock_session):
        sentence_list = [
            "这是一个测试句子",
            "这是另一个测试句子"
        ]
        expected_result = {"这是", "一个", "测试", "句子", "另一个"}
        
        # 模拟 tokenize_and_filter 的返回值
        mock_tokenize_and_filter.side_effect = [{"这是", "一个", "测试", "句子"}, {"这是", "另一个", "测试", "句子"}]

        result = LLM_Split_words(sentence_list)
        self.assertEqual(result, expected_result)

class TestMain(unittest.TestCase):

    @patch('aiohttp.ClientSession')
    @patch('Tokenizer.tokenize_and_filter')
    @patch('Tokenizer.jieba_tokenizer')
    def test_main(self, mock_jieba_tokenizer, mock_tokenize_and_filter, mock_session):
        sentence_list = [
            "这是一个测试句子",
            "这是另一个测试句子"
        ]
        expected_result_jieba = {"这是", "一个", "测试", "句子"}
        expected_result_deepseek = {"这是", "另一个", "测试", "句子"}
        
        # 模拟 jieba_tokenizer 的返回值
        mock_jieba_tokenizer.return_value = ["这是", "一个", "测试", "句子"]
        
        # 模拟 tokenize_and_filter 的返回值
        mock_tokenize_and_filter.side_effect = [expected_result_jieba, expected_result_deepseek]

        main()

        # 验证 tokenize_and_filter 被正确调用
        mock_tokenize_and_filter.assert_any_call(sentence_list[0], jieba_tokenizer)
        mock_tokenize_and_filter.assert_any_call(sentence_list[1], deepseek_tokenizer, mock_session.return_value)


if __name__ == '__main__':
    unittest.main()
