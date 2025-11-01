import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'
import { type viewConfig } from "@/types/view.ts"
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    tab?: {
      label: string
      icon: string
      closable: boolean
    }
  }
}

// type TabMeta = {
//   label: string
//   icon: string
//   closable: boolean
// }

const comandroutes: RouteRecordRaw[] = [
  {
    path: 'task/:id',
    component: () => import('@/views/scriptManager/taskView/taskDtail.vue'),
  },
]

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'root',
    redirect: '/home',
  },

]

const modules = import.meta.glob<true, string, viewConfig>('/src/views/*/config.ts', { import: 'default', eager: true })

for (const path in modules) {
  const mod = modules[path]
  console.log('module', mod.router)
  if (mod.router) {
    routes.push(mod.router)
  }
}

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
