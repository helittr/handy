import { ref } from 'vue'
import { defineStore } from 'pinia'

export type Tab = {
  name?: string
  label: string
  icon: string
  url: string
  curUrl?: string
  closable: boolean
}

export const useTabStore = defineStore('tabs', () => {
  const tabs = ref<Tab[]>([{ label: '主页', icon: 'i:home', closable: false, url: '/home' }])
  const curTab = ref<Tab>()

  const addTab = (tab: Tab) => {
    if (!tabs.value.some((t) => t.url === tab.url)) {
      tabs.value.push(tab)
      console.log('add tab', tab)
    }
  }

  const removeTab = (url: string) => {
    const index = tabs.value.findIndex((t) => t.url === url)
    if (index !== -1) {
      tabs.value.splice(index, 1)
      console.log('remove tab', url)
    }
  }

  const clearTabs = () => {
    tabs.value = []
    console.log('clear tabs')
  }

  return { tabs, curTab, addTab, removeTab, clearTabs }
})
