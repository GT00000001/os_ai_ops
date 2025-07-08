# 日志配置
# 功能：配置系统日志
# 日志级别：DEBUG、INFO、WARNING、ERROR、CRITICAL
# 日志输出：
# 控制台输出
# 文件输出
# 远程日志服务（可选）

import logging
from app.config import config
import os

def get_logger(name):
    """获取配置好的logger实例"""
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    # ===== 新增代码：确保日志目录存在 =====
    log_dir = os.path.dirname(config.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    # ===================================

    # 创建文件处理器
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(config.LOG_LEVEL)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.LOG_LEVEL)

    # 创建格式化器并添加到处理器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 清除旧的处理器并添加新的处理器
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger