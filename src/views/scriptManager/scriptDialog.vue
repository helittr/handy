<template>
  <n-modal v-model:show="isShow" :mask-closable="false">
    <n-card class="card" size="small" :on-close="onClose" closable>
      <template #header>
        <n-breadcrumb>
          <n-breadcrumb-item class="breadcrumb-item" v-for="(item, index) in cmdPath" :key="index">
            {{ item }}
          </n-breadcrumb-item>
        </n-breadcrumb>
      </template>

      <n-ellipsis>
        {{ cmd?.description }}
      </n-ellipsis>

      <n-divider />

      <paramForm v-if="cmd" :params="cmd.parameters" @execute="onExecute" />
    </n-card>
  </n-modal>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useCommandStore } from '@/stores/commandStore.ts'
import { useRouter } from "vue-router"
import { type ParamValue, type Command, executeCommand, statusCode } from '@/api/commands/scriptsManager'

import paramForm from './paramForm.vue'
import { useMessage } from 'naive-ui'

import { NModal, NCard, NBreadcrumb, NBreadcrumbItem, NEllipsis, NDivider } from 'naive-ui'

const cmdStore = useCommandStore()
const router = useRouter()
const message = useMessage()

const status = ref(statusCode.PRE)
const cmdPath = ref<string[]>([])
const isShow = ref(false)

const cmd = ref<Command | null>(null)

async function onExecute(param: ParamValue) {
  if (!cmd.value) return

  const ret = await executeCommand(cmd.value.id, param)
  if (ret.code == 0) {
    router.push('/sm/task/' + ret.data.taskId)

    message.success(
      `任务 ${ret.data.taskId} 已创建`
    )
  }
  status.value = statusCode.RUNNING
  isShow.value = false
}

const showDialog = (cmdId: number) => {
  isShow.value = true
  cmdPath.value = cmdStore.getCommandPath(cmdId)
  cmd.value = cmdStore.getCommand(cmdId) || null
}

const onClose = () => {
  isShow.value = false
}

defineExpose({
  showDialog
})

</script>

<style scoped>
.card {
  min-width: 400px;
  width: 60%;
}

.breadcrumb-item {
  font-size: var(--n-title-font-size);
  font-weight: bold;
  text-align: left;
}
</style>
