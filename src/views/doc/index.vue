<template>
    <iframe ref="docRef" src="/docs/" class="h-full w-full"></iframe>
    <!-- <div id="doc" class="w-full h-full"></div> -->
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { useGlobalStateStore } from '@/stores/globaleState.ts'

const globaleStateStore = useGlobalStateStore()
const docRef = ref<HTMLIFrameElement>()

watch(globaleStateStore, () => {
    const msg = { type: 'THEME', isDark: globaleStateStore.isDark }
    console.log("postMessage", msg)
    if (docRef.value) {
        docRef.value.contentWindow?.postMessage(msg, "*")
    }
})

// onMounted(() => {
//     console.log('docRef', typeof docRef)
//     const postMsg = () => {
//         if (docRef.value) {
//             docRef.value.contentWindow?.postMessage({ type: 'THEME', theme: 'dark' }, "*")
//         }
//         setTimeout(postMsg, 1000)
//     }
//     postMsg()
// })

</script>


<style lang="css" module></style>