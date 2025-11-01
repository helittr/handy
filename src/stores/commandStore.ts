import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import { type Command, type CommandGroup, getCommands } from '@/api/commands/scriptsManager'

export const useCommandStore = defineStore('commands', () => {
  const commandTree = ref<CommandGroup[]>([])
  const commandMap = new Map<number, Command>()
  const currentCommand = ref<Command | null>(null)
  const currentSn = ref<string | null>(null)

  const firstCommand = computed(() => {
    const keys = Array.from(commandMap.keys())
    if (keys.length) {
      return commandMap.get(keys[0])
    }
    return undefined
  })

  function treeToMap() {
    function iterGroup(grp: CommandGroup) {
      for (const item of grp.children) {
        commandMap.set(item.id, item as Command)
        if (item.type == 'scriptgroup') {
          iterGroup(item)
        }
      }
    }

    commandTree.value.forEach((element) => {
      iterGroup(element)
    })
  }
  async function updateCommandTree() {
    const cg = await getCommands()

    console.log('Fetched command tree:', cg)
    commandTree.value = cg
    if (commandTree.value.length > 0) {
      treeToMap()
      console.log('Setting current command to first command in tree')
    }
  }
  function getCommand(id: number) {
    return commandMap.get(id)
  }

  function getCommandPath(id: number): string[] {
    const path: string[] = []
    function itercmd(items: (CommandGroup | Command)[]): boolean {
      const ret = items.find((item) => {
        if (item.type == 'scriptgroup') {
          path.push(item.label)
          if (itercmd(item.children)) {
            return true
          } else {
            path.pop()
          }
        } else if (item.id == id) {
          path.push(item.label)
          return true
        }
        return false
      })

      return ret ? true : false
    }
    itercmd(commandTree.value)
    console.log('command path ', path)

    return path
  }

  return {
    getCommand,
    commandTree,
    currentCommand,
    updateCommandTree,
    currentSn,
    firstCommand,
    getCommandPath,
  }
})
