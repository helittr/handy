import { type RouteRecordRaw } from 'vue-router'


export type viewConfig = {
    index: number,
    label: string,
    path: string,
    name: string,
    icon: string,
    show?: boolean,
    router: RouteRecordRaw
}
