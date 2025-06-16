# ADB 脚本开发文档

## 脚本结构
脚本存储在 `src/adb/scripts/powershell/` 目录下

## 脚本定义
脚本信息定义在 `scripts.json` 中，包含以下字段：
- id: 脚本ID
- name: 脚本名称
- type: 脚本类型 (如 winpowershell)
- path: 脚本路径
- label: 显示标签
- description: 描述
- parameters: 参数列表

## 参数类型
支持三种参数类型：
1. InputParameter: 文本输入
2. SelectParameter: 下拉选择
3. SwitchParameter: 开关选项

## 示例脚本
```powershell
param(
    [string]$deviceId,
    [string]$command
)

adb -s $deviceId shell $command
