<template>
  <n-drawer v-model:show="drawer" resizable width="60%" content-style="height: 100vh;">
    <JsonEditorVue v-model="value" readOnly />
  </n-drawer>
</template>


<script lang="ts" setup>
import { ref } from 'vue'
import { useCommandStore } from '@/stores/commandStore.ts'
import { getSchema } from '@/api/commands/scriptsManager.ts'
import JsonEditorVue from 'json-editor-vue'
import { NDrawer } from 'naive-ui'


const cmdStore = useCommandStore()

const value = ref({})
const schema = ref({})
const drawer = ref(false)

getSchema().then(data => {
  console.log('Schema data:', data)
  schema.value = data
  value.value = cmdStore.commandTree
})

function openDrawer() {
  drawer.value = true
}

defineExpose({
  openDrawer
})

</script>
