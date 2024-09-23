import inspect
import logging
import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)


def setup_logger():
    log_level = config.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        # 从配置文件当中读取LOG_LEVEL
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logger()


def inspect_trace():
    traceback = inspect.trace()
    skip_first_frame = True
    for frame, _ in traceback:
        info = inspect.getframeinfo(frame)
        if skip_first_frame:
            skip_first_frame = False
            continue
        logger.error(f"File: {info.filename}, Line: {info.lineno}, Function: {info.function}")
