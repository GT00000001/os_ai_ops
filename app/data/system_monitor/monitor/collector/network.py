import psutil
from .base import Collector
from typing import List, Dict, Any
import time


class NetworkCollector(Collector):
    """网络 I/O 情况采集器"""

    def collect(self) -> dict:
        try:
            # 每个网卡的累计统计
            per_nic = psutil.net_io_counters(pernic=True)
            nic_stats = {}
            for nic, stats in per_nic.items():
                nic_stats[nic] = {
                    "bytes_sent": stats.bytes_sent,
                    "bytes_recv": stats.bytes_recv,
                    "packets_sent": stats.packets_sent,
                    "packets_recv": stats.packets_recv,
                    "errin": stats.errin,
                    "errout": stats.errout,
                    "dropin": stats.dropin,
                    "dropout": stats.dropout,
                }

            # 全局统计
            total = psutil.net_io_counters(pernic=False)
            return {
                "per_nic": nic_stats,
                "total": {
                    "bytes_sent": total.bytes_sent,
                    "bytes_recv": total.bytes_recv,
                    "packets_sent": total.packets_sent,
                    "packets_recv": total.packets_recv,
                },
            }
        except Exception as e:
            return {"error": f"NetworkCollector failed: {e}"}

    def top(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        返回当前网络 I/O 最多的 n 个进程（通过进程 io_counters 中的 bytes_sent+bytes_recv）。
        每项包含 pid、name、bytes_sent、bytes_recv。
        """
        procs = []
        for p in psutil.process_iter(['pid', 'name']):
            try:
                io = p.io_counters()
                sent, recv = io.bytes_sent, io.bytes_recv
                procs.append({
                    'pid': p.pid,
                    'name': p.info['name'],
                    'bytes_sent': sent,
                    'bytes_recv': recv,
                    'total': sent + recv
                })
            except Exception:
                continue
        procs.sort(key=lambda x: x['total'], reverse=True)
        return procs[:n]

    def recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        返回最近建立的 n 条 TCP 连接。
        每项包含 laddr、raddr、status。
        注意：psutil.net_connections 不包含创建时间，这里按遍历顺序近似。
        """
        conns = []
        for c in psutil.net_connections(kind='tcp'):
            try:
                conns.append({
                    'laddr': f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else None,
                    'raddr': f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else None,
                    'status': c.status
                })
            except Exception:
                continue
        # 直接取列表末尾 n 条，近似“最近”——可根据实际需求改为 pcap 方案
        return conns[-n:]
