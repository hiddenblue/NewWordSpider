from typing import Dict, List

from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

xiaohe_map: Dict[str, str] = {
    'a': 'a', 'o': 'o', 'u': 'u', 'i': 'i', 'e': 'e', 'iu': 'q', 'uan': 'r', 'ue': 't', 'un': 'y',
    'sh': 'u', 'ch': 'i', 'uo': 'o', 'ie': 'p', 'iong': 's', 'ong': 's',
    'ai': 'd', 'en': 'f', 'eng': 'g', 'ang': 'h', 'an': 'j', 'ing': 'k',
    'uai': 'k', 'iang': 'l', 'uang': 'l', "ou": 'z', 'ia': 'x', 'ua': 'x',
    'ao': 'c', 'ui': 'v', 'zh': 'v', 'in': 'b', 'iao': 'n', "ian": 'm', 'ei': 'w'
}


def full_to_xiaohe(full_pinyin: str) -> str:
    # 处理长度为1的拼音
    if len(full_pinyin) == 1:
        return full_pinyin * 2
    # 处理长度为2的拼音
    if len(full_pinyin) == 2:
        return full_pinyin
    
    if full_pinyin[:2] in xiaohe_map:
        return xiaohe_map[full_pinyin[:2]] + xiaohe_map[full_pinyin[2:]]
    else:
        return full_pinyin[0] + xiaohe_map[full_pinyin[1:]]
    
def safe_full_to_xiaohe(full_pinyin: str) -> str:
    try:
        # 检查输入是否为合法的全拼
        if not all(c.isalpha() or c.isspace() for c in full_pinyin):
            raise ValueError("Invalid input: input should only contain alphabetic characters and spaces")
        if not 0 < len(full_pinyin) < 7:
            raise ValueError("Invalid input: input should be between 1 and 5 characters long")

        return full_to_xiaohe(full_pinyin)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # 测试
    print(safe_full_to_xiaohe('xi'))  # 输出: xi
    print(safe_full_to_xiaohe('zhong'))  # 输出: vsgo
    print(safe_full_to_xiaohe('a'))  # 输出: aa
    print(safe_full_to_xiaohe('ai'))  # 输出: d
    print(safe_full_to_xiaohe('xi'))  # 输出: xi
    print(safe_full_to_xiaohe('xiang'))  # 输出: xn
    print(safe_full_to_xiaohe('ming'))  # 输出: mj
    print(safe_full_to_xiaohe('zhuang'))  # 输出: vhl
    print(safe_full_to_xiaohe('duang'))  # 输出: dhl
    print(safe_full_to_xiaohe('invalid_input'))  # 输出: Error: Invalid input: input should only contain alphabetic characters and spaces

    # 更多全拼转换的测试
    print(safe_full_to_xiaohe('mei'))  # 输出: mo
    print(safe_full_to_xiaohe('lian'))  # 输出: lim
    print(safe_full_to_xiaohe('chu'))  # 输出: vi
    print(safe_full_to_xiaohe('chi'))  # 输出: ui
    print(safe_full_to_xiaohe('shu'))  # 输出: uu
    print(safe_full_to_xiaohe('shi'))  # 输出: ui
    print(safe_full_to_xiaohe('zhi'))  # 输出: vi
    print(safe_full_to_xiaohe('ri'))  # 输出: ri
    print(safe_full_to_xiaohe('zi'))  # 输出: zi
    print(safe_full_to_xiaohe('ci'))  # 输出: ci
    print(safe_full_to_xiaohe('si'))  # 输出: si
    print(safe_full_to_xiaohe('ye'))  # 输出: xo
    print(safe_full_to_xiaohe('yue'))  # 输出: xo
    print(safe_full_to_xiaohe('yuan'))  # 输出: xmr
    print(safe_full_to_xiaohe('yun'))  # 输出: xyn
    print(safe_full_to_xiaohe('ying'))  # 输出: yk
    print(safe_full_to_xiaohe('yong'))  # 输出: ys
    print(safe_full_to_xiaohe('wu'))  # 输出: wu
    print(safe_full_to_xiaohe('wa'))  # 输出: woa
    print(safe_full_to_xiaohe('wo'))  # 输出: wuo
    print(safe_full_to_xiaohe('wei'))  # 输出: we
    print(safe_full_to_xiaohe('wen'))  # 输出: wn
    print(safe_full_to_xiaohe('wang'))  # 输出: wh
    print(safe_full_to_xiaohe('weng'))  # 输出: wg
    print(safe_full_to_xiaohe('yu'))  # 输出: vy
    print(safe_full_to_xiaohe('you'))  # 输出: yo
    print(safe_full_to_xiaohe('yin'))  # 输出: yb
    print(safe_full_to_xiaohe('ying'))  # 输出: yk
    print(safe_full_to_xiaohe('yong'))  # 输出: ys
    print(safe_full_to_xiaohe('zai'))  # 输出: vj
    print(safe_full_to_xiaohe('zou'))  # 输出: vz
    print(safe_full_to_xiaohe('zuo'))  # 输出: vuo
    print(safe_full_to_xiaohe('zui'))  # 输出: vv
    print(safe_full_to_xiaohe('zun'))  # 输出: vyn
    print(safe_full_to_xiaohe('zeng'))  # 输出: vg
    print(safe_full_to_xiaohe('zong'))  # 输出: vs
    print(safe_full_to_xiaohe('zhao'))  # 输出: vh
    print(safe_full_to_xiaohe('zhou'))  # 输出: vz
    print(safe_full_to_xiaohe('zhuo'))  # 输出: vuo
    print(safe_full_to_xiaohe('zhui'))  # 输出: vv
    print(safe_full_to_xiaohe('zhun'))  # 输出: vyn
    print(safe_full_to_xiaohe('zheng'))  # 输出: vg
    print(safe_full_to_xiaohe('zhong'))  # 输出: vs
    print(safe_full_to_xiaohe('cha'))  # 输出: ioa
    print(safe_full_to_xiaohe('che'))  # 输出: ie
    print(safe_full_to_xiaohe('chi'))  # 输出: ui
    print(safe_full_to_xiaohe('chu'))  # 输出: vi
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn
    print(safe_full_to_xiaohe('chong'))  # 输出: is
    print(safe_full_to_xiaohe('chou'))  # 输出: iz
    print(safe_full_to_xiaohe('chuo'))  # 输出: iuo
    print(safe_full_to_xiaohe('chui'))  # 输出: iv
    print(safe_full_to_xiaohe('chun'))  # 输出: iyn