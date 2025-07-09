#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : system_command.py
Author      : wzw
Date Created: 2025/7/2
Description : Add your script's purpose here.
"""
import subprocess

def run_shell(command: str) -> str:
    """执行 shell 命令并返回输出"""
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""

def collect_top() -> str:
    return run_shell("top -b -n 1")

def collect_vmstat() -> str:
    return run_shell("vmstat 1 2 | tail -1")

def collect_pidstat() -> str:
    return run_shell("pidstat 1 1")

def collect_free() -> str:
    return run_shell("free -m")

def collect_df() -> str:
    return run_shell("df -h")

def collect_iostat() -> str:
    return run_shell("iostat -x 1 1")

def collect_ethtool(interface: str = "eth0") -> str:
    return run_shell(f"ethtool {interface}")
