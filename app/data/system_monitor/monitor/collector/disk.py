import psutil
from .base import Collector
from typing import List, Dict, Any
import time

class DiskCollector(Collector):
    """磁盘使用情况采集器"""

    def collect(self) -> dict:
        result = {}
        try:
            # 遍历所有分区
            for part in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    result[part.device] = {
                        "mountpoint": part.mountpoint,
                        "fstype": part.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent,
                    }
                except PermissionError:
                    # 某些系统分区可能无法访问
                    result[part.device] = {"error": "permission denied"}
            # 还可以采集总体 I/O 统计
            io_counters = psutil.disk_io_counters()
            result["io"] = {
                "read_count": io_counters.read_count,
                "write_count": io_counters.write_count,
                "read_bytes": io_counters.read_bytes,
                "write_bytes": io_counters.write_bytes,
            }
            return result
        except Exception as e:
            return {"error": f"DiskCollector failed: {e}"}

    def top(self, n: int = 5, path: str = '/') -> List[Dict[str, Any]]:
        """
        返回指定目录下（默认为根）最大的 n 个文件。
        每项包含 file_path、size。
        """
        files = []
        for root, _, filenames in os.walk(path):
            for fn in filenames:
                full = os.path.join(root, fn)
                try:
                    size = os.path.getsize(full)
                    files.append({'file_path': full, 'size': size})
                except Exception:
                    continue
        files.sort(key=lambda x: x['size'], reverse=True)
        return files[:n]

    def recent(self, n: int = 5, path: str = '/') -> List[Dict[str, Any]]:
        """
        返回指定目录下最近创建的 n 个文件。
        每项包含 file_path、create_time。
        """
        files = []
        for root, _, filenames in os.walk(path):
            for fn in filenames:
                full = os.path.join(root, fn)
                try:
                    c = os.path.getctime(full)
                    files.append({
                        'file_path': full,
                        'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c))
                    })
                except Exception:
                    continue
        files.sort(key=lambda x: x['create_time'], reverse=True)
        return files[:n]