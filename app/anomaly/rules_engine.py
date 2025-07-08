# 基于规则的检测
# 功能：基于规则的异常检测
# 核心方法：
# check_thresholds()：检查指标阈值
# check_patterns()：检查异常模式（如突然激增）
# 规则示例：
# CPU 使用率 > 90% 持续 5 分钟
# 内存泄漏检测（持续增长）

from app.config import config
from app.utils.logger import get_logger


class RulesEngine:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.rules = self._load_rules()

    def _load_rules(self):
        """加载异常检测规则"""
        return [
            {
                "name": "high_cpu",
                "condition": lambda metrics: metrics.get("cpu_usage", 0) > 90,
                "severity": "high",
                "description": "CPU使用率过高"
            },
            {
                "name": "high_memory",
                "condition": lambda metrics: metrics.get("memory_usage", 0) > 90,
                "severity": "high",
                "description": "内存使用率过高"
            },
            {
                "name": "low_disk_space",
                "condition": lambda metrics: metrics.get("disk_usage", 0) > 90,
                "severity": "high",
                "description": "磁盘空间不足"
            },
            {
                "name": "network_spike",
                "condition": lambda metrics:
                metrics.get("network", {}).get("bytes_recv", 0) > 10000000 or
                metrics.get("network", {}).get("bytes_sent", 0) > 10000000,
                "severity": "medium",
                "description": "网络流量异常"
            }
        ]

    def check_rules(self, metrics):
        """检查指标是否违反规则"""
        violations = []
        for rule in self.rules:
            if rule["condition"](metrics):
                violations.append({
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "metrics": metrics
                })

        return violations