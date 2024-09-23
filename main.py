import logging
import os
import json
import jieba
from pathlib import Path
from RimeHandler import RimeFileHandler, RimeSQLiteHandler, RimeEntry
from PinyinTools import quanpin_to_xiaohe, word_get_pinyin
from Crawler import fetch_new_sentences, RebangParser
from Tokenizer import LLM_Split_words
import asyncio
from logger_config import setup_logger, inspect_trace

# 配置日志系统
logger = setup_logger()

# 读取配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

SPLIT_WORDS_MODE = config.get('SPLIT_WORDS_MODE')

# 读取之前的词集合
user_dict_path = Path(config.get('USER_DICT_PATH'))
user_dict_db_path = Path(config.get('USER_DICT_DB_PATH'))

# 创建 RimeFileHandler 和 RimeSQLiteHandler 实例
file_handler = RimeFileHandler(user_dict_path)
sqlite_handler = RimeSQLiteHandler(user_dict_db_path)

# 从词库文件读取
if os.path.exists(user_dict_path):
    old_user_dict = file_handler.read_dict()
else:
    old_user_dict = {}

# API URL
source_api_url = "https://api.rebang.today/v1/items"
params = {
    "tab": "top",
    "sub_tab": "today",
    "version": 1
}

new_sentences_list = fetch_new_sentences(source_api_url, params=params, parser=RebangParser())

# 打印获取到的标题
for index, sentence in enumerate(new_sentences_list):
    logger.info(f"{index + 1} {sentence}")


def process_new_words(new_words_set):
    # 生成新用户词典
    new_user_dict = {}
    for word in new_words_set:
        try:
            full_pinyin = word_get_pinyin(word)
            xiaohe_pinyin = [quanpin_to_xiaohe(item) for item in full_pinyin]
            logger.debug(f"{xiaohe_pinyin}")
        except Exception as e:
            logger.error(f"Error processing word '{word}': {e}")
            inspect_trace()
            continue

        # 如果该词语的拼音解析转换没有出错，那么就会被添加到新用户词典当中
        rimeentry = RimeEntry(''.join(xiaohe_pinyin), 1)
        if word not in old_user_dict:
            new_user_dict[word] = rimeentry

    logger.info(f"{new_words_set}")
    for item in new_user_dict:
        logger.info(f"{item}: {new_user_dict[item]}")

    # 保存到SQLite数据库
    if not os.path.exists(user_dict_db_path):
        # 初次运行，备份老用户词典的数据到数据库中，后面只需要追加新词
        sqlite_handler.save_sqlite(old_user_dict)

    sqlite_handler.save_sqlite(new_user_dict)

    # 追加新词条到词库文件
    append_result = file_handler.append_dict(new_user_dict, add_date_comment=True)

    if append_result:
        logger.info(f"{len(new_user_dict)} 个新词条已成功追加到词库文件当中。")
        logger.info("本次运行结束")
    else:
        logger.error("追加新词条到词库文件时发生错误。")
        logger.error("本次运行结束")


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
    # 为了异步运行
    asyncio.run(main())
