import type { MenuOption } from 'naive-ui'
import { type viewConfig } from "@/types/view.ts"

function get_menu1(): MenuOption[] {
  return [
    {
      label: '脚本管理',
      key: 'scriptManagement',
      iconString: 'i:scripts',
      url: '/sm',
    },
    {
      label: '火焰图',
      key: 'flamegraph',
      iconString: 'i:fire',
      url: '/flamegraph',
    },
    {
      label: '日历',
      key: 'calendar',
      iconString: 'i:calender',
      url: '/calendar',
    },
    {
      label: '开发工具',
      key: 'devTools',
      iconString: 'i:devtool',
      children: [
        {
          label: 'API 测试',
          key: 'apiTest',
          iconString: 'i:interface',
          url: '/devtools/api',
        },
      ],
    },
    {
      label: '设置',
      key: 'settings',
      iconString: 'i:setting',
      url: '/settings',
    },
    {
      label: '文档',
      key: 'settings',
      iconString: 'i:document',
      url: '/doc',
    },
  ]
}

type MenuOptionExt = MenuOption & { index: number }

async function get_menu(): Promise<(MenuOptionExt)[]> {
  const modules = import.meta.glob<true, string, viewConfig>('/src/views/*/config.ts', { import: 'default', eager: true })
  let menuOptions: MenuOptionExt[] = []

  console.log('modules', modules)
  for (const path in modules) {
    const mod = modules[path]
    menuOptions.push({
      index: mod.index,
      label: mod.label,
      key: mod.name,
      iconString: mod.icon,
      url: mod.path,
      show: mod.show
    })
  }

  menuOptions.sort((a, b) => a.index - b.index)

  return menuOptions
}

export { get_menu }
