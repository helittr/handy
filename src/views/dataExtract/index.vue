<template>
  <div class="enhanced-mermaid-editor">
    <div ref="editorRef" class="editor-container"></div>
    <div class="preview-container">
      <div class="mermaid-preview" ref="previewRef"></div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { keymap } from '@codemirror/view'
import { javascript } from '@codemirror/lang-javascript'
import { oneDark } from '@codemirror/theme-one-dark'
import { defaultKeymap, indentWithTab } from '@codemirror/commands'
import mermaid from 'mermaid'
import { debounce } from 'lodash-es'

// 响应式引用
const editorRef = ref<HTMLElement | null>(null)
const previewRef = ref<HTMLElement | null>(null)
const error = ref<string | null>(null)
let editorView: EditorView | null = null

// 初始化 Mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  flowchart: { useMaxWidth: true },
  suppressErrorRendering: true,
})

// 渲染图表函数
const renderDiagram = debounce(async () => {
  if (!previewRef.value || !editorView) return

  try {
    error.value = null
    const code = editorView.state.doc.toString()
    const { svg } = await mermaid.render('mermaid-diagram', code)
    previewRef.value.innerHTML = svg
  } catch (err) {
    error.value = `Render error: ${err instanceof Error ? err.message : String(err)}`
  }
}, 300)

// 初始化编辑器
onMounted(() => {
  if (!editorRef.value) return

  editorView = new EditorView({
    doc: `graph TD
  A[Start] --> B(Process)
  B --> C{Decision}
  C -->|Yes| D[Result 1]
  C -->|No| E[Result 2]`,
    extensions: [
      basicSetup,
      keymap.of([...defaultKeymap, indentWithTab]),
      javascript(),
      oneDark,
      EditorView.updateListener.of(update => {
        if (update.docChanged) {
          renderDiagram()
        }
      })
    ],
    parent: editorRef.value
  })

  // 初始渲染
  renderDiagram()
})

// 清理编辑器实例
onBeforeUnmount(() => {
  if (editorView) {
    editorView.destroy()
  }
})
</script>

<style scoped>
.enhanced-mermaid-editor {
  display: flex;
  height: 100%;
  overflow: hidden;
  background: #282c34;
}

.editor-container {
  flex: 1;
  height: 100%;
  overflow: hidden;
  font-size: 16px;
}

.preview-container {
  flex: 1;
  height: 100%;
  padding: 16px;
  overflow: auto;
  background: #282c34;
  color: white;
}

.mermaid-preview {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
  padding: 8px 12px;
  border-radius: 4px;
  margin-top: 10px;
  font-size: 14px;
}
</style>
