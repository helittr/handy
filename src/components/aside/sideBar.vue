<template>
  <n-layout class="side-layout">
    <n-layout-header class="sideBar-header" bordered>
      <router-link to="/home">
        <n-gradient-text type="primary" size="24px">
          {{ globaleStateStore.isCollapse ? 'H' : 'Handy' }}
        </n-gradient-text>
      </router-link>
    </n-layout-header>

    <n-layout-content>
      <n-menu :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions" :render-label="renderMenuLabel"
        :render-icon="renderMenuIcon" :collapsed="globaleStateStore.isCollapse" />
    </n-layout-content>
  </n-layout>
</template>

<script lang="ts" setup>
import { NMenu, NGradientText, NLayout, NLayoutHeader, NLayoutContent } from 'naive-ui';
import type { MenuOption } from 'naive-ui';
import { h, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router';
import { Icon } from "@iconify/vue";
import { get_menu } from '@/api/api.ts'
import { useGlobalStateStore } from '@/stores/globaleState';

const globaleStateStore = useGlobalStateStore()
const menuOptions = ref<MenuOption[]>()

function renderMenuLabel(option: MenuOption) {
  return h(
    RouterLink,
    {
      to: option.url || '/',
    },
    { default: () => option.label }
  )
}

function renderMenuIcon(option: MenuOption) {
  if (option?.iconString) {
    return h(Icon, { icon: option.iconString as string })
  }
  return h(Icon, { icon: 'bx:bx-home' })
}

onMounted(async () => {
  menuOptions.value = await get_menu()

  console.log("MenuOption", menuOptions)
})
</script>

<style scoped>
.sideBar-header {
  text-align: center;
  height: 39px;
}

.side-layout {
  height: 100%;
}
</style>
