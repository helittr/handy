import { dirname, resolve } from 'node:path'
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import { viteStaticCopy } from 'vite-plugin-static-copy'


const __dirname = dirname(fileURLToPath(import.meta.url))

const host = process.env.TAURI_DEV_HOST;
// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [vue(), tailwindcss(), viteStaticCopy({
    targets: [
      {
        src: 'docs/*.md',
        dest: 'docs'
      },
      {
        src: 'docs/.nojekyll',
        dest: 'docs'
      }
    ]
  })],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  clearScreen: false,
  server: {
    port: 1420,
    cors: true,
    strictPort: true,
    host: host || false,
    hmr: host
      ? {
        protocol: "ws",
        host,
        port: 1421,
      }
      : undefined,
    watch: {
      // 3. tell vite to ignore watching `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        nested: resolve(__dirname, 'docs/index.html'),
      },
    },
  },
})
