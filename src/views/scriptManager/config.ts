import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 0,
    path: '/sm',
    name: 'scriptManagement',
    label: '脚本',
    icon: 'i:scripts',

    router: {
        path: '/sm',
        component: () => import('@/views/scriptManager/index.vue'),
        children: [
            {
                path: 'task/:id',
                component: () => import('@/views/scriptManager/taskView/taskDtail.vue'),
            },
        ],
        meta: {
            tab: {
                label: '脚本管理',
                icon: 'i:scripts',
                closable: true,
            },
        },
    }
}

export default config
