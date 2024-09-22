from typing import Dict, Optional
from pathlib import Path
from collections import namedtuple
from datetime import datetime
import sqlite3

# 定义命名元组
RimeEntry = namedtuple("RimeEntry", ["code", "weight"])

from logger_config import setup_logger

logger = setup_logger()

def read_rime_user_dict(file_path: Path) -> Dict[str, RimeEntry]:
    """
    读取Rime用户词库文件
    :param file_path: 词库文件路径
    :return: 词库字典，格式为 {词条: RimeEntry}
    """
    user_dict: Dict[str, RimeEntry] = {}
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                # 跳过注释和空行
                if line.startswith("#") or line.strip() == "":
                    continue
                # 按Tab符分割词条、编码和权重
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    word, code = parts
                    weight = None
                elif len(parts) == 3:
                    word, code, weight = parts
                else:
                    raise ValueError(f"Invalid line: {line}")
                user_dict[word] = RimeEntry(code, weight)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except IOError as e:
        logger.error(f"Error reading file: {e}")
        return {}
    return user_dict

def write_rime_user_dict(file_path: Path, user_dict: Dict[str, RimeEntry]) -> bool:
    """
    写入Rime用户词库文件
    :param file_path: 词库文件路径
    :param user_dict: 词库字典，格式为 {词条: RimeEntry}
    :return: 如果写入成功返回 True，否则返回 False
    """
    try:
        with file_path.open("w", encoding="utf-8") as f:
            for word, entry in user_dict.items():
                if entry.weight:
                    f.write(f"{word}\t{entry.code}\t{entry.weight}\n")
                else:
                    f.write(f"{word}\t{entry.code}\n")
        return True
    except IOError as e:
        logger.error(f"Error writing file: {e}")
        return False

def append_rime_user_dict(file_path: Path, new_entries: Dict[str, RimeEntry], add_date_comment: bool = False) -> bool:
    """
    追加新行到Rime用户词库文件
    :param file_path: 词库文件路径
    :param new_entries: 新词条字典，格式为 {词条: RimeEntry}
    :param add_date_comment: 是否添加日期注释
    :return: 如果追加成功返回 True，否则返回 False
    """
    try:
        with file_path.open("a", encoding="utf-8") as f:
            if add_date_comment:
                f.write(f"\n# Added on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for word, entry in new_entries.items():
                if entry.weight:
                    f.write(f"{word}\t{entry.code}\t{entry.weight}\n")
                else:
                    f.write(f"{word}\t{entry.code}\n")
        return True
    except IOError as e:
        logger.error(f"Error appending to file: {e}")
        return False

def save_to_sqlite(db_path: Path, user_dict: Dict[str, RimeEntry]) -> bool:
    """
    将词库字典保存到SQLite3数据库
    :param db_path: 数据库文件路径
    :param user_dict: 词库字典，格式为 {词条: RimeEntry}
    :return: 如果保存成功返回 True，否则返回 False
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rime_user_dict (
                    word TEXT PRIMARY KEY,
                    code TEXT,
                    weight TEXT
                )
            """)
            for word, entry in user_dict.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO rime_user_dict (word, code, weight)
                    VALUES (?, ?, ?)
                """, (word, entry.code, entry.weight))
            conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Error saving to SQLite: {e}")
        return False

def load_from_sqlite(db_path: Path) -> Dict[str, RimeEntry]:
    """
    从SQLite3数据库加载词库字典
    :param db_path: 数据库文件路径
    :return: 词库字典，格式为 {词条: RimeEntry}
    """
    user_dict: Dict[str, RimeEntry] = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word, code, weight FROM rime_user_dict")
            for row in cursor.fetchall():
                word, code, weight = row
                # 将数据库中的NULL值转换为None
                weight = weight if weight is not None else None
                user_dict[word] = RimeEntry(code, weight)
        return user_dict
    except sqlite3.Error as e:
        logger.error(f"Error loading from SQLite: {e}")
        return {}

# 示例用法
if __name__ == "__main__":
    file_path = Path("rime_user_dict.txt")
    db_path = Path("rime_user_dict.db")

    # 读取词库文件
    user_dict = read_rime_user_dict(file_path)
    logger.info("Current user dictionary:", user_dict)

    # 保存到SQLite数据库
    save_to_sqlite(db_path, user_dict)

    # 添加新词条
    new_entries = {
        "新词条1": RimeEntry("xin1ci2tiao3", "100"),
        "新词条2": RimeEntry("xin1ci2tiao3", None),
    }

    # 追加新词条到词库文件
    append_rime_user_dict(file_path, new_entries, add_date_comment=True)

    # 重新读取词库文件
    updated_user_dict = read_rime_user_dict(file_path)
    logger.info(f"Updated user dictionary: {updated_user_dict}")

    # 从SQLite数据库加载词库字典
    loaded_user_dict = load_from_sqlite(db_path)
    logger.info(f"Loaded user dictionary from SQLite: {loaded_user_dict}")