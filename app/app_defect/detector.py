# 应用缺陷检测
# 功能：检测应用缺陷
# 核心组件：
# AppDefectDetector 类：应用缺陷检测主类
# scan_application()：扫描应用缺陷
# get_risk_level()：计算风险等级
# 检测内容：
# CVE 漏洞
# 配置错误
# 性能瓶颈
from app.app_defect.cve_scanner import CVEScanner
from app.app_defect.config_analyzer import ConfigAnalyzer


class AppDefectDetector:
    def __init__(self):
        self.cve_scanner = CVEScanner()
        self.config_analyzer = ConfigAnalyzer()

    def scan_application(self, app_name, version=None):
        """扫描应用缺陷"""
        defects = []

        # 检查CVE漏洞
        cve_issues = self.cve_scanner.scan(app_name, version)
        if cve_issues:
            defects.extend(cve_issues)

        # 检查配置问题
        config_issues = self.config_analyzer.analyze(app_name)
        if config_issues:
            defects.extend(config_issues)

        return defects

    def get_risk_level(self, defects):
        """计算风险等级"""
        if not defects:
            return "low"

        high_severity = [d for d in defects if d.get("severity", "") == "high"]
        if high_severity:
            return "high"

        medium_severity = [d for d in defects if d.get("severity", "") == "medium"]
        if medium_severity:
            return "medium"

        return "low"