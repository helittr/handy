import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/flamegraph',
    name: 'flamegraph',
    label: '火焰图',
    icon: 'i:fire',

    router: {
        path: '/flamegraph/',
        name: 'flamegraph',
        component: () => import('@/views/flamegraph/index.vue'),
        meta: {
            tab: {
                label: '火焰图',
                icon: 'i:fire',
                closable: true,
            },
        },
    },
}

export default config
