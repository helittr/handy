<template>
    <n-flex class="p-10 h-full" vertical align="start">

        <n-space wrap-item :wrap="false">
            <n-tag v-for="value, index in functions" :key="index" type="success" @click="onFunc(value)" size="large"
                class="transition-transform hover:scale-105" strong bordered checked>
                {{ value }}
            </n-tag>

            <n-tag v-for="value, index in units" :key="index" type="error" @click="onFunc(value)" size="large"
                class="transition-transform hover:scale-105" strong bordered checked>
                {{ value }}
            </n-tag>
        </n-space>


        <n-input ref="inputRef" id="calinput" class="mt-6 transition-all duration-300 !text-xl !font-bold"
            :on-input="onInput" size="large" :on-change="onEnter" v-model:value="expression" :status="status">
            <template #suffix>
                <n-gradient-text class="text-lg !font-bold" :type="status">
                    = {{ result }}
                </n-gradient-text>
            </template>
        </n-input>

        <n-ellipsis :line-clamp="10">
            {{ errmsg }}
        </n-ellipsis>

        <n-list class="w-full shrink-1 overflow-hidden mt-4" bordered hoverable :show-divider="false">
            <template #header>
                <n-flex justify="space-between">
                    <span class="text-lg !font-bold">历史记录</span>
                    <n-button type="primary" @click="onClear" dashed>清空</n-button>
                </n-flex>
            </template>
            <n-scrollbar>
                <transition-group name="list" mode="out-in">
                    <n-list-item v-for="item, index in history" :key="index">
                        <n-gradient-text class="text-lg !font-bold" type="success">
                            {{ item.exp }}
                        </n-gradient-text>
                        <template #suffix>
                            <n-flex>
                                <n-dropdown trigger="hover" :options="generateOptions(index)" :on-select="onAction">
                                    <n-gradient-text class="text-lg !font-bold" type="success">
                                        = {{ item.res }}
                                    </n-gradient-text>
                                </n-dropdown>
                            </n-flex>
                        </template>
                    </n-list-item>
                </transition-group>
            </n-scrollbar>
        </n-list>
    </n-flex>
</template>

<script lang="ts" setup>
import { NInput, NFlex, NGradientText, NList, NListItem, NScrollbar, NButton, NDropdown, NSpace, NTag, NEllipsis } from 'naive-ui'
import { type DropdownOption } from 'naive-ui'
import { evaluate, typeOf } from 'mathjs'
import { ref, onMounted } from 'vue'

const expression = ref('')
const result = ref('')
const errmsg = ref('')
const status = ref<'success' | 'error'>('success')
const history = ref<{ exp: string, res: string }[]>([])
const functions = ref(["sin", "cos", "hex", "oct", "bin", "sqrt", "square", "abs"])
const units = ref(["GB", "MB", "kB", "Hz", "us", "ns", "ms", "secs", "min", "hour", "A", "mA", "nA", "uA"])
const inputRef = ref()

function generateOptions(index: number) {
    return [
        { label: '复制', key: 1, index },
        { label: '删除', key: 2, index },
        { label: '插入', key: 3, index }
    ]
}

function onFunc(func: string) {
    const el: HTMLInputElement = inputRef.value.$el.querySelector('input')
    el.focus()
    if (el.selectionStart !== el.selectionEnd) {
        expression.value = expression.value.replace(
            expression.value.substring(el.selectionStart as number, el.selectionEnd as number),
            ''
        )
    }
    expression.value =
        expression.value.substring(0, el.selectionStart as number) +
        func +
        expression.value.substring(el.selectionStart as number)
}

function onAction(key: number, option: DropdownOption) {
    const his = history.value[option.index as number]
    switch (key) {
        case 1:
            navigator.clipboard.writeText(`${his.exp}=${his.res}`)
            break
        case 2:
            history.value.splice(option.index as number, 1)
            break
        case 3:
            onFunc(`(${his.exp})`)
    }
}

function onInput(value: string) {
    expression.value = value.replace('  ', ' ')
    try {
        const ret = evaluate(value)
        if (typeOf(ret) === "number" || typeOf(ret) === "Unit") {
            result.value = ret.toString()
            errmsg.value = ''
        } else {
            errmsg.value = ret
        }
        status.value = 'success'
    } catch (error) {
        status.value = 'error'
        if (error instanceof Error) {
            errmsg.value = error.message
        }
    }
}

function onEnter() {
    if (status.value === 'success' && expression.value) {
        history.value.push({ exp: expression.value, res: result.value })
    }
}

function onClear() {
    history.value = []
}

onMounted(() => {
    expression.value = "1+1"
    onInput('1+1')
})
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
    transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(10px);
}
</style>
