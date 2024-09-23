import sqlite3
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import Dict
from logger_config import setup_logger

# 定义命名元组
RimeEntry = namedtuple("RimeEntry", ["code", "weight"])

logger = setup_logger()


class RimeFileHandler:
    """
    处理Rime用户词库文件的类
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_dict(self) -> Dict[str, RimeEntry]:
        """
        读取Rime用户词库文件
        :return: 词库字典，格式为 {词条: RimeEntry}
        """
        user_dict: Dict[str, RimeEntry] = {}
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
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
            logger.error(f"File not found: {self.file_path}")
            return {}
        except IOError as e:
            logger.error(f"Error reading file: {e}")
            return {}
        return user_dict

    def write_dict(self, user_dict: Dict[str, RimeEntry]) -> bool:
        """
        写入Rime用户词库文件
        :param user_dict: 词库字典，格式为 {词条: RimeEntry}
        :return: 如果写入成功返回 True，否则返回 False
        """
        try:
            with self.file_path.open("w", encoding="utf-8") as f:
                for word, entry in user_dict.items():
                    if entry.weight:
                        f.write(f"{word}\t{entry.code}\t{entry.weight}\n")
                    else:
                        f.write(f"{word}\t{entry.code}\n")
            return True
        except IOError as e:
            logger.error(f"Error writing file: {e}")
            return False

    def append_dict(self, new_entries: Dict[str, RimeEntry], add_date_comment: bool = False) -> bool:
        """
        追加新行到Rime用户词库文件
        :param new_entries: 新词条字典，格式为 {词条: RimeEntry}
        :param add_date_comment: 是否添加日期注释
        :return: 如果追加成功返回 True，否则返回 False
        """
        try:
            with self.file_path.open("a", encoding="utf-8") as f:
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


class RimeSQLiteHandler:
    """
    处理Rime用户词库SQLite数据库的类
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def save_sqlite(self, user_dict: Dict[str, RimeEntry]) -> bool:
        """
        将词库字典保存到SQLite3数据库
        :param user_dict: 词库字典，格式为 {词条: RimeEntry}
        :return: 如果保存成功返回 True，否则返回 False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
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

    def load_sqlite(self) -> Dict[str, RimeEntry]:
        """
        从SQLite3数据库加载词库字典
        :return: 词库字典，格式为 {词条: RimeEntry}
        """
        user_dict: Dict[str, RimeEntry] = {}
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT word, code, weight FROM rime_user_dict")
                for row in cursor.fetchall():
                    word, code, weight = row
                    # 将数据库中的NULL值转换为None
                    weight = weight if weight is not None else None
                    user_dict[word] = RimeEntry(code, weight)
        except sqlite3.Error as e:
            logger.error(f"Error loading from SQLite: {e}")
            return {}
        return user_dict


# 示例用法
if __name__ == "__main__":
    file_path = Path("rime_user_dict.txt")
    db_path = Path("rime_user_dict.db")

    file_handler = RimeFileHandler(file_path)
    sqlite_handler = RimeSQLiteHandler(db_path)

    # 读取词库文件
    user_dict = file_handler.read_dict()
    logger.info(f"Current user dictionary: {user_dict}")

    # 保存到SQLite数据库
    sqlite_handler.save_sqlite(user_dict)

    # 添加新词条
    new_entries = {
        "新词条1": RimeEntry("xin1ci2tiao3", "100"),
        "新词条2": RimeEntry("xin1ci2tiao3", None),
    }

    # 追加新词条到词库文件
    file_handler.append_dict(new_entries, add_date_comment=True)

    # 重新读取词库文件
    updated_user_dict = file_handler.read_dict()
    logger.info(f"Updated user dictionary: {updated_user_dict}")

    # 从SQLite数据库加载词库字典
    loaded_user_dict = sqlite_handler.load_sqlite()
    logger.info(f"Loaded user dictionary from SQLite: {loaded_user_dict}")
