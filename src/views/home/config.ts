import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/home',
    name: 'home',
    label: '主页',
    icon: 'i:home',
    show: false,

    router: {
        path: '/home',
        name: 'home',
        meta: {
            tab: {
                label: '主页',
                icon: 'oui:home',
                closable: false,
            },
        },
        component: () => import('@/views/home/index.vue'),
    }
}

export default config
