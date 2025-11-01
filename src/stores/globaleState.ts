import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { GlobalTheme } from 'naive-ui'
import { darkTheme, lightTheme} from 'naive-ui'

export const useGlobalStateStore = defineStore("globalState",()=>{

  const isDark = ref<boolean>(true)
  const currentTheme = computed<GlobalTheme>(()=>{
    return isDark.value ? darkTheme : lightTheme;
  })

  const isCollapse = ref<boolean>(true)

  return {
    isDark,
    currentTheme,
    isCollapse
  }
})
