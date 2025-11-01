<template>
  <div ref="swaggerContainer" class="swagger-container"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import SwaggerUI from 'swagger-ui-dist/swagger-ui-es-bundle'
import 'swagger-ui-dist/swagger-ui.css'

const swaggerContainer = ref(null)

onMounted(() => {
  SwaggerUI({
    domNode: swaggerContainer.value,
    url: 'http://localhost:8001/openapi.json',
    presets: [
      SwaggerUI.presets.apis,
      SwaggerUI.SwaggerUIStandalonePreset
    ]
  })
})
</script>
