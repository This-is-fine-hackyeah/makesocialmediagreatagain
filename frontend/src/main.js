import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import '@/assets/styles/fonts.css'
import '@/assets/styles/main.css'
import '@/assets/styles/tailwind.css'
import App from '@/app.vue'
import { routes } from '@/routes.js'

import { Quasar } from 'quasar'
import 'quasar/src/css/index.sass'
import '@quasar/extras/material-icons/material-icons.css'

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PUBLIC_PATH),
  routes
})

const app = createApp(App)
app.use(router)
app.use(Quasar, {
  plugins: {}
})

app.mount('#app')
