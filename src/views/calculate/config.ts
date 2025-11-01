import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/calculate/',
    name: 'calculate',
    label: '计算器',
    icon: 'i:calculate',

    router: {
        path: '/calculate/',
        name: 'calculate',
        component: () => import('@/views/calculate/index.vue'),
        meta: {
            tab: {
                label: '计算器',
                icon: 'i:calculate',
                closable: true,
            },
        },
    },
}

export default config