#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : log_reader.py
Author      : wzw
Date Created: 2025/7/3
Description : Add your script's purpose here.
"""
import subprocess
import os

def run_shell(command: str) -> str:
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""

def collect_system_log(lines: int = 100) -> str:
    """收集系统日志（journalctl）"""
    return run_shell(f"journalctl -n {lines}")

def collect_kernel_log(lines: int = 100) -> str:
    """收集内核日志（dmesg）"""
    return run_shell(f"dmesg | tail -n {lines}")

def collect_app_log(path: str, lines: int = 100) -> str:
    """收集指定路径的应用日志"""
    if not os.path.isfile(path):
        return f"Log file not found: {path}"
    return run_shell(f"tail -n {lines} {path}")

