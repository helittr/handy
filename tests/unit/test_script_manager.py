"""ScriptManager单元测试"""

import pytest
from src.adb.core.scriptManager import ScriptManager


class TestScriptManager:
    """ScriptManager测试类"""

    def test_init(self, scripts_json):
        """测试初始化"""
        manager = ScriptManager(str(scripts_json))
        assert manager is not None
