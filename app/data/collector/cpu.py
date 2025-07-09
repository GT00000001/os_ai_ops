import psutil
from .base import Collector
from typing import List, Dict, Any
import time


class CPUCollector(Collector):
    """CPU 与内存使用情况采集器"""

    def collect(self) -> dict:
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5, percpu=False)
            cpu_percpu = psutil.cpu_percent(interval=None, percpu=True)
            virtual = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "cpu_percent_overall": cpu_percent,
                "cpu_percent_per_core": cpu_percpu,
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "cpu_count_physical": psutil.cpu_count(logical=False),
                "memory_total": virtual.total,
                "memory_available": virtual.available,
                "memory_used": virtual.used,
                "memory_percent": virtual.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_percent": swap.percent,
            }
        except Exception as e:
            return {"error": f"CPUCollector failed: {e}"}

    def top(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        返回当前占用 CPU 百分比最高的 n 个进程。
        每项包含 pid、name、cpu_percent。
        """
        procs = []
        for p in psutil.process_iter(['pid', 'name']):
            try:
                cpu = p.cpu_percent(interval=0.1)
                procs.append({'pid': p.pid, 'name': p.info['name'], 'cpu_percent': cpu})
            except Exception:
                continue
        procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return procs[:n]

    def recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        返回最近创建的 n 个进程。
        每项包含 pid、name、create_time。
        """
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                procs.append({
                    'pid': p.pid,
                    'name': p.info['name'],
                    'create_time': time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(p.info['create_time'])
                    )
                })
            except Exception:
                continue
        procs.sort(key=lambda x: x['create_time'], reverse=True)
        return procs[:n]
