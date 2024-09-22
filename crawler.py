import json

import requests

from logger_config import setup_logger

# 配置日志系统
logger = setup_logger()

def fetch_new_sentences(api_url: str) -> list:
    """
    从API获取新句子列表
    :param api_url: API的URL
    :param params: 请求参数
    :param headers: 请求头
    :return: 新句子列表
    """
    # 发送第一次请求以获取总页数
    params = {
        "tab": "top",
        "sub_tab": "today",
        "version": 1
    }
    
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,en-GB;q=0.8,zh-CN;q=0.7,zh;q=0.6",
        "authorization": "undefined",
        "cache-control": "no-cache",
        "dnt": "1",
        "origin": "https://rebang.today",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://rebang.today/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    response = requests.get(api_url, params=params, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()

        # 提取总页数
        total_page = data['data']['total_page']
        list_data = json.loads(data['data']['list'])

        if total_page > 1:
            # 遍历所有页
            for page in range(1, total_page + 1):
                params['page'] = page
                response = requests.get(api_url, params=params, headers=headers)

                # 检查请求是否成功
                if response.status_code == 200:
                    # 解析JSON数据
                    data = response.json()

                    # 提取list字段并解析为Python列表
                    list_data.extend(json.loads(data['data']['list']))
                else:
                    logger.error(f"请求第 {page} 页失败，状态码: {response.status_code}")
        return [item['title'] for item in list_data]
    else:
        logger.error(f"请求失败，状态码: {response.status_code}")
        return []

# 示例用法
if __name__ == "__main__":
    api_url = "https://api.rebang.today/v1/items"


    new_sentences = fetch_new_sentences(api_url)
    print(new_sentences)