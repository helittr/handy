import '@csstools/normalize.css'

import './utils/icon.ts'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 添加全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.log('Vue instance:', instance)
  console.log('Error info:', info)
}

app.use(createPinia())
app.use(router)

app.mount('#app')
