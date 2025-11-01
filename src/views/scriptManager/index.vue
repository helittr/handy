<template>
  <n-split class="h-full" direction="horizontal" max="400px" min="200px" default-size="240px" :resize-trigger-size="2"
    pane2-style="overflow: hidden; display: flex; flex-direction: column;"
    pane2-class="flex justify-center items-center">
    <template #1>
      <n-split class="h-full" direction="vertical" :max="0.8" min="150px" :default-size="0.3">
        <template #1>
          <n-card class="h-full" title="任务列表" size="small" :bordered="false"
            content-class="!p-1 !flex-1 !overflow-hidden">
            <template #header-extra>
              <n-tooltip trigger="hover">
                <template #trigger>
                  <n-button :bordered="false" size="small" @click.stop="onOpenClick" circle>
                    <template #icon>
                      <Icon icon="i:open" />
                    </template>
                  </n-button>
                </template>
                打开日志文件夹
              </n-tooltip>
            </template>
            <taskList v-model="currCmd" />
          </n-card>
        </template>

        <template #2>
          <n-card class="h-full" title="脚本列表" size="small" :bordered="false"
            content-class="!p-1 !flex-1 !overflow-hidden">
            <template #header-extra>
              <n-tooltip trigger="hover">
                <template #trigger>
                  <n-button :bordered="false" size="small" @click.stop="onSettingClick" circle>
                    <template #icon>
                      <Icon icon="i:content" />
                    </template>
                  </n-button>
                </template>
                查看配置内容
              </n-tooltip>
              <n-tooltip trigger="hover">
                <template #trigger>
                  <n-button :bordered="false" size="small" @click.stop="onRefreshClick" circle>
                    <template #icon>
                      <Icon icon="i:refresh" />
                    </template>
                  </n-button>
                </template>
                重新加载脚本配置文件
              </n-tooltip>
            </template>
            <n-scrollbar trigger="none">
              <toolTree v-model="currCmd" />
            </n-scrollbar>
          </n-card>
        </template>
      </n-split>
    </template>

    <template #2>
      <n-result v-if="errorMessage != null" status="500" title="获取脚本列表出错了！！！" :description=errorMessage size="huge" />

      <RouterView v-else-if="route.fullPath.includes('/task/')" v-slot="{ Component }">
        <keep-alive :max="10">
          <component :is="Component" :key="$route.path" />
        </keep-alive>
      </RouterView>

      <n-result v-else status="info" title="请选择一个脚本任务" description="从左侧脚本列表中选择一个脚本任务以查看详情" size="huge" />
      <configView ref="scriptConfigRef" />
    </template>
  </n-split>

</template>

<script lang="ts" setup>
import toolTree from './toolTree.vue'
import taskList from './taskList.vue'
import configView from './configView.vue'

import { ref, onBeforeMount, onMounted, watch } from 'vue'
import { type Command, reloadScripts, getManagerInfo, registerErrorHandler } from '@/api/commands/scriptsManager'
import { useCommandStore } from '@/stores/commandStore.ts'

import { NSplit, NCard, NScrollbar, NButton, NTooltip, NResult } from 'naive-ui'
import { Icon } from '@iconify/vue'
import { sys_start } from "@/api/sys.ts"
import { useMessage } from 'naive-ui';

import { useRoute } from 'vue-router'

const scriptConfigRef = ref<typeof configView>()
const cmdStore = useCommandStore()
const currCmd = ref<Command | null>(null)
const message = useMessage()
const errorMessage = ref<string | null>(null)
const route = useRoute()

watch(route, (newRoute) => {
  console.log('Route changed:', newRoute)
})

const onOpenClick = async () => {
  const info = await getManagerInfo()
  sys_start(info.logpath)
}

const onSettingClick = () => {
  console.log('Setting clicked', scriptConfigRef.value)
  scriptConfigRef.value?.openDrawer()
}

const onRefreshClick = () => {
  console.log('Refresh clicked')
  reloadScripts().then(() => {
    cmdStore.updateCommandTree()
    message.success('Scripts reloaded successfully')
  })
}

onBeforeMount(() => {
  registerErrorHandler((error) => {
    message.error(error.detail, { keepAliveOnHover: true })
  })
})

onMounted(() => {
  cmdStore.updateCommandTree().catch((error) => {
    errorMessage.value = error.detail
    console.error('Failed to load command tree:', error)
  })
})
</script>
