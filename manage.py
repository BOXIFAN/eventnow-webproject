#!/usr/bin/env python
"""Django 命令行入口，用于运行服务器、迁移数据库等任务。"""
import os
import sys


def main():
    """运行 Django 管理命令。"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Please install dependencies first."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
