# 模型训练
# 功能：模型训练与优化
# 核心方法：
# prepare_training_data()：准备训练数据
# cross_validate()：交叉验证模型
# optimize_hyperparameters()：超参数调优
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, f1_score
from app.anomaly.detector import AnomalyDetector
from app.config import config
from app.utils.logger import get_logger


class AnomalyTrainer:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.detector = AnomalyDetector()

    def prepare_training_data(self, metrics_data, anomaly_labels):
        """准备训练数据"""
        features = self._extract_features(metrics_data)
        X_train, X_test, y_train, y_test = train_test_split(
            features, anomaly_labels, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    def _extract_features(self, metrics_data):
        """从指标数据中提取特征"""
        features = []
        for metrics in metrics_data:
            feature = [
                metrics.get("cpu_usage", 0),
                metrics.get("memory_usage", 0),
                metrics.get("disk_usage", 0),
                metrics.get("network", {}).get("bytes_recv", 0),
                metrics.get("network", {}).get("bytes_sent", 0)
            ]
            features.append(feature)
        return np.array(features)

    def optimize_hyperparameters(self, X_train, y_train):
        """优化模型超参数"""
        param_grid = {
            'n_estimators': [50, 100, 200],
            'contamination': [0.05, 0.1, 0.15],
            'max_samples': ['auto', 0.8, 0.9]
        }

        scoring = make_scorer(f1_score, pos_label=-1)  # 异常标签为-1

        grid_search = GridSearchCV(
            estimator=self.detector.model,
            param_grid=param_grid,
            scoring=scoring,
            cv=3,
            n_jobs=-1
        )

        grid_search.fit(X_train, y_train)
        self.logger.info(f"Best parameters: {grid_search.best_params_}")
        self.logger.info(f"Best F1 score: {grid_search.best_score_}")

        # 更新检测器模型为最优模型
        self.detector.model = grid_search.best_estimator_
        return grid_search.best_params_

    def cross_validate(self, X, y, cv=5):
        """交叉验证模型"""
        from sklearn.model_selection import cross_val_score

        scores = cross_val_score(
            self.detector.model, X, y, cv=cv, scoring=make_scorer(f1_score, pos_label=-1)
        )

        self.logger.info(f"Cross-validation scores: {scores}")
        self.logger.info(f"Average F1 score: {np.mean(scores)}")
        return np.mean(scores)

    def train(self, metrics_data, anomaly_labels):
        """训练异常检测模型"""
        X_train, X_test, y_train, y_test = self.prepare_training_data(
            metrics_data, anomaly_labels
        )

        # 优化超参数
        best_params = self.optimize_hyperparameters(X_train, y_train)

        # 训练最终模型
        self.detector.model.fit(X_train)

        # 评估模型
        y_pred = self.detector.model.predict(X_test)
        f1 = f1_score(y_test, y_pred, pos_label=-1)
        self.logger.info(f"Final model F1 score: {f1}")

        # 保存模型
        self.detector.save_model()

        return {
            "best_params": best_params,
            "f1_score": f1
        }