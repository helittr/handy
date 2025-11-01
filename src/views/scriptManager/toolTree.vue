<template>
  <n-flex>

    <n-input v-model:value="input" placeholder="搜索">
      <template #prefix>
        <icon icon="i:search" />
      </template>
    </n-input>

    <n-tree class="w-full" ref="treeRef" :pattern="input" :data="cmdStore.commandTree" :filter="filterNode"
      key-field="id" :override-default-node-click-behavior="onNodeClick" :indent="12" default-expand-all expand-on-click
      show-line :show-irrelevant-nodes="false" :selectable="false" :render-prefix="renderPrefix" block-line>
    </n-tree>

    <scriptDialog ref="scriptDialogRef" />

  </n-flex>
</template>

<script lang="ts" setup>
import { ref, h } from 'vue'

import { useCommandStore } from '@/stores/commandStore.ts'
import scriptDialog from './scriptDialog.vue'

import { NFlex, NInput, NTree } from 'naive-ui'
import type { TreeOption, TreeOverrideNodeClickBehaviorReturn } from 'naive-ui'
import { Icon } from "@iconify/vue";

const scriptDialogRef = ref<typeof scriptDialog>()
const input = ref<string>('')
const cmdStore = useCommandStore()

function filterNode(pattern: string, node: TreeOption): boolean {
  if (pattern.length == 0 || !('label' in node)) return true
  return Boolean(node.label?.includes(pattern))
}

function isLeaf(option: TreeOption): boolean {
  return !('children' in option)
}

const onNodeClick = ({ option }: { option: TreeOption }): TreeOverrideNodeClickBehaviorReturn => {
  console.debug('Node clicked:', option);
  if (isLeaf(option))
    scriptDialogRef.value?.showDialog(option.id)
  return 'default'
}

// function renderPrefix({ option }: { option: TreeOption }) {
//   if (!isLeaf(option)) {
//     return undefined
//   }
//   return h(Icon, { icon: 'i:script', height: '18' })
// }

function renderPrefix({ option }: { option: TreeOption }) {
  if (!isLeaf(option)) {
    return undefined
  }

  // console.log("optin", option.type)
  // switch(option.type){
  //   case 'python': return 
  // }
  return h(Icon, { icon: `i:${option.type}`, height: '18', inline: true })
}
</script>
