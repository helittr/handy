# HandyAPI - ADB脚本管理服务

HandyAPI是一个基于FastAPI的Web服务，用于管理和执行ADB(Android Debug Bridge)脚本。它提供了一个RESTful API接口，可以方便地执行预定义的ADB命令和脚本。

## 功能特性

- 管理预定义的ADB脚本集合
- 通过API执行ADB脚本
- 支持参数化脚本执行
- 支持Windows PowerShell脚本
- 简单的RESTful接口

## 项目结构

```
handyApi/
├── .git/                # Git版本控制
├── .gitignore           # Git忽略规则
├── .python-version      # Python版本指定
├── .venv/               # Python虚拟环境
├── pyproject.toml       # 项目配置和依赖
├── README.md            # 项目文档
├── src/                 # 源代码目录
│   ├── app.py           # FastAPI主应用
│   ├── adb/             # ADB功能模块
│   │   ├── api.py       # API路由定义
│   │   ├── deviceManager.py # 设备管理(待实现)
│   │   ├── scriptManager.py # 脚本管理
│   │   ├── scripts/     # 脚本目录
│   │   │   └── scripts.json # 脚本配置
│   │   └── __init__.py  # 包初始化
└── uv.lock              # 依赖锁定文件
```

## API端点

### 获取可用命令列表
```
GET /adb/commands
```

返回所有可用的ADB脚本列表。

### 执行指定命令
```
POST /adb/commands/{id}/execute
```

执行指定ID的ADB脚本，可以传递参数。

## 安装与运行

### 前提条件
- Python 3.12+
- ADB工具已安装并配置

### 安装步骤
1. 克隆仓库：
   ```bash
   git clone https://github.com/your-repo/handyApi.git
   cd handyApi
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -e .
   ```

4. 运行服务：
   ```bash
   uvicorn src.app:app --reload
   ```

服务将在 `http://localhost:8000` 启动。

## 配置脚本

编辑 `src/adb/scripts/scripts.json` 文件来添加或修改ADB脚本。每个脚本可以定义输入参数和选择参数。

## 未来计划

- 实现设备管理功能
- 支持更多脚本类型
- 添加用户认证
- 提供Web界面

## 贡献

欢迎提交Pull Request或Issue来改进项目。