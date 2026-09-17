<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ForgotPassword from './forgot-password.vue'
import HomePage from './home.vue'
import SignupPage from './signup.vue'
import RequestPage from './request.vue'
import AccountPage from './account.vue'
import ThemeToggle from '../components/ThemeToggle.vue'

const home = ref(false)
const account = ref(false)
const myRequests = ref(false)
const signup = ref(false)
const requestPage = ref(false)
const requestId = ref(null)
const routeKey = ref('')
function logout() {
  sessionStorage.removeItem('educacao.session')
  home.value = false
  window.location.hash = '/login'
}

const recovering = ref(window.location.hash === '#/esqueci-minha-senha')
function updateScreen() {
  routeKey.value = window.location.hash
  account.value = window.location.hash === '#/minha-conta' && Boolean(sessionStorage.getItem('educacao.session'))
  if (window.location.hash === '#/minha-conta' && !account.value) window.location.hash = '/login'
  signup.value = window.location.hash === '#/cadastro'
  const match = window.location.hash.match(/^#\/solicitacao\/(nova|[0-9]+)$/)
  requestPage.value = Boolean(match) && Boolean(sessionStorage.getItem('educacao.session'))
  requestId.value = match && match[1] !== 'nova' ? match[1] : null
  if (match && !requestPage.value) window.location.hash = '/login'
  myRequests.value = window.location.hash === '#/minhas-solicitacoes'
  home.value = ['#/home', '#/minhas-solicitacoes'].includes(window.location.hash) && Boolean(sessionStorage.getItem('educacao.session'))
  if (['#/home', '#/minhas-solicitacoes'].includes(window.location.hash) && !home.value) window.location.hash = '/login'
  recovering.value = window.location.hash === '#/esqueci-minha-senha'
  password.value = ''
  error.value = ''
  showPassword.value = false
  document.title = requestPage.value ? 'Solicitação | EducAção' : signup.value ? 'Criar conta | EducAção' : home.value ? (myRequests.value ? 'Minhas solicitações | EducAção' : 'Início | EducAção') : recovering.value ? 'Recuperar senha | EducAção' : 'Entrar | EducAção'
  if (account.value) document.title = 'Minha conta | EducAção'
}
onMounted(() => {
  updateScreen()
  window.addEventListener('hashchange', updateScreen)
})
onUnmounted(() => window.removeEventListener('hashchange', updateScreen))

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function login() {
  if (loading.value) return
  error.value = ''
  loading.value = true
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 15000)

  try {
    const response = await fetch('/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gmail: email.value.trim(), senha: password.value }),
      signal: controller.signal,
      cache: 'no-store',
    })
    const data = await response.json().catch(() => ({}))
    if (!response.ok || typeof data?.Session_Code !== 'string' || !data.Session_Code) {
      error.value = response.status === 401
        ? 'E-mail ou senha incorretos.'
        : response.status === 422
          ? 'Confira o e-mail e preencha sua senha.'
          : 'Não foi possível entrar agora. Tente novamente em instantes.'
      return
    }
    sessionStorage.setItem('educacao.session', data.Session_Code)
    password.value = ''
    window.location.hash = '/home'
    updateScreen()
  } catch {
    error.value = 'Não foi possível conectar ao servidor. Tente novamente.'
  } finally {
    clearTimeout(timeout)
    loading.value = false
  }
}
</script>

<template>
  <HomePage v-if="home" :key="routeKey" :mine="myRequests" @logout="logout" />
  <AccountPage v-else-if="account" />
  <RequestPage v-else-if="requestPage" :key="routeKey" :id="requestId" />
  <main v-else class="page-shell">
    <header class="login-brand" aria-label="EducAção">
      <div class="brand-name">
        <span class="brand-symbol" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 6.5C9 4.8 6 4.5 3 5v14c3-.5 6-.2 9 1.5 3-1.7 6-2 9-1.5V5c-3-.5-6-.2-9 1.5Zm0 0v14" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
        </span>
        <span>Educ<span class="brand-accent">Ação</span></span>
      </div>
      <p>Juntos, levando material escolar a quem precisa.</p>
      <ThemeToggle class="login-theme-toggle" />
    </header>
    <SignupPage v-if="signup" />
    <ForgotPassword v-else-if="recovering" />
    <section v-else class="login-panel" aria-labelledby="login-title">

          <h1 id="login-title">Que bom ter você aqui.</h1>
          <p class="login-description">Entre na sua conta para continuar.</p>
          <form @submit.prevent="login">
            <div class="field">
              <label for="email">E-mail</label>
              <input id="email" v-model="email" type="email" name="email" placeholder="seuemail@exemplo.com" autocomplete="username" inputmode="email" autocapitalize="none" :disabled="loading" required />
            </div>
            <div class="field">
              <label for="password">Senha</label>
              <div class="password-field">
                <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'" name="password" placeholder="Digite sua senha" autocomplete="current-password" :disabled="loading" required />
                <button class="password-toggle" type="button" :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'" :aria-pressed="showPassword" @click="showPassword = !showPassword">
                  <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="2.5" stroke="currentColor" stroke-width="1.6"/><path v-if="showPassword" d="m4 3 16 18" stroke="currentColor" stroke-width="1.6"/></svg>
                </button>
              </div>
            </div>
            <a class="forgot-link" href="#/esqueci-minha-senha">Esqueci minha senha</a>
            <p v-if="error" class="error-message" role="alert">{{ error }}</p>
            <button class="submit-button" type="submit" :disabled="loading"><span>{{ loading ? 'Entrando…' : 'Entrar na minha conta' }}</span><span v-if="!loading" aria-hidden="true">↗</span><span v-else class="spinner" aria-hidden="true"></span></button>
          </form>
          <a class="back-link" href="#/cadastro">Não tem conta? Criar conta</a>

    </section>
  </main>
</template>
