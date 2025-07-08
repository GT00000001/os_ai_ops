from typing import Dict, Any, List
from app.config import config
from app.utils.logger import get_logger


class ResponseGenerator:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.templates = self._load_response_templates()

    def _load_response_templates(self) -> Dict[str, List[str]]:
        """加载回复模板"""
        return {
            "check_metric": [
                "当前{metric}使用率为{value}%",
                "{metric}使用率是{value}%",
                "{metric}的当前值为{value}%"
            ],
            "detect_anomaly": [
                "系统运行正常，未检测到异常",
                "发现{count}个异常：{details}",
                "系统存在{severity}级异常：{details}"
            ],
            "fix_fault": [
                "故障已成功修复",
                "正在尝试修复{fault_type}故障",
                "修复操作已执行，请检查系统状态",
                "无法修复问题，请人工干预"
            ],
            "check_app_defect": [
                "应用运行正常，未发现缺陷",
                "发现{count}个应用缺陷：{details}",
                "检测到{severity}风险：{details}"
            ],
            "unknown": [
                "抱歉，我不理解您的问题，请换一种表达方式",
                "请您提供更多信息，以便我更好地回答您",
                "我无法处理这个请求，请尝试其他问题"
            ]
        }

    def generate_response(self, intent: str, entities: Dict[str, Any], data: Dict[str, Any]) -> str:
        """根据意图、实体和数据生成回复"""
        # 选择合适的模板组
        templates = self.templates.get(intent, self.templates["unknown"])

        # 根据数据选择具体模板
        if intent == "check_metric":
            template = self._select_metric_template(entities, templates)
        elif intent == "detect_anomaly":
            template = self._select_anomaly_template(data, templates)
        elif intent == "fix_fault":
            template = self._select_fault_template(data, templates)
        elif intent == "check_app_defect":
            template = self._select_defect_template(data, templates)
        else:
            template = templates[0]

        # 填充模板变量
        response = self._fill_template(template, entities, data)
        return response

    def _select_metric_template(self, entities: Dict[str, Any], templates: List[str]) -> str:
        """选择指标查询的回复模板"""
        if "duration" in entities:
            # 带时间范围的查询
            return next(
                (t for t in templates if "{duration}" in t),
                templates[0]
            )
        return templates[0]

    def _select_anomaly_template(self, data: Dict[str, Any], templates: List[str]) -> str:
        """选择异常检测的回复模板"""
        if data.get("anomaly_count", 0) == 0:
            return templates[0]
        elif data.get("anomaly_severity"):
            return next(
                (t for t in templates if "{severity}" in t),
                templates[1]
            )
        return templates[1]

    def _select_fault_template(self, data: Dict[str, Any], templates: List[str]) -> str:
        """选择故障修复的回复模板"""
        if data.get("success", False):
            return templates[0]
        elif data.get("fault_type"):
            return next(
                (t for t in templates if "{fault_type}" in t),
                templates[1]
            )
        elif data.get("executed", False):
            return templates[2]
        return templates[3]

    def _select_defect_template(self, data: Dict[str, Any], templates: List[str]) -> str:
        """选择应用缺陷检测的回复模板"""
        if data.get("defect_count", 0) == 0:
            return templates[0]
        elif data.get("highest_severity"):
            return next(
                (t for t in templates if "{severity}" in t),
                templates[2]
            )
        return templates[1]

    def _fill_template(self, template: str, entities: Dict[str, Any], data: Dict[str, Any]) -> str:
        """填充模板变量"""
        # 合并实体和数据
        context = {**entities, **data}

        # 特殊处理列表类型的数据
        if "details" in template and "anomalies" in data:
            context["details"] = ", ".join([
                f"{anomaly.get('description', '未知异常')}({anomaly.get('severity', '中等')}风险)"
                for anomaly in data["anomalies"]
            ])

        if "details" in template and "defects" in data:
            context["details"] = ", ".join([
                f"{defect.get('description', '应用缺陷')}({defect.get('severity', '中等')}风险)"
                for defect in data["defects"]
            ])

        # 填充模板
        try:
            return template.format(**context)
        except KeyError as e:
            self.logger.error(f"模板填充失败: {e}")
            return template

    def generate_unknown_response(self) -> str:
        """生成无法理解请求的回复"""
        from random import choice
        return choice(self.templates["unknown"])

    def generate_follow_up(self, intent: str, missing_entity: str) -> str:
        """生成追问回复"""
        follow_ups = {
            "metric": [
                "您想查询哪种指标？(CPU、内存、磁盘等)",
                "请问您想了解哪方面的系统信息？"
            ],
            "duration": [
                "您想查询多长时间范围内的数据？",
                "请问具体时间范围是多少？"
            ],
            "application": [
                "您想检查哪个应用？",
                "请问具体是哪个应用？"
            ]
        }

        return follow_ups.get(missing_entity, ["请提供更多信息"])[0]