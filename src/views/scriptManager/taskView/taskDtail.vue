<template>
  <n-flex class="w-full h-full" :size="0" vertical>
    <n-card class="f-0 max-h-1/5 over" title="任务详情" size="small" content-class="overflow-auto">
      <template #header-extra>
        <n-button-group>
          <n-button type="error" @click="delTask" size="small">删除</n-button>
          <!-- <n-button type="primary" @click="normalStopTask" size="small">Crtl+c</n-button> -->
          <n-button type="warning" @click="forceStopTask" size="small">终止</n-button>
        </n-button-group>
      </template>
      <n-scrollbar>
        <n-descriptions label-placement="left">
          <n-descriptions-item label="任务 ID">{{ task?.taskId }}</n-descriptions-item>
          <n-descriptions-item label="状态">
            {{ status == statusCode.RUNNING ? '运行中' : '已完成' }}
          </n-descriptions-item>
          <n-descriptions-item label="脚本 ID">{{ task?.commandId }}</n-descriptions-item>
          <n-descriptions-item label="cmdline">{{ task?.cmdline }}</n-descriptions-item>
        </n-descriptions>
      </n-scrollbar>
    </n-card>
    <logTerm ref="logTermRef" />
  </n-flex>
</template>

<script lang="ts" setup>
import { ref, onBeforeMount, computed } from 'vue';
import logTerm from '@/views/scriptManager/taskView/logTerm.vue';
// import { type task } from '@/api/scriptsManager';
import { useRoute, useRouter } from 'vue-router';
import useTaskStore from '@/stores/taskStore.ts';
import { statusCode, deleteTask, stopTask as apiStopTask, type Task } from '@/api/commands/scriptsManager';

import { NDescriptions, NDescriptionsItem, NButton, NButtonGroup, NCard, NFlex, NScrollbar } from 'naive-ui';
import { useMessage } from 'naive-ui';

const route = useRoute();
const router = useRouter();

const taskStore = useTaskStore();

const logTermRef = ref<typeof logTerm | null>(null);

const message = useMessage();

const task = ref<Task>()

const status = computed(() => {
  return taskStore.taskMap.get(parseInt(route.params.id as string))?.status
});

const delTask = async () => {
  if (status.value == statusCode.RUNNING) {
    message.error(`任务(${task.value?.taskId})正在运行，无法删除`)
    return
  }
  if (await deleteTask(task.value?.taskId as number)) {
    message.success(`任务(${task.value?.taskId})删除成功`)
    await taskStore.updateTasks()
    for (let i = taskStore.tasks.length - 1; i > 0; i--) {
      if (task.value?.taskId != taskStore.tasks[i].taskId) {
        console.log("push to : ", taskStore.tasks[0].taskId)
        router.push('/sm/task/' + taskStore.tasks[0].taskId)
        return
      }
    }

    router.push('/sm')
  }
}

// const normalStopTask = async () => {
//   if (status.value != statusCode.RUNNING) {
//     message.error(`任务(${task.value?.taskId})未运行，无法中止`)
//   } else {
//     await apiStopTask(task.value?.taskId as number)
//     message.success(`任务(${task.value?.taskId})中止信号发送成功`)
//   }
// }

const forceStopTask = async () => {
  if (status.value != statusCode.RUNNING) {
    message.error(`任务(${task.value?.taskId})未运行，无法强制中止`)
  } else {
    await apiStopTask(task.value?.taskId as number, true)
    message.success(`任务(${task.value?.taskId})强制中止信号发送成功`)
  }
}

onBeforeMount(async () => {
  await taskStore.updateTasks()
  task.value = taskStore.taskMap.get(parseInt(route.params.id as string))
  console.log('task dtail:', task.value)
  if (task.value === undefined) {
    router.push('/sm')
  }
})
</script>
