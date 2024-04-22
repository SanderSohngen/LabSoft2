import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  server: {
	host: '0.0.0.0'
	}
  return {
    define: {
      'process.env': env
    },
    plugins: [react()],
  }
})
