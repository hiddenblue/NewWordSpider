from typing import List
from pypinyin import pinyin, Style

from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

def add_pinyin_to_words(word: str) -> List[str]:
    """
    给汉字词语标注上拼音，不需要声调，处理多音字问题
    :param word: 汉字词语
    :return: 标注拼音后的词语列表
    """
    pinyin_list = pinyin(word, style=Style.NORMAL, heteronym=True)
    logger.info(f"{word} {pinyin_list}")
    
    return [item[0] for item in pinyin_list]

if __name__ == '__main__':
    # 示例用法

    print("吸睛：", add_pinyin_to_words("吸睛"))

    # 测试用例生成
    test_cases = [
        "吸睛",
        "创新",
        "技术",
        "智能",
        "开发",
        "项目",
        "编程",
        "算法",
        "数据",
        "分析",
        "网络",
        "安全",
        "架构",
        "设计",
        "优化",
        "测试",
        "运维",
        "部署",
        "云端",
        "应用",
        "框架",
        "库",
        "工具",
        "平台",
        "接口",
        "协议",
        "数据库",
        "模型",
        "预测",
        "学习",
        "研究",
        "教育",
        "文档",
        "指南",
        "教程",
        "示例",
        "案例",
        "实践",
        "解决方案",
        "性能",
        "效率",
        "兼容性",
        "用户体验",
        "界面",
        "交互"
    ]

    # 打印测试用例
    for test_case in test_cases:
        print(f"{test_case}：", add_pinyin_to_words(test_case))
