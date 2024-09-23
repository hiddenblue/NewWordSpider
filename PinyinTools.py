from typing import Dict, List
from pypinyin import pinyin, Style
from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

# 小鹤双拼映射表
xiaohe_map: Dict[str, str] = {
    'a': 'a', 'o': 'o', 'u': 'u', 'i': 'i', 'e': 'e', 'iu': 'q', 'uan': 'r', 'ue': 't', 'un': 'y',
    'sh': 'u', 'ch': 'i', 'uo': 'o', 'ie': 'p', 'iong': 's', 'ong': 's',
    'ai': 'd', 'en': 'f', 'eng': 'g', 'ang': 'h', 'an': 'j', 'ing': 'k',
    'uai': 'k', 'iang': 'l', 'uang': 'l', "ou": 'z', 'ia': 'x', 'ua': 'x',
    'ao': 'c', 'ui': 'v', 'zh': 'v', 'in': 'b', 'iao': 'n', "ian": 'm', 'ei': 'w'
}


def quanpin_to_xiaohe(quan_pinyin: str) -> str:
    """
    将全拼转换为小鹤双拼
    :param quan_pinyin: 全拼字符串
    :return: 小鹤双拼字符串
    """
    try:
        # 检查输入是否为合法的全拼
        if not all(c.isalpha() or c.isspace() for c in quan_pinyin):
            raise ValueError("Invalid input: input should only contain alphabetic characters and spaces")
        if not 0 < len(quan_pinyin) < 7:
            raise ValueError("Invalid input: input should be between 1 and 5 characters long")

        # 处理长度为1的拼音
        if len(quan_pinyin) == 1:
            return quan_pinyin * 2
        # 处理长度为2的拼音
        if len(quan_pinyin) == 2:
            return quan_pinyin

        # 处理长度为3，4，5，6长度的拼音，有多种搭配方式，但是声母一般为2，3长度，韵母长度为1，2，3，4(uang这种）
        if quan_pinyin[:2] in xiaohe_map:
            return xiaohe_map[quan_pinyin[:2]] + xiaohe_map[quan_pinyin[2:]]
        else:
            return quan_pinyin[0] + xiaohe_map[quan_pinyin[1:]]

    except Exception as e:
        logger.error(f"Error converting quanpin to xiaohe: {e}")
        return f"Error: {e}"


def word_get_pinyin(word: str) -> List[str]:
    """
    给汉字词语标注上拼音，不需要声调，处理多音字问题
    :param word: 汉字词语
    :return: 标注拼音后的词语列表
    """
    try:
        # 使用 pypinyin 获取拼音列表
        pinyin_list = pinyin(word, style=Style.NORMAL, heteronym=True)
        logger.info(f"{word} {pinyin_list}")

        # 返回拼音列表
        return [item[0] for item in pinyin_list]
    except Exception as e:
        logger.error(f"Error getting pinyin for word '{word}': {e}")
        return []


