import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/settings',
    name: 'settings',
    label: '设置',
    icon: 'i:setting',

    router: {
        path: '/settings/',
        name: 'settings',
        component: () => import('@/views/settings/index.vue'),
        meta: {
            tab: {
                label: '设置',
                icon: 'i:setting',
                closable: true,
            },
        },
    }
}

export default config
