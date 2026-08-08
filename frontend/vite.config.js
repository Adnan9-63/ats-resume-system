import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server proxies /api calls to the FastAPI backend on :8000, so the
// frontend can just call fetch('/api/analyze') without hardcoding a full
// URL -- this makes deployment easier later too (swap the proxy target
// for an env var instead of changing every fetch call in the codebase).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
