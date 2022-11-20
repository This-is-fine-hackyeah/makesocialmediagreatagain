import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import svgLoader from 'vite-svg-loader'
import { resolve } from 'path'

export default ({ mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) }

  return defineConfig({
    base: process.env.VITE_BASE_PUBLIC_PATH,
    plugins: [
      svgLoader(),
      vue()
    ],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      },
      dedupe: [
        'vue'
      ]
    }
  })
}
