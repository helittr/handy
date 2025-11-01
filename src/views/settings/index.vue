<template>
  <n-card class="card" footer-class="card-footer">
    <n-collapse>
      <n-collapse-item title="常规设置" name="1">
        <n-form label-placement="left">
          <n-form-item label="主题" :show-feedback="false">
              <n-switch :round="false" v-model:value="data.isDark">
                <template #checked>
                  暗
                </template>
                <template #unchecked>
                  亮
                </template>
              </n-switch>
          </n-form-item>
          <n-form-item label="侧边栏" :show-feedback="false">
              <n-switch :round="false" v-model:value="data.isCollapsed">
                <template #checked>
                  折叠
                </template>
                <template #unchecked>
                  展开
                </template>
              </n-switch>
          </n-form-item>
        </n-form>
      </n-collapse-item>

      <n-collapse-item title="脚本管理器" name="2">
        <n-form label-placement="left">
          <n-form-item label="日志保存目录" >
              <n-input v-model:value="data.logDir" />
          </n-form-item>
          <n-form-item label="脚本配置文件" >
              <n-input v-model:value="data.scriptPath" />
          </n-form-item>
        </n-form>
      </n-collapse-item>
    </n-collapse>
    <template #footer>
      <n-button type="primary" @click="onSave">保存</n-button>
    </template>
  </n-card>
</template>

<script lang="ts" setup>
import { get_settings, update_settings, type settings } from '@/api/settings.ts'

import { ref, onMounted, reactive } from 'vue'
import { NSwitch, NCard, NCollapse, NCollapseItem, NInput,NForm, NFormItem, NButton } from 'naive-ui'
import { useGlobalStateStore } from '@/stores/globaleState.ts'

const globaleStateStore = useGlobalStateStore()
const settingsImpl = ref<settings>()

const data = reactive({
  isDark:false,
  isCollapsed:false,
  logDir:'',
  scriptPath:''
})

function onSave(){
  if(settingsImpl.value){
    settingsImpl.value.theme = data.isDark ? 'dark' : 'light'
    settingsImpl.value.collapsed = data.isCollapsed
    settingsImpl.value.scriptManager.logPath = data.logDir
    settingsImpl.value.scriptManager.scriptPath = data.scriptPath
    update_settings(settingsImpl.value)
  }
  globaleStateStore.isDark = data.isDark
  globaleStateStore.isCollapse = data.isCollapsed
}

onMounted(async () => {
  settingsImpl.value = await get_settings()
  data.isDark = globaleStateStore.isDark = settingsImpl.value.theme == 'dark'
  data.isCollapsed = globaleStateStore.isCollapse = settingsImpl.value.collapsed
  data.logDir = settingsImpl.value.scriptManager.logPath
  data.scriptPath = settingsImpl.value.scriptManager.scriptPath
})
</script>

<style scoped>
.card {
  height: 100%;
}

:deep(.n-form-item-blank){
  justify-content: end;
}

:deep(.card-footer) {
  display: flex;
  justify-content: end;
}
</style>
