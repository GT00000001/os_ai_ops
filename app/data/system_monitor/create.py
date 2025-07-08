#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : temp.py
Author      : wzw
Date Created: 2025/6/28
Description : Add your script's purpose here.
"""
import os


def create_structure():
    # 根目录
    root = "system_monitor"

    # 目录列表
    dirs = [
        "monitor/collector",
        "monitor/exporter",
        "monitor/utils",
    ]

    # 文件列表（相对于根目录）
    files = [
        "app.py",
        "pyproject.toml",
        "monitor/__init__.py",
        "monitor/config.py",
        "monitor/collector/base.py",
        "monitor/collector/cpu.py",
        "monitor/collector/disk.py",
        "monitor/collector/network.py",
        "monitor/collector/gpu_domestic.py",
        "monitor/collector/system_command.py",
        "monitor/collector/log_reader.py",
        "monitor/exporter/rest_api.py",
        "monitor/utils/os_info.py",
    ]

    # 创建根目录
    os.makedirs(root, exist_ok=True)

    # 创建所有子目录
    for d in dirs:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    # 创建所有空文件
    for f in files:
        file_path = os.path.join(root, f)
        open(file_path, 'a').close()  # 'a'模式文件不存在时会创建

    print(f"目录结构 '{root}' 创建完成!")


if __name__ == "__main__":
    create_structure()