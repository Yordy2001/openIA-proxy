import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  esbuild: {
    loader: 'jsx',
    include: /src\/.*\.[jt]sx?$/,
    exclude: []
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:7000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/analyze': 'http://localhost:7000',
      '/chat': 'http://localhost:7000',
      '/sessions': 'http://localhost:7000',
      '/health': 'http://localhost:7000',
      '/extract': 'http://localhost:7000',
      '/edit': 'http://localhost:7000',
      '/download': 'http://localhost:7000'
    }
  },
  build: {
    outDir: 'build',
    sourcemap: true
  },
  define: {
    'process.env': process.env
  },
  envPrefix: 'REACT_APP_'
}) 