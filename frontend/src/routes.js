import MainPage from '@/pages/MainPage.vue'
import NotFound from '@/pages/not-found.vue'

export const routes = [
  { path: '/', component: MainPage },
  { path: '/:path(.*)', component: NotFound }
]

export default routes
