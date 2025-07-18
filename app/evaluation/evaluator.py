# 模型评估指标
# 功能：评估模型性能
# 核心组件：
# ModelEvaluator 类：模型评估主类
# 评估指标：
# 准确率、精确率、召回率、F1 分数
# 误报率、漏报率
# 修复成功率、算法执行效率、分析效率
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from app.anomaly.detector import AnomalyDetector
from app.fault.healer import FaultHealer
from app.evaluation.test_cases import generate_test_data

class ModelEvaluator:
    def __init__(self):
        self.detector = AnomalyDetector()
        self.healer = FaultHealer()
        self.test_data, self.true_labels = generate_test_data()
        try:
            self.pred_labels = [1 if self.detector.detect(data) else 0 for data in self.test_data]
        except Exception as e:
            self.pred_labels = []
            print(f"预测模块出错: {e}")

    def evaluate(self) -> dict:
        """评估模型：准确率、误报率、召回率等"""
        if not self.pred_labels == []:
            accuracy = accuracy_score(self.true_labels, self.pred_labels)
            precision = precision_score(self.true_labels, self.pred_labels)
            recall = recall_score(self.true_labels, self.pred_labels)
            f1 = f1_score(self.true_labels, self.pred_labels)
            false_positive_rate = self._calculate_false_positive_rate()
            false_negative_rate = self._calculate_false_negative_rate()
        else:
            accuracy = 0.0
            precision = 0.0
            recall = 0.0
            f1 = 0.0
            false_positive_rate = 0.0
            false_negative_rate = 0.0

        # 计算修复成功率、算法执行效率和分析效率
        total_faults = 0
        successful_fixes = 0
        total_execution_time = 0
        total_analysis_time = 0

        # for data in self.test_data:
        #     if self.detector.detect(data):
        #         total_faults += 1
        #         is_fixed, execution_time, analysis_time = self.healer.heal(data)
        #         if is_fixed:
        #             successful_fixes += 1
        #         total_execution_time += execution_time
        #         total_analysis_time += analysis_time
        #
        # if total_faults > 0:
        #     repair_success_rate = successful_fixes / total_faults
        #     average_execution_time = total_execution_time / total_faults
        #     average_analysis_time = total_analysis_time / total_faults
        # else:
        #     repair_success_rate = 0
        #     average_execution_time = 0
        #     average_analysis_time = 0

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            # "f1_score": f1,
            "false_positive_rate": false_positive_rate,
            "false_negative_rate": false_negative_rate,
            # "repair_success_rate": repair_success_rate,
            # "average_execution_time": average_execution_time,
            # "average_analysis_time": average_analysis_time
        }

    def _calculate_false_positive_rate(self):
        """计算误报率"""
        fp = sum([1 for t, p in zip(self.true_labels, self.pred_labels) if t == 0 and p == 1])
        tn = sum([1 for t, p in zip(self.true_labels, self.pred_labels) if t == 0 and p == 0])
        return fp / (fp + tn) if (fp + tn) != 0 else 0

    def _calculate_false_negative_rate(self):
        """计算漏报率"""
        fn = sum([1 for t, p in zip(self.true_labels, self.pred_labels) if t == 1 and p == 0])
        tp = sum([1 for t, p in zip(self.true_labels, self.pred_labels) if t == 1 and p == 1])
        return fn / (fn + tp) if (fn + tp) != 0 else 0

