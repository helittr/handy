<template>
  <n-config-provider class="layout" :theme="globaleStateStore.currentTheme">
    <n-message-provider>
      <n-layout class="layout" has-sider>
        <n-layout-sider :width="180" :collapsed-width="64" show-trigger="arrow-circle"
          v-model:collapsed="globaleStateStore.isCollapse" collapse-mode="width" bordered>
          <sideBar />
        </n-layout-sider>

        <n-layout content-class="main-layout">
          <n-layout-header class="main-header" bordered>
            <headerContent />
          </n-layout-header>

          <n-layout-content content-class="main-content" :native-scrollbar="false">
            <router-view v-slot="{ Component }">
              <transition>
                <keep-alive>
                  <component :is="Component" />
                </keep-alive>
              </transition>
            </router-view>
          </n-layout-content>
        </n-layout>
      </n-layout>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { NLayout, NLayoutSider, NLayoutHeader, NLayoutContent, NConfigProvider, NMessageProvider } from 'naive-ui';
import sideBar from './components/aside/sideBar.vue';
import headerContent from './components/header/headerContent.vue';
import { useGlobalStateStore } from './stores/globaleState';

const globaleStateStore = useGlobalStateStore()
</script>

<style scoped>
.layout {
  height: 100%;
}

:deep(.main-layout) {
  display: flex;
  flex-direction: column;
}

.main-header {
  height: 39px;
}

:deep(.main-content) {
  height: 100%;
  width: 100%;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
