import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',  // 允许所有主机访问
    port: 3000,       // 根据需要修改端口
    open: true,       // 自动打开浏览器
  },
})
