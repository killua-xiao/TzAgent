import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  css: {
    preprocessorOptions: {
      less: {
        modifyVars: {
          '@btn-height-default': '40px',
          '@primary-color': '#1E6FEB',
          '@text-color': '#0F1421'
        },
        javascriptEnabled: true
      }
    }
  }
})