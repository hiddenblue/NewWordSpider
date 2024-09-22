import os
import jieba
import re
import json
import aiohttp
import asyncio
from typing import List, Set

from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

# 读取配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

API_URL = config.get('API_URL')
API_KEY = config.get('API_KEY')

exclude_words = [
    '的', '了', '和', '或', '与', '在', '更', '这', '是', '不']

async def jieba_tokenizer(sentence: str) -> List[str]:
    """
    使用jieba进行分词
    :param sentence: 输入句子
    :return: 分词结果列表
    """
    return jieba.lcut(sentence)

async def deepseek_tokenizer(sentence: str, session: aiohttp.ClientSession) -> List[str]:
    """
    使用 DeepSeek API 进行分词
    :param sentence: 输入句子
    :param session: aiohttp 客户端会话
    :return: 分词结果列表
    """
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 请求数据
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"样例输入 \"2.5亿美元打造游戏史首个变性黑人！揭秘《星鸣特攻》究竟是如何“正确”地走向暴死的\" 样例输出 ['2.5亿美元', '打造', '游戏史', '首个', '变性', '黑人', '揭秘', '星鸣特攻', '究竟', '如何', '正确地', '走向', '暴死']  参靠输入输出对后面这句话进行拆分  {sentence}"}
        ],
        "stream": False
    }

    try:
        # 发送请求
        async with session.post(API_URL, headers=headers, data=json.dumps(data)) as response:
            response.raise_for_status()  # 检查请求是否成功

            # 解析响应数据
            response_data = await response.json()

            # 提取分词结果
            tokenized_phrases = response_data['choices'][0]['message']['content'].strip("[]").split(", ")
            return [phrase.strip("'") for phrase in tokenized_phrases]

    except aiohttp.ClientError as e:
        logger.error(f"请求失败: {e}")
        return []
    except KeyError as e:
        logger.error(f"解析响应数据失败: {e}")
        return []
    except Exception as e:
        logger.error(f"发生未知错误: {e}")
        return []

def filter_chinese_words(words: List[str], min_length: int = 2, max_length: int = 8) -> Set[str]:
    """
    过滤出符合长度要求的中文词
    :param words: 分词结果列表
    :param min_length: 词的最小长度
    :param max_length: 词的最大长度
    :return: 符合要求的中文词集合
    """
    filtered_words = set()
    for word in words:
        if "·" in word:
            word = word.replace("·", "")
        if re.match(r"[\u4e00-\u9fa5]+", word) and min_length <= len(word) <= max_length:
            
            add_word = True
            for i in exclude_words:
                if i in word:
                    add_word = False
                    break
            if word.startswith("一"):
                add_word = False
                
            # 判断word里面是否有数字，有则跳过
            if re.search(r"\d", word):
                add_word = False
                
            if add_word :
                filtered_words.add(word)
    return filtered_words

async def tokenize_and_filter(sentence: str, tokenizer_func, *args, min_length: int = 2, max_length: int = 8) -> Set[str]:
    """
    通用分词和过滤接口
    :param sentence: 输入句子
    :param tokenizer_func: 分词函数
    :param args: 分词函数的额外参数
    :param min_length: 词的最小长度
    :param max_length: 词的最大长度
    :return: 符合要求的中文词集合
    """
    words = await tokenizer_func(sentence, *args)
    return filter_chinese_words(words, min_length, max_length)

async def LLM_Split_words(sentence_list: List[str]) -> Set[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [tokenize_and_filter(sentence, deepseek_tokenizer, session) for sentence in sentence_list]
        results = await asyncio.gather(*tasks) 
    return set.union(*results)

async def main():
    sentence_list = [
        "2.5亿美元打造游戏史首个变性黑人！揭秘《星鸣特攻》究竟是如何“正确”地走向暴死的",
        "1k出头！锐度报表！全画幅75mm F2，质感满满的国货之光，铭匠光学75 F2到底咋样？",
        "日本平成时代所有被停播的违规广告&具体封禁理由",
        "26岁的日本京都大学热血男：为了挽救即将被废除的泡澡社团，他作出的决定是……"
    ]

    for senten in sentence_list:
        splited_words = await tokenize_and_filter(senten, jieba_tokenizer)
        logger.info(f"jieba分词结果: {splited_words}")

    async with aiohttp.ClientSession() as session:
        tasks = [tokenize_and_filter(sentence, deepseek_tokenizer, session) for sentence in sentence_list]
        results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        logger.info(f"句子 {i + 1} 的分词结果: {result}")

# 示例用法
if __name__ == "__main__":
    asyncio.run(main())