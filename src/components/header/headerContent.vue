<template>
  <n-tabs class="tabs" type="card" :on-update:value="onTabUpdate" :value="curTabUrl" :on-close="onCloseTab" closable
    animated>
    <n-tab v-for="item in tabStore.tabs" :key="item.url" :name="item.url" :closable="item.closable">
      <icon :icon="item.icon" height="20" style="margin-right: 6px;"></icon>
      {{ item.label }}
    </n-tab>
    <template #suffix>
      <n-switch :round="false" v-model:value="globaleStateStore.isDark">
        <template #checked>
          暗
        </template>
        <template #unchecked>
          亮
        </template>
      </n-switch>
    </template>
  </n-tabs>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'

import { useTabStore } from '../../stores/tabs.ts'
import { useRoute, useRouter } from 'vue-router'

import { NTabs, NTab, NSwitch } from 'naive-ui'
import { useGlobalStateStore } from '@/stores/globaleState.ts'

import { Icon } from '@iconify/vue'

const curTabUrl = ref<string>('/home')
const route = useRoute()
const router = useRouter()
const tabStore = useTabStore()

const globaleStateStore = useGlobalStateStore()

watch(
  () => route.path,
  () => {
    console.log("route path change", route);

    if (route.meta.tab === undefined) {
      return
    }

    for (const r of route.matched) {
      if ('tab' in r.meta) {
        console.log('tab meta:', r.meta.tab)
        const foundTab = tabStore.tabs.find((t) => t.url == r.path)
        if (foundTab) {
          foundTab.curUrl = route.fullPath
        } else {
          tabStore.addTab({
            ...(route.meta.tab),
            url: r.path,
            curUrl: r.path
          })
        }
        curTabUrl.value = r.path
      }
    }
  }
)

function onTabUpdate(url: string) {
  console.log("tabChange", url)
  for (const tab of tabStore.tabs) {
    if (tab.url == url) {
      router.push(tab.curUrl || tab.url)
      tabStore.curTab = tab
      break
    }
  }
}

function onCloseTab(url: string) {
  console.log("tabClose", url)
  tabStore.removeTab(url)
  router.push('/home')
  curTabUrl.value = '/home'
}
</script>

<style scoped>
.header-layout {
  align-items: center;
  height: 100%;
}
</style>

<style></style>
