import lodash from 'lodash'

import { server } from '../../utils/server.ts'
import { AxiosError, type AxiosResponse } from 'axios'

// 统一错误处理
const handleError = (error: import('axios').AxiosError) => {
  console.error('API Error:', error.response?.status, error.response?.data)
  return Promise.reject(error)
}

// 添加响应拦截器
server.interceptors.response.use(
  (response) => response,
  (error) => handleError(error),
)

/**
 * 基础命令接口
 */
interface CommandBase {
  type: 'winpowershell' | 'powershell' | 'scriptgroup' | 'python'
  id: number
  name: string
  label: string
  description: string
}

/**
 * 参数值类型
 */
export interface ParamValue {
  [key: string]: string | string[]
}

/**
 * 参数定义接口
 */
export interface Parameter {
  name: string
  label: string
  type: 'input' | 'select' | 'switch'
  required?: boolean
  multiple?: boolean
  default: string | string[]
  options?: {
    label: string
    value: string | number
  }[]
}

/**
 * 命令接口
 */
export interface Command extends CommandBase {
  type: 'winpowershell' | 'powershell'
  parameters: Parameter[]
}

/**
 * 命令组接口
 */
export interface CommandGroup extends CommandBase {
  type: 'scriptgroup'
  children: (CommandGroup | Command)[]
}

interface ErrorDetail {
  detail: string
}

export async function getCommands(): Promise<CommandGroup[]> {
  try {
    const res = await server.get('/adb/commands')
    return res.data
  } catch (error) {
    console.log('Error fetching commands:', error)
    if (error instanceof AxiosError) {
      return Promise.reject(error.response?.data as ErrorDetail)
    }

    throw error
  }
}

/**
 * Executes a command on the specified device.
 * @param commandId - The ID of the command to execute
 * @param params - The parameters to pass with the command
 */
export async function executeCommand(commandId: number, params: ParamValue) {
  console.log(`Executing command ${commandId} with params:`, params)
  const res = await server.post('/adb/commands/' + commandId + '/execute', params)
  return res.data
}

export enum statusCode {
  PRE = 1,
  RUNNING,
  FINISH,
  TERMINATED,
}

export interface CommandStatus {
  taskId: number
  status: statusCode
  updatedAt?: string
}
/**
 * Fetches and logs the status of a command by its ID.
 * @param commandId - The ID of the command to check.
 */
export async function getTaskStatus(taskId: number): Promise<CommandStatus> {
  const res = await server.get('/adb/commands/' + taskId + '/status')
  return res.data
}

export async function getTaskLog(
  taskId: number,
  pos: number = 0,
  size: number = -1,
): Promise<Uint8Array> {
  const res = await server.get('/adb/commands/tasks/' + taskId + '/log', {
    params: {
      pos: pos,
      size,
    },
    responseType: 'arraybuffer',
  })
  return res.data
}

export interface Task {
  taskId: number
  commandId: number
  status: statusCode
  createdAt?: string
  cmdline: string
  logfile: string
}

export interface TaskResult {
  lastUpdate: number
  tasks: Task[]
}

export async function getTasks(): Promise<TaskResult | undefined> {
  try {
    const res = await server.get('/adb/commands/tasks')
    if (res.status == 200) {
      // console.log('res', res.data)
      return lodash.cloneDeep(res.data)
    }
  } catch {
    return Promise.reject()
  }
}

export async function deleteTask(taskId: number): Promise<boolean> {
  const res = await server.delete(`/adb/commands/tasks/${taskId}/delete`)
  if (res.data.code == 0) {
    return true
  }
  return false
}

export async function stopTask(taskId: number, force: boolean = false): Promise<unknown> {
  const reqParams: { force: boolean } = { force: force }
  return server.post(`/adb/commands/tasks/${taskId}/stop`, reqParams)
}

export async function getSocket(): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket('ws://127.0.0.1:8001/adb/ws')

    socket.addEventListener('open', () => {
      console.log('WebSocket connection established')
      resolve(socket)
    })

    socket.addEventListener('error', (error) => {
      reject(error)
    })

    socket.addEventListener('close', () => {
      console.log('WebSocket connection closed')
    })
  })
}

export async function getSchema(): Promise<object> {
  const res = await server.get('/adb/commands/schema')
  if (res.status == 200) {
    return res.data
  }
  return {}
}

export async function reloadScripts(): Promise<boolean> {
  const res = await server.post('/adb/commands/reload')
  if (res.status == 200) {
    return res.data.code == 0
  }
  return false
}

interface managerInfo {
  logpath: string
}

export async function getManagerInfo(): Promise<managerInfo> {
  const res = await server.get<managerInfo>('/adb/info')
  return res.data
}

export function registerErrorHandler(handler: (error: ErrorDetail) => void) {
  server.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: import('axios').AxiosError<ErrorDetail, ErrorDetail>) => {
      handler(error.response?.data as ErrorDetail)
      return Promise.reject(error)
    },
  )
}
