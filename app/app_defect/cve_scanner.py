# CVE漏洞扫描
# 功能：扫描已知 CVE 漏洞
# 核心方法：
# scan()：检查应用版本是否存在已知漏洞
# 技术实现：
# 查询本地 CVE 数据库（如 NVD 镜像）
# 调用第三方 API（如 Vulners、CVE Search）

import requests
from app.config import config
from app.utils.logger import get_logger


class CVEScanner:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.api_url = "https://cve.circl.lu/api/search"  # 示例API

    def scan(self, app_name, version=None):
        """扫描应用CVE漏洞"""
        try:
            if version:
                search_query = f"{app_name} {version}"
            else:
                search_query = app_name

            response = requests.get(f"{self.api_url}/{search_query}")
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch CVE data: {response.text}")
                return []

            cves = response.json()
            if not cves:
                return []

            # 过滤高风险漏洞
            high_risk_cves = []
            for cve in cves:
                if cve.get("cvss", 0) >= 7.0:
                    high_risk_cves.append({
                        "cve_id": cve["id"],
                        "cvss": cve["cvss"],
                        "summary": cve["summary"],
                        "published": cve["Published"],
                        "severity": "high" if cve["cvss"] >= 7.0 else "medium"
                    })

            return high_risk_cves
        except Exception as e:
            self.logger.error(f"Failed to scan CVE: {e}")
            return []