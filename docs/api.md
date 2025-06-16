# ADB API 文档

## 基础信息
- 基础路径: `/adb`
- 标签: `ADB`

## 接口列表

### 获取ADB命令列表
- 路径: `/commands`
- 方法: GET
- 描述: 获取所有可用的ADB命令

### 执行指定命令
- 路径: `/commands/{sid}/execute`
- 方法: POST
- 参数:
  - sid: 命令ID
  - params: 执行参数

### 获取命令状态  
- 路径: `/commands/{sid}/status`
- 方法: GET
- 参数:
  - sid: 命令ID

### 获取任务日志
- 路径: `/commands/tasks/{tid}/log`
- 方法: GET
- 参数:
  - tid: 任务ID
  - pos: 日志位置
  - size: 日志大小

### 获取任务列表
- 路径: `/commands/tasks`
- 方法: GET

### 删除任务
- 路径: `/commands/tasks/{tid}/delete`
- 方法: DELETE
- 参数:
  - tid: 任务ID

### 停止任务
- 路径: `/commands/tasks/{tid}/stop`
- 方法: POST
- 参数:
  - tid: 任务ID
