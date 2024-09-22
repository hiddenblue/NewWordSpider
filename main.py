import os
import json
import jieba
import re
from pathlib import Path
from RimeUser import (RimeEntry,
                      read_rime_user_dict,
                      write_rime_user_dict,
                      append_rime_user_dict,
                      load_from_sqlite,
                      save_to_sqlite)
from PinyinAdder import add_pinyin_to_words
from QuanPintoXiaohe import safe_full_to_xiaohe
from crawler import fetch_new_sentences
from tokenizer import LLM_Split_words
import aiohttp
import asyncio

from logger_config import setup_logger

from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

# 读取配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

API_URL = config.get('API_URL')
API_KEY = config.get('API_KEY')
SPLIT_WORDS_MODE = config.get('SPLIT_WORDS_MODE')

# 读取之前的词集合
user_dict_path = Path(config.get('USER_DICT_PATH'))
user_dict_db_path = Path(config.get('USER_DICT_DB_PATH'))

# 从词库文件读取
if os.path.exists(user_dict_path):
    old_user_dict = read_rime_user_dict(user_dict_path)
else:
    old_user_dict = {}

# API URL
api_url = "https://api.rebang.today/v1/items"

new_sentences_list = fetch_new_sentences(api_url)

# 打印获取到的标题
for index, sentence in enumerate(new_sentences_list):
    logger.info(f"{index + 1} {sentence}" )

def process_new_words(new_words_set):
    # 生成新用户词典
    new_user_dict = {}
    for word in new_words_set:
        try:
            full_pinyin = add_pinyin_to_words(word)
            xiaohe_pinyin = [safe_full_to_xiaohe(item) for item in full_pinyin]
            logger.info(f"{xiaohe_pinyin}")
        except Exception as e:
            logger.error(f"Error processing word '{word}': {e}")
            continue

        rimeentry = RimeEntry(''.join(xiaohe_pinyin), 1)

        if word not in old_user_dict:
            new_user_dict[word] = rimeentry

    # 保存到SQLite数据库
    if not os.path.exists(user_dict_db_path):
        # 初次运行，备份老用户词典的数据到数据库中，后面只需要追加新词
        save_to_sqlite(user_dict_db_path, old_user_dict)

    save_to_sqlite(user_dict_db_path, new_user_dict)

    # 追加新词条到词库文件
    Append_result = append_rime_user_dict(user_dict_path, new_user_dict, add_date_comment=True)

    if Append_result:
        logger.info("新词条已成功追加到词库文件。")
    else:
        logger.error("追加新词条到词库文件时发生错误。")

async def main():
    if SPLIT_WORDS_MODE == 'deepseek':
        new_words_set = await LLM_Split_words(new_sentences_list)
    else:
        new_words_set = set()
        for sentence in new_sentences_list:
            words = jieba.lcut(sentence)
            new_words_set.update(words)

    logger.info(f"new_words_set: {new_words_set}")
    logger.info(f"new_words_set length: {len(new_words_set)}")

    process_new_words(new_words_set)

# 示例用法
if __name__ == "__main__":
    asyncio.run(main())