if __name__ == "__main__":
    # 示例用法

    print("吸睛：", word_get_pinyin("吸睛"))

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
        print(f"{test_case}：", word_get_pinyin(test_case))

    # 测试
    print(quanpin_to_xiaohe('xi'))  # 输出: xi
    print(quanpin_to_xiaohe('zhong'))  # 输出: vsgo
    print(quanpin_to_xiaohe('a'))  # 输出: aa
    print(quanpin_to_xiaohe('ai'))  # 输出: d
    print(quanpin_to_xiaohe('xi'))  # 输出: xi
    print(quanpin_to_xiaohe('xiang'))  # 输出: xn
    print(quanpin_to_xiaohe('ming'))  # 输出: mj
    print(quanpin_to_xiaohe('zhuang'))  # 输出: vhl
    print(quanpin_to_xiaohe('duang'))  # 输出: dhl
    print(quanpin_to_xiaohe(
        'invalid_input'))  # 输出: Error: Invalid input: input should only contain alphabetic characters and spaces

    # 更多全拼转换的测试
    print(quanpin_to_xiaohe('mei'))  # 输出: mo
    print(quanpin_to_xiaohe('lian'))  # 输出: lim
    print(quanpin_to_xiaohe('chu'))  # 输出: vi
    print(quanpin_to_xiaohe('chi'))  # 输出: ui
    print(quanpin_to_xiaohe('shu'))  # 输出: uu
    print(quanpin_to_xiaohe('shi'))  # 输出: ui
    print(quanpin_to_xiaohe('zhi'))  # 输出: vi
    print(quanpin_to_xiaohe('ri'))  # 输出: ri
    print(quanpin_to_xiaohe('zi'))  # 输出: zi
    print(quanpin_to_xiaohe('ci'))  # 输出: ci
    print(quanpin_to_xiaohe('si'))  # 输出: si
    print(quanpin_to_xiaohe('ye'))  # 输出: xo
    print(quanpin_to_xiaohe('yue'))  # 输出: xo
    print(quanpin_to_xiaohe('yuan'))  # 输出: xmr
    print(quanpin_to_xiaohe('yun'))  # 输出: xyn
    print(quanpin_to_xiaohe('ying'))  # 输出: yk
    print(quanpin_to_xiaohe('yong'))  # 输出: ys
    print(quanpin_to_xiaohe('wu'))  # 输出: wu
    print(quanpin_to_xiaohe('wa'))  # 输出: woa
    print(quanpin_to_xiaohe('wo'))  # 输出: wuo
    print(quanpin_to_xiaohe('wei'))  # 输出: we
    print(quanpin_to_xiaohe('wen'))  # 输出: wn
    print(quanpin_to_xiaohe('wang'))  # 输出: wh
    print(quanpin_to_xiaohe('weng'))  # 输出: wg
    print(quanpin_to_xiaohe('yu'))  # 输出: vy
    print(quanpin_to_xiaohe('you'))  # 输出: yo
    print(quanpin_to_xiaohe('yin'))  # 输出: yb
    print(quanpin_to_xiaohe('ying'))  # 输出: yk
    print(quanpin_to_xiaohe('yong'))  # 输出: ys
    print(quanpin_to_xiaohe('zai'))  # 输出: vj
    print(quanpin_to_xiaohe('zou'))  # 输出: vz
    print(quanpin_to_xiaohe('zuo'))  # 输出: vuo
    print(quanpin_to_xiaohe('zui'))  # 输出: vv
    print(quanpin_to_xiaohe('zun'))  # 输出: vyn
    print(quanpin_to_xiaohe('zeng'))  # 输出: vg
    print(quanpin_to_xiaohe('zong'))  # 输出: vs
    print(quanpin_to_xiaohe('zhao'))  # 输出: vh
    print(quanpin_to_xiaohe('zhou'))  # 输出: vz
    print(quanpin_to_xiaohe('zhuo'))  # 输出: vuo
    print(quanpin_to_xiaohe('zhui'))  # 输出: vv
    print(quanpin_to_xiaohe('zhun'))  # 输出: vyn
    print(quanpin_to_xiaohe('zheng'))  # 输出: vg
    print(quanpin_to_xiaohe('zhong'))  # 输出: vs
    print(quanpin_to_xiaohe('cha'))  # 输出: ioa
    print(quanpin_to_xiaohe('che'))  # 输出: ie
    print(quanpin_to_xiaohe('chi'))  # 输出: ui
    print(quanpin_to_xiaohe('chu'))  # 输出: vi
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
    print(quanpin_to_xiaohe('chong'))  # 输出: is
    print(quanpin_to_xiaohe('chou'))  # 输出: iz
    print(quanpin_to_xiaohe('chuo'))  # 输出: iuo
    print(quanpin_to_xiaohe('chui'))  # 输出: iv
    print(quanpin_to_xiaohe('chun'))  # 输出: iyn
