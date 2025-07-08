# 模型评估指标
# 功能：评估模型性能
# 核心组件：
# ModelEvaluator 类：模型评估主类
# evaluate_anomaly_detector()：评估异常检测模型
# evaluate_nlp_processor()：评估 NLP 处理器
# 评估指标：
# 准确率、精确率、召回率、F1 分数
# 误报率、漏报率
class ModelEvaluator:
    def __init__(self, detector):
        self.detector = detector  # 传入异常检测模型

    def evaluate(self, test_data):
        """评估模型：准确率、误报率、召回率等"""
        true_labels = [1 if "anomaly" in d else 0 for d in test_data]
        pred_labels = [1 if self.detector.detect(d) >= 5 else 0 for d in test_data]

        tp = sum(1 for t, p in zip(true_labels, pred_labels) if t == 1 and p == 1)
        fp = sum(1 for t, p in zip(true_labels, pred_labels) if t == 0 and p == 1)
        tn = sum(1 for t, p in zip(true_labels, pred_labels) if t == 0 and p == 0)
        fn = sum(1 for t, p in zip(true_labels, pred_labels) if t == 1 and p == 0)

        accuracy = (tp + tn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) != 0 else 0
        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) != 0 else 0

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "false_positive_rate": fpr,
        }