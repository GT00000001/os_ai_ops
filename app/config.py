# 全局配置
# 功能：集中管理系统配置参数
# 核心配置项：
# 日志级别与路径
# 模型存储路径
# 数据采集频率
# 日志文件路径
# 安全白名单（允许执行的命令、脚本）
# 设计模式：单例模式，全局共享配置实例
import os

class Config:
    DEBUG = False
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/aiops.log"

    # 模型路径
    ANOMALY_MODEL_PATH = "models/anomaly_model.joblib"
    NLP_MODEL_PATH = "models/nlp_model"

    # 数据采集配置
    COLLECT_INTERVAL = 30  # 秒
    LOG_PATHS = {
        "system": "/var/log/syslog",
        "application": "/var/log/app.log"
    }

    # 安全配置
    ALLOWED_REMOTE_COMMANDS = ["restart", "stop", "start"]
    SCRIPT_WHITELIST = ["fix_cpu.sh", "restart_service.sh"]


config = Config()