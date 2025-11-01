<template>
  <n-form ref="formRef" label-placement="left" require-mark-placement="left" :model="paramsValue" :rules="rules">
    <n-form-item v-for="param in props.params" :key="param.name" :label="param.label" :path="param.name"
      :show-require-mark="param.required">
      <n-input v-if="param.type === 'input'" v-model:value="paramsValue[param.name] as string" clearable />
      <n-select v-else-if="param.type === 'select'" v-model:value="paramsValue[param.name]" :options="param.options"
        clearable :multiple="param.multiple" />
      <n-switch v-else-if="param.type === 'switch'" v-model:value="paramsValue[param.name] as string" />
    </n-form-item>
    <n-button type="primary" @click="onExecute" strong>
      执行
    </n-button>
  </n-form>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import { type ParamValue, type Parameter } from '@/api/commands/scriptsManager'

import { NForm, NFormItem, NInput, NSelect, NSwitch, NButton } from 'naive-ui';
import type { FormRules, FormInst } from 'naive-ui'

const props = defineProps<{
  params: Parameter[]
}>()

const emit = defineEmits<{
  (e: 'execute', ParamValue: ParamValue): void
}>()

const formRef = ref<FormInst>()
const paramsValue: ParamValue = reactive({})
const rules = reactive<FormRules>({})

function onExecute() {
  formRef.value?.validate(
    (errors) => {
      console.log(errors)
      if (!errors) {
        console.log("paramsValue", paramsValue)
        emit('execute', paramsValue)
      }
    }
  );
}

onMounted(() => {
  console.debug('params:', props.params);

  if (props.params !== undefined) {
    props.params.forEach((param) => {
      paramsValue[param.name] = param.default
      console.log(`Initialized param ${param.name} with default value:`, param.default);

      if (param.type != 'switch')
        rules[param.name] = {
          required: param?.required,
          message: "请输入",
        }

    })
  }
})
</script>
