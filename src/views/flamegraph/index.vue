<template>
  <n-flex vertical style="height: 100%;" @dragover.prevent="(e: DragEvent) => e.preventDefault()"
    @drop.prevent="openData" size="small">
    <n-flex justify="space-between" align="center" style="margin: 10px;">
      <n-input-group style="width: fit-content;">
        <n-button type="primary" @click="graph.resetZoom()" :focusable="false" size="small">复位</n-button>
      </n-input-group>
      <n-flex :wrap="false" justify="space-between" align="center">
        <n-checkbox size="large" label="倒置" v-model:checked="graphConfig.isInverted"> </n-checkbox>
        <n-checkbox size="large" label="selfValue" v-model:checked="graphConfig.isSelfValue"> </n-checkbox>
        <n-checkbox size="large" label="computeDelta" v-model:checked="graphConfig.isComputeDelta"> </n-checkbox>
        <n-input-number class="layerHeightInput" v-model:value="graphConfig.layerHeight" :step="1" size="small"
          :min="20" />
        <span>层高</span>
        <n-select v-model:value="graphConfig.colorMapper" :options="options" style="width: 100px;"></n-select>
        <span>颜色</span>
      </n-flex>
      <n-input-group style="width: fit-content;">
        <n-input v-model:value="searchTerm" autosize style="min-width: 200px;" :focusable="false" size="small"
          clearable></n-input>
        <n-button type="primary" size="small" @click="search" :focusable="false">搜索</n-button>
        <n-button type="warning" size="small" @click="clear" :focusable="false">清除</n-button>
      </n-input-group>
    </n-flex>
    <div id="graph" ref="graphRef"> </div>
    <div id="details" ref="detailsRef"> </div>
  </n-flex>
</template>


<script lang="ts" setup>
import { onMounted, ref, onUnmounted, watch, reactive } from "vue";
import { debounce } from "lodash-es"
// @ts-expect-error: Could not find differentialColorMapper for module 'd3-flame-graph'
import { flamegraph, differentialColorMapper, offCpuColorMapper, defaultFlamegraphTooltip } from "d3-flame-graph"
import { type FlameGraph } from "d3-flame-graph"
import * as d3 from "d3";
import exampleData from "./stacks.min.json"
import { NFlex, NInputGroup, NInput, NButton, NCheckbox, NInputNumber, NSelect } from "naive-ui";

const graphRef = ref<HTMLElement>()
const detailsRef = ref<HTMLElement>()
const graph = ref<FlameGraph>(flamegraph())
const searchTerm = ref("")

const graphConfig = reactive({
  isInverted: false,
  isSelfValue: false,
  isComputeDelta: false,
  layerHeight: 24,
  colorMapper: 0,
})

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function myColorMapper1(d: any, originalColor: string) {
  if (d.highlight) return originalColor

  return `hsl(0 100% ${50 - 30 * ((d.x1 - d.x0))}%)`
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function myColorMapper2(d: any, originalColor: string) {
  if (d.highlight) return originalColor

  return `hsl(60 100% ${50 - 40 * ((d.x1 - d.x0))}%)`
}

const colorMappers = [null, differentialColorMapper, offCpuColorMapper, myColorMapper1, myColorMapper2]

const options = [
  { label: "默认", value: 0 },
  { label: "差分", value: 1 },
  { label: "OffCPU", value: 2 },
  { label: "红色", value: 3 },
  { label: "橙色", value: 4 },
]

let data = exampleData
let selection = d3.select("#" + graphRef.value?.id)
// const tip = defaultFlamegraphTooltip()
// tip.html(d=>{
//   // console.log('defaultFlamegraphTooltip', d)
//   return `name:${d.data.n} value:${d.data.v} delta: ${d.data.d}`;
// })

// @ts-expect-error: d has no type
function labelHander(d) {
  return `😎 name: ${d.data.name || d.data.n} 😉 value: ${d.data.v || d.data.value}` + (d.data.d ? ` 😊 delta: ${d.data.d || d.data.delta}` : '') + ` 😂 percentage: ${(100 * (d.x1 - d.x0)).toFixed(2)}%`;
}

const observe = new ResizeObserver((entries) => {
  console.log('resize:', "width:", entries[0].contentRect.width, "height:", entries[0].contentRect.height)

  debounce(() => {
    graph.value
      .height(entries[0].contentRect.height)
      .width(entries[0].contentRect.width)
      .selfValue(false)
    selection.selectAll("svg").remove();

    selection
      .datum(data)
      .call(graph.value);

  }, 600, { leading: false, trailing: true })()
})

function openData(e: DragEvent) {
  if (e.dataTransfer === null || e.dataTransfer.files.length === 0) return;
  console.log('open data', e.dataTransfer.files);
  const file = e.dataTransfer.files[0];

  const reader = new FileReader();
  reader.onload = (event) => {
    if (event.target === null) return;
    const json = JSON.parse(event.target.result as string);
    console.log('file json', json);
    data = json
    graph.value.update(json);
  }
  reader.readAsText(file);
}

watch(graphConfig, (newVal) => {
  graph.value
    .inverted(newVal.isInverted)
    .selfValue(newVal.isSelfValue)
    .computeDelta(newVal.isComputeDelta)
    .cellHeight(graphConfig.layerHeight)

  if (colorMappers[newVal.colorMapper] !== null)
    graph.value.setColorMapper(colorMappers[newVal.colorMapper])
  else
    graph.value.setColorMapper()
  // @ts-expect-error: can normally setColorMapper with no args
  graph.value.update()
})

function search() {
  console.log('search', searchTerm.value)
  graph.value.search(searchTerm.value)
}

function clear() {
  console.log('clear')
  graph.value.clear()
  searchTerm.value = ''
}


onMounted(() => {
  graph.value
    .height(graphRef.value?.clientHeight as number)
    .width(graphRef.value?.clientWidth as number)
    .cellHeight(graphConfig.layerHeight)
    .transitionDuration(300)
    .minFrameSize(0)
    .sort(true)
    .setDetailsElement(detailsRef.value as HTMLElement)
    .label(labelHander)

  console.log('defaultFlamegraphTooltip', defaultFlamegraphTooltip)


  selection = d3.select("#" + graphRef.value?.id)

  observe.observe(graphRef.value as HTMLElement)
})

onUnmounted(() => {
  console.log('unmounted')
  observe.disconnect();
  graph.value.destroy()
})

</script>

<style scoped>
#graph {
  height: calc(100% - 30px);
  flex: 1;
  overflow: hidden;
  padding: 0 4px;
}

#details {
  height: 30px;
}

.layerHeightInput {
  width: 80px;
  color: hsl(61, 100%, 50%);
}
</style>
