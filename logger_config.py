import logging
import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

import inspect

import logging
import inspect

class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # 获取当前函数和模块名称
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals['__name__']
        func_name = frame.f_code.co_name

        # 将模块和函数名称添加到日志消息中
        return f"[{module_name}.{func_name}] {msg}", kwargs

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

    # 返回自定义的日志记录器
    return CustomLoggerAdapter(logging.getLogger(__name__), {})