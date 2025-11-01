import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getTasks, type Task, getSocket } from '@/api/commands/scriptsManager'

const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const taskMap = ref<Map<number, Task>>(new Map())
  const lastUpdate = ref(0)
  let socket: WebSocket | null = null

  async function updateTasks() {
    try {
      const newTasks = await getTasks()
      if (newTasks == undefined) {
        return false
      }
      //   console.log('Fetched tasks:', newTasks, lastUpdate.value)
      if (newTasks?.lastUpdate != lastUpdate.value) {
        // console.log('Tasks updated:', newTasks)
        lastUpdate.value = newTasks.lastUpdate
        tasks.value = newTasks.tasks
        console.log('Tasks updated:', tasks.value)
        taskMap.value.clear()
        newTasks.tasks?.forEach((task) => {
          taskMap.value.set(task.taskId, task)
        })
      }
    } catch (error) {
      console.error('Failed to update tasks:', error)
    }
    return true
  }

  const getTask = (id: number) => {
    return taskMap.value.get(id)
  }

  async function startSync() {
    if (socket) {
      console.warn('WebSocket already connected, skipping reconnection')
      return
    }

    try {
      socket = await getSocket()
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error)
      return
    }

    if (!socket) {
      console.error('Failed to establish WebSocket connection')
      return
    }

    socket.addEventListener('message', ({ data }) => {
      if (data === 'ping') {
        // console.log('Received pong from server')
        socket?.send('pong') // Send pong response
        return
      }

      try {
        const newTasks = JSON.parse(data)
        // console.log('Received WebSocket message:', newTasks);

        if (newTasks?.lastUpdate != lastUpdate.value) {
          console.log('Tasks updated:', newTasks)
          lastUpdate.value = newTasks.lastUpdate
          tasks.value = newTasks.tasks
          console.log('Tasks updated:', tasks.value)
          taskMap.value.clear()
          newTasks.tasks.forEach((task: Task) => {
            taskMap.value.set(task.taskId, task)
          })
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error)
      }
    })
  }

  function stopSync() {
    // Implement logic to stop the WebSocket connection if needed
    console.log('Stopping task sync')
  }

  return {
    tasks,
    currentTask,
    startSync,
    stopSync,
    getTask,
    taskMap,
    updateTasks,
  }
})

export default useTaskStore
