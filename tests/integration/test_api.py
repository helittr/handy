"""API集成测试"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestAPI:
    """API测试类"""

    def test_get_commands(self):
        """测试获取命令列表"""
        pass
