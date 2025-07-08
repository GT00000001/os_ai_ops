import os


class Config:
    DEBUG = False
    LOG_LEVEL = "INFO"

    # 获取项目根目录（假设Config类位于app/utils/config.py中）
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LOG_FILE = os.path.join(BASE_DIR, "logs", "aiops.log")

    # 模型路径
    ANOMALY_MODEL_PATH = os.path.join(BASE_DIR, "models", "anomaly_model.joblib")
    NLP_MODEL_PATH = os.path.join(BASE_DIR, "models", "nlp_model")

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