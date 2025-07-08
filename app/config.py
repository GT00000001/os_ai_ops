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

    # NLP 模型训练配置
    NLP_MODEL_NAME = "bert-base-chinese"  # 预训练模型名称
    NLP_TRAINING_DATA_PATH = os.path.join(BASE_DIR, "data", "nlp_training_data.txt")  # 训练数据文件路径
    NLP_TRAINING_OUTPUT_DIR = os.path.join(BASE_DIR, "models", "nlp_training_output")  # 训练输出目录
    NLP_NUM_TRAIN_EPOCHS = 3  # 训练轮数
    NLP_PER_DEVICE_TRAIN_BATCH_SIZE = 16  # 每个设备的训练批次大小
    NLP_PER_DEVICE_EVAL_BATCH_SIZE = 16  # 每个设备的评估批次大小
    NLP_WARMUP_STEPS = 500  # 热身步数
    NLP_WEIGHT_DECAY = 0.01  # 权重衰减
    NLP_LOGGING_DIR = os.path.join(BASE_DIR, "logs", "nlp_logs")  # 日志目录
    NLP_LOGGING_STEPS = 100  # 日志记录步数
    NLP_EVAL_STEPS = 500  # 评估步数
    NLP_SAVE_STEPS = 500  # 保存步数

    # 异常检测模型训练配置
    ANOMALY_TRAINING_DATA_DIR = os.path.join(BASE_DIR, "data", "anomaly_training_data")  # 异常检测训练数据目录


config = Config()