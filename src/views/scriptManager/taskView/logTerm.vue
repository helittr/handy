<template>
  <n-card class="overflow-hidden flex-1" content-class="card-content" :title="`日志(${logfile})`" size="small">
    <template #header-extra>
      <n-button-group>
        <n-button @click="openLog" type="error" size="small">
          打开
        </n-button>
        <n-button @click="freshLog" type="primary" size="small">
          刷新
        </n-button>
      </n-button-group>
    </template>
    <div ref="logAreaeIns" class="h-full log pl-(--n-padding-left) select-text">
      <n-log ref="logRef" :log="logs" :loading="isLoading" :rows="rows" trim />
    </div>
  </n-card>
</template>

<script lang="ts" setup>
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import { getTaskLog, getTaskStatus, statusCode } from '@/api/commands/scriptsManager'
import { useRoute, useRouter } from 'vue-router'
import useTaskStore from '@/stores/taskStore'

import { sys_start } from '@/api/sys'

import { NLog, NCard, NButton, NButtonGroup } from 'naive-ui'

const logRef = ref<typeof NLog>()
const rows = ref(20)

const route = useRoute()
const router = useRouter()
const logs = ref<string>('')
const currPos = ref<number>(0)
const logAreaeIns = ref<HTMLElement>()
const taskStore = useTaskStore()
const logfile = ref<string>('')
const isLoading = ref(true)

console.log('get task', logfile.value)

const addLog = (length: number, content: string) => {
  logs.value += content
  currPos.value += length
}

const decode = new TextDecoder('utf-8')

function openLog() {
  sys_start(logfile.value)
}

const freshLog = () => {
  clearLogs()
  poll_log()
}

const clearLogs = () => {
  logs.value = ''
  currPos.value = 0
}

async function poll_log() {
  const tid = parseInt(route.params.id as string)

  if (!isNaN(tid)) {
    if (logfile.value == '') {
      const task = taskStore.getTask(tid)
      if (task) {
        logfile.value = task?.logfile
      }
    }

    try {
      const log = await getTaskLog(tid, currPos.value, 1024000)
      if (log.byteLength) {
        addLog(log.byteLength, decode.decode(log, { stream: true }))
      }

      const st = await getTaskStatus(tid)

      if (!((st.status == statusCode.FINISH || st.status == statusCode.TERMINATED) && log.byteLength == 0)) {
        setTimeout(poll_log, 500)
      } else {
        isLoading.value = false
      }
    }
    catch (e) {
      console.log('error', e)
    }
  } else {
    router.push('/sm')
  }
}

const observe = new ResizeObserver((entries) => {
  for (const entry of entries) {
    console.log("rows:", rows.value, "height:", entry.contentRect.height)
    rows.value = Math.floor(entry.contentRect.height / 14 / 1.25)
  }
})

onMounted(() => {
  poll_log()
  rows.value = Math.floor(logAreaeIns.value!.offsetHeight / 14 / 1.25)
  observe.observe(logAreaeIns.value as Element)
  watch(logs, () => {
    nextTick(() => {
      logRef.value?.scrollTo({ position: 'bottom', silent: true })
    })
  })
})

onUnmounted(() => {
  observe.disconnect()
})

defineExpose({ clearLogs })
</script>
