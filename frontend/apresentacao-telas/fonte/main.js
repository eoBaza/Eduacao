import { createApp } from 'vue'
import App from './pages/index.vue'
import { api } from './api.js'
import './style.css'

// Login e recuperação usam fetch no original. Aqui nenhuma chamada sai da página.
window.fetch = async (path, options) => {
  try {
    if (typeof path !== 'string' || !path.startsWith('/api/')) throw new Error('Somente demonstração local.')
    return new Response(JSON.stringify(await api(path.slice(4), options)), { status: 200, headers: { 'Content-Type': 'application/json' } })
  } catch (error) {
    return new Response(JSON.stringify({ detail: error.message }), { status: 400 })
  }
}
if (!window.location.hash) window.location.hash = document.body.dataset.route || '/login'
document.documentElement.dataset.theme = 'light'
createApp(App).mount('#app')
