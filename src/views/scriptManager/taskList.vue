<template>
  <n-collapse class="h-full flex flex-col" :default-expanded-names="['running', 'finished']">
    <n-collapse-item title="运行中" name="running">
      <n-scrollbar style="max-height: 100%;">
        <n-list clickable :show-divider="false" hoverable s>
          <n-list-item class="!p-[6px] leading-[1]"
            :class="{ current: parseInt(route.params.id as string) == t.taskId }" v-for="t in runingTask"
            :key="t.taskId" @click="onTaskClick(t)">
            <template #prefix>
              <Icon class="icon" icon="i:running" width="16" />
            </template>
            <n-ellipsis>{{ get_label(t) }}</n-ellipsis>
          </n-list-item>
        </n-list>
      </n-scrollbar>
    </n-collapse-item>
    <n-collapse-item title="已完成" name="finished">
      <n-scrollbar style="max-height: 100%;">
        <n-list clickable :show-divider="false" hoverable>
          <n-list-item class="!p-[6px] leading-[1]"
            :class="{ current: parseInt(route.params.id as string) == t.taskId }" v-for="t in otherTask" :key="t.taskId"
            @click="onTaskClick(t)">
            <template #prefix>
              <Icon class="icon" icon="i:task" width="16" />
            </template>
            <n-ellipsis style="width: 100%;">{{ get_label(t) }}</n-ellipsis>
          </n-list-item>
        </n-list>
      </n-scrollbar>
    </n-collapse-item>
  </n-collapse>
</template>

<script lang="ts" setup>
import { onBeforeMount, computed, type ComputedRef } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { type Task, statusCode } from '@/api/commands/scriptsManager'
import { useCommandStore } from '@/stores/commandStore.ts'
import useTaskStore from '@/stores/taskStore.ts'
import { Icon } from "@iconify/vue";

import { NCollapse, NCollapseItem, NList, NListItem, NEllipsis, NScrollbar } from 'naive-ui'

interface taskGroup {
  label: string
  children: ComputedRef<Task[]>
}

const cmdStore = useCommandStore()
const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()
const runingTask = computed(() => taskStore.tasks.filter(t => t.status == statusCode.RUNNING))
const otherTask = computed(() => taskStore.tasks.filter(t => t.status != statusCode.RUNNING))


function get_label(node: Task | taskGroup) {
  if ('children' in node) {
    return node.label
  } else {
    return cmdStore.getCommand(node.commandId)?.label + ' ' + node.taskId
  }
}

function onTaskClick(task: Task) {
  if ('children' in task) return
  router.push('/sm/task/' + task.taskId)
}

onBeforeMount(async () => taskStore.startSync())
</script>

<style scoped>
.current {
  background-color: var(--n-color-hover);
  color: var(--n-color-target);
}

.n-collapse-item {
  --n-item-margin: 0;
  --n-title-padding: 0;
  min-height: 30px;
  /* padding: 0; */
  /* flex-shrink: 1; */
  /* overflow: hidden;
  display: flex;
  flex-direction: column; */
}

:deep(.n-collapse-item__content-inner) {
  height: 100%;
}

:deep(.n-collapse-item .n-collapse-item__content-wrapper) {
  overflow: hidden;
  flex-shrink: 1;
}

:deep(.list-item > .n-list-item__main) {
  display: flex;
  align-items: center;
}

:deep(.n-collapse-item__content-inner) {
  padding: 0 !important;
}
</style>
