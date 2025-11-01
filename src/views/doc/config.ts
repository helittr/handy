import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/doc',
    name: 'document',
    label: '文档',
    icon: 'i:document',

    router: {
        path: '/doc/',
        name: 'doc',
        component: () => import('@/views/doc/index.vue'),
        meta: {
            tab: {
                label: '文档',
                icon: 'i:document',
                closable: true,
            },
        },
    },
}

export default config
