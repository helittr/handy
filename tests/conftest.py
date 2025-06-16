"""测试配置"""

import pytest
from pathlib import Path
from src.adb.config import settings


@pytest.fixture
def scripts_json(tmp_path):
    """创建临时scripts.json文件"""
    json_file = tmp_path / "scripts.json"
    json_file.write_text("[]")
    return json_file
