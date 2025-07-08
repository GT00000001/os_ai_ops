# 工具函数（命令执行、文件操作等）
# 功能：通用工具函数
# 核心方法：
# run_command()：安全执行系统命令
# parse_json()：解析 JSON 数据
# validate_input()：验证用户输入
# format_bytes()：格式化字节单位
import subprocess
import json
import re
from app.config import config

def run_command(command, timeout=30):
    """安全执行系统命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise Exception(f"Command failed: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def parse_json(json_str):
    """解析JSON字符串"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

def validate_input(input_str, pattern=r'^[a-zA-Z0-9\s_-]+$'):
    """验证输入是否符合安全模式"""
    return re.match(pattern, input_str) is not None

def format_bytes(bytes_size, precision=2):
    """格式化字节单位"""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while bytes_size >= 1024 and unit_index < len(units) - 1:
        bytes_size /= 1024
        unit_index += 1
    return f"{bytes_size:.{precision}f} {units[unit_index]}"