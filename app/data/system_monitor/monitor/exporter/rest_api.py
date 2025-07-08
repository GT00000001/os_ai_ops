from fastapi import FastAPI, Query
import os
import sys

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 exporter 目录
monitor_dir = os.path.dirname(current_dir)
# 获取项目根目录
project_root = os.path.dirname(monitor_dir)
# 添加项目根目录到Python路径
sys.path.insert(0, project_root)

print(f"Current directory: {current_dir}")
print(f"Exporter directory: {monitor_dir}")
print(f"Project root directory: {project_root}")
print(sys.path)

from monitor.collector.cpu import CPUCollector
from monitor.collector.disk import DiskCollector
from monitor.collector.network import NetworkCollector
from monitor.collector import system_command, log_reader
from typing import Any, Dict, List

app = FastAPI(title="System Monitor")

cpu = CPUCollector()
disk = DiskCollector()
net = NetworkCollector()


@app.get("/metrics")  # 保留原 /metrics
async def metrics():
    return {
        "cpu": cpu.collect(),
        "disk": disk.collect(),
        "network": net.collect()
    }


# —— CPU Top/Recent ——
@app.get("/metrics/cpu/top")
async def cpu_top(n: int = Query(5, ge=1, le=100)) -> List[Dict[str, Any]]:
    return cpu.top(n)


@app.get("/metrics/cpu/recent")
async def cpu_recent(n: int = Query(5, ge=1, le=100)) -> List[Dict[str, Any]]:
    return cpu.recent(n)


# —— Disk Top/Recent ——
@app.get("/metrics/disk/top")
async def disk_top(n: int = Query(5, ge=1, le=100), path: str = Query('/', min_length=1)) -> List[Dict[str, Any]]:
    return disk.top(n, path)


@app.get("/metrics/disk/recent")
async def disk_recent(n: int = Query(5, ge=1, le=100), path: str = Query('/', min_length=1)) -> List[Dict[str, Any]]:
    return disk.recent(n, path)


# —— Network Top/Recent ——
@app.get("/metrics/network/top")
async def network_top(n: int = Query(5, ge=1, le=100)) -> List[Dict[str, Any]]:
    return net.top(n)


@app.get("/metrics/network/recent")
async def network_recent(n: int = Query(5, ge=1, le=100)) -> List[Dict[str, Any]]:
    return net.recent(n)

# —— System Command ——
@app.get("/metrics/command/top")
async def get_top():
    return {"output": system_command.collect_top()}

@app.get("/metrics/command/vmstat")
async def get_vmstat():
    return {"output": system_command.collect_vmstat()}

@app.get("/metrics/command/pidstat")
async def get_pidstat():
    return {"output": system_command.collect_pidstat()}

@app.get("/metrics/command/free")
async def get_free():
    return {"output": system_command.collect_free()}

@app.get("/metrics/command/df")
async def get_df():
    return {"output": system_command.collect_df()}

@app.get("/metrics/command/iostat")
async def get_iostat():
    return {"output": system_command.collect_iostat()}

@app.get("/metrics/command/ethtool")
async def get_ethtool(interface: str = Query("eth0")):
    return {"output": system_command.collect_ethtool(interface)}

# —— Log Reader ——
# 系统日志
@app.get("/metrics/logs/system")
async def get_system_log(lines: int = Query(100, ge=1, le=1000)):
    return {"output": log_reader.collect_system_log(lines)}

# 内核日志
@app.get("/metrics/logs/kernel")
async def get_kernel_log(lines: int = Query(100, ge=1, le=1000)):
    return {"output": log_reader.collect_kernel_log(lines)}

# 应用日志（需提供路径）
@app.get("/metrics/logs/app")
async def get_app_log(path: str = Query(..., min_length=1), lines: int = Query(100, ge=1, le=1000)):
    return {"output": log_reader.collect_app_log(path, lines)}

@app.get("/")
async def root():
    return {"message": "System Monitor is running. Try GET /metrics"}


"""
运行命令：
uvicorn monitor.exporter.rest_api:app --host 0.0.0.0 --port 8000
访问：http://127.0.0.1:8000/metrics
curl http://127.0.0.1:8000/metrics
文档：http://127.0.0.1:8000/docs
"""
