<template>
  <n-modal v-model:show="dialogVisible">
    <n-card style="width: 60%;">
    <n-form label-placement="left" label-width="80px" :model="model">
      <n-form-item path="file">
        <n-upload accept=".json" :max="1" >
          <n-upload-dragger>
            <n-text >
              点击或者拖动文件到该区域来上传
            </n-text>
          </n-upload-dragger>
        </n-upload>
      </n-form-item>
      <n-form-item label="差分模式" path="isDifferential">
        <n-switch v-model:value="model.isDifferential" />
      </n-form-item>
      <n-form-item>
        <n-flex justify="end" :gap="10" style="width: 100%;">
          <n-button @click="submit">确认</n-button>
        </n-flex>
      </n-form-item>
    </n-form>
    </n-card>
  </n-modal>
</template>


<script lang="ts" setup>
import { ref } from "vue";
import { NModal, NCard, NForm, NFormItem, NButton, NSwitch, NUpload, NUploadDragger, NText, NFlex } from "naive-ui";

const dialogVisible = ref(false)
const model = ref({
  file: null as File | null,
  isDifferential: false
})
function openDialog() {
  dialogVisible.value = true
}

function submit() {
  console.log("file:", model.value)
}

// function update({file}: {file: File}) {
//   console.log("file:", file)
//   model.value.file = file
// }

defineExpose({
  openDialog
})
</script>
<style scoped></style>
