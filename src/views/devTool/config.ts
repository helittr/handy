import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/devtools/api',
    name: 'api',
    label: 'API',
    icon: 'i:interface',

    router: {
        path: '/devtools/api',
        name: 'api',
        component: () => import('@/views/devTool/index.vue'),
        meta: {
            tab: {
                label: 'API',
                icon: 'i:interface',
                closable: true,
            },
        },
    },
}
export default config