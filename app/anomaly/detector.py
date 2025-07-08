# 异常检测模型
# 功能：检测系统异常
# 核心组件：
# AnomalyDetector 类：异常检测主类
# load_model()：加载预训练模型
# train()：训练新模型
# detect()：检测异常
# get_anomaly_score()：获取异常分数
# 技术实现：
# 无监督学习：Isolation Forest、One-Class SVM
# 有监督学习：随机森林、深度学习模型
import numpy as np
from sklearn.ensemble import IsolationForest
from joblib import dump, load
from app.config import config


class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.model_path = config.ANOMALY_MODEL_PATH
        self.load_model()

    def load_model(self):
        """加载预训练模型或创建新模型"""
        try:
            self.model = load(self.model_path)
        except FileNotFoundError:
            self.model = IsolationForest(contamination=0.1, random_state=42)

    def train(self, data):
        """训练异常检测模型"""
        features = self._preprocess(data)
        self.model.fit(features)
        self.save_model()

    def save_model(self):
        """保存模型到文件"""
        dump(self.model, self.model_path)

    def detect(self, metrics):
        """检测是否存在异常"""
        features = self._preprocess([metrics])
        prediction = self.model.predict(features)
        return prediction[0] == -1  # -1表示异常，1表示正常

    def get_anomaly_score(self, metrics):
        """获取异常分数（越接近1越异常）"""
        features = self._preprocess([metrics])
        return -self.model.decision_function(features)[0]

    def _preprocess(self, data):
        """将数据转换为模型可用的特征"""
        # 提取关键指标并标准化
        features = []
        for item in data:
            feature = [
                item.get("cpu_usage", 0),
                item.get("memory_usage", 0),
                item.get("disk_usage", 0)
            ]
            features.append(feature)
        return np.array(features)