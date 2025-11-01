import { type viewConfig } from "@/types/view.ts"

const config: viewConfig = {
    index: 1,
    path: '/calendar/',
    name: 'calendar',
    label: '日历',
    icon: 'i:calender',

    router: {
        path: '/calendar/',
        name: 'calendar',
        component: () => import('@/views/calendar/index.vue'),
        meta: {
            tab: {
                label: '日历',
                icon: 'i:calender',
                closable: true,
            },
        },
    },
}

export default config