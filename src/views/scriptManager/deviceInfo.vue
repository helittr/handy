<template>
  <el-card class="card" shadow="hover">
    <template #header>
      <div class="devices">
        <el-segmented v-model="currDeviceIndex" :options="devOptions" size="large" :props="{ value: 'index' }">
          <template #default="{ item }">

            <el-icon color="green" size="20px">
              <Iphone />
            </el-icon>
            <el-text size="large" tag="b"> {{ " " + (item as devOption).project }} </el-text>

          </template>
        </el-segmented>
        <span>
          <el-button v-for="btn in quickBtns" :key="btn.label" size="default" :type="btn.type" :icon="btn.icon"
            :disabled="currDevice ? false : true">
            {{ btn.label }}
          </el-button>
        </span>
      </div>
    </template>

    <template v-if="currDevice">
      <el-descriptions size="large" :column="4">
        <el-descriptions-item :label="currDevice.basicInfo.serial.label + ':'">
          {{ currDevice.basicInfo.serial.value }}
        </el-descriptions-item>
        <el-descriptions-item :label="currDevice.basicInfo.project.label + ':'">
          {{ currDevice.basicInfo.project.value }}
        </el-descriptions-item>
        <el-descriptions-item :label="currDevice.basicInfo.model.label + ':'">
          {{ currDevice.basicInfo.project.value }}
        </el-descriptions-item>

        <el-descriptions-item v-for="info, index in devInfoList[currDeviceIndex].basicInfo.more" :key="index"
          :label="info.label + ':'">
          {{ info.value }}
        </el-descriptions-item>
      </el-descriptions>
      <el-collapse v-for="devInfo, index in devInfoList[currDeviceIndex].otherInfo" :key="index"
        expand-icon-position="left">
        <el-collapse-item :title="devInfo.label" name="basicInfo">
          <el-descriptions size="large" :column="4">
            <el-descriptions-item v-for="info, index in devInfo.more" :key="index" :label="info.label + ':'">
              {{ info.value }}
            </el-descriptions-item>
          </el-descriptions>
        </el-collapse-item>
      </el-collapse>
    </template>
    <template v-else>
      <!-- <el-skeleton :rows="2" /> -->
      <el-result icon="error" title="没有设备" sub-title="请连接设备，并打开 ADB 调试"> </el-result>
    </template>
  </el-card>
</template>

<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { type dev, get_devs } from '@/api/adbDevice'
import { useCommandStore } from '@/stores/commandStore'
import { storeToRefs } from 'pinia'

const { currentSn } = storeToRefs(useCommandStore())

interface devOption {
  index: number
  project: string
}

const currDeviceIndex = ref<number>(-1)

const currDevice = computed(() => {
  if (devInfoList.value.length == 0 || currDeviceIndex.value == -1) {
    return null
  }
  return devInfoList.value[currDeviceIndex.value]
})

const devOptions = computed<devOption[]>(() => {
  return devInfoList.value.map((dev, index) => {
    return { index: index, project: dev.basicInfo.project.value }
  })
})

const devInfoList = ref<dev[]>([])

watch(devInfoList, (newVal) => {
  if (newVal.length == 0) {
    currDeviceIndex.value = -1
  } else if (currDeviceIndex.value >= newVal.length) {
    currDeviceIndex.value = newVal.length - 1
  } else if (currDeviceIndex.value == -1 && newVal.length > 0) {
    currDeviceIndex.value = 0
  }
})

watch(currDeviceIndex, (newIndex) => {
  if (currDeviceIndex.value != -1) {
    currentSn.value = devInfoList.value[newIndex].basicInfo.serial.value
  } else {
    currentSn.value = null
  }
  console.log('Current device index changed:', newIndex, 'Current SN:', currentSn.value);
})

interface quickBtn {
  label: string
  type: string
  icon?: string
}

const quickBtns = ref<quickBtn[]>([
  {
    label: '关机',
    type: 'success'
  },
  {
    label: '重启',
    type: 'danger'
  },
  {
    label: '刷机',
    type: 'warning'
  },
  {
    label: '电源键',
    type: 'info'
  }
]
)

onMounted(() => {
  devInfoList.value = get_devs()
})
</script>

<style scope>
.card {
  height: 100%;
  --el-card-padding: 12px
}

.devices {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
