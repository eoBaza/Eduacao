<script setup>
import { ref, onUnmounted } from 'vue'

const email = ref('')
const password = ref('')
const confirmation = ref('')
const visible = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const confirmationInput = ref(null)
let activeRequest

function validateConfirmation() {
  confirmationInput.value?.setCustomValidity(
    confirmation.value && confirmation.value !== password.value ? 'As senhas não coincidem.' : '',
  )
}

onUnmounted(() => activeRequest?.abort())

async function resetPassword() {
  if (loading.value) return
  validateConfirmation()
  if (password.value !== confirmation.value) {
    confirmationInput.value?.reportValidity()
    return
  }
  error.value = ''
  loading.value = true
  activeRequest = new AbortController()
  const timeout = setTimeout(() => activeRequest.abort(), 15000)
  try {
    const response = await fetch('/api/user/reset-password/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gmail: email.value.trim(), senha: password.value, confirma_senha: confirmation.value }),
      signal: activeRequest.signal,
    })
    const data = await response.json().catch(() => null)
    if (!response.ok || typeof data?.message !== 'string') {
      error.value = response.status === 404
        ? 'Não foi possível recuperar o acesso. Confira o e-mail informado.'
        : 'Não foi possível alterar sua senha. Tente novamente em instantes.'
      return
    }
    password.value = ''
    confirmation.value = ''
    success.value = true
  } catch {
    error.value = 'Não foi possível conectar ao servidor. Tente novamente.'
  } finally {
    clearTimeout(timeout)
    loading.value = false
  }
}
</script>

<template>
  <section class="login-panel" aria-labelledby="recovery-title">
    <template v-if="!success">
      <h1 id="recovery-title">Esqueceu sua senha?</h1>
      <p class="login-description">Informe seu e-mail e escolha uma nova senha.</p>
      <form @submit.prevent="resetPassword">
        <div class="field">
          <label for="recovery-email">E-mail</label>
          <input id="recovery-email" v-model="email" name="email" type="email" placeholder="seuemail@exemplo.com" autocomplete="username" inputmode="email" autocapitalize="none" :disabled="loading" required />
        </div>
        <div class="field">
          <label for="new-password">Nova senha</label>
          <input id="new-password" v-model="password" name="new-password" :type="visible ? 'text' : 'password'" placeholder="Digite sua nova senha" autocomplete="new-password" :disabled="loading" required @input="validateConfirmation" />
        </div>
        <div class="field">
          <label for="confirm-password">Confirmar senha</label>
          <input id="confirm-password" ref="confirmationInput" v-model="confirmation" name="confirm-password" :type="visible ? 'text' : 'password'" placeholder="Repita sua nova senha" autocomplete="new-password" :disabled="loading" required @input="validateConfirmation" />
        </div>
        <button class="visibility-button" type="button" :aria-pressed="visible" @click="visible = !visible">{{ visible ? 'Ocultar senhas' : 'Mostrar senhas' }}</button>
        <p v-if="error" class="error-message" role="alert">{{ error }}</p>
        <button class="submit-button" type="submit" :disabled="loading">
          <span>{{ loading ? 'Salvando…' : 'Salvar nova senha' }}</span>
          <span v-if="loading" class="spinner" aria-hidden="true"></span>
          <span v-else aria-hidden="true">↗</span>
        </button>
      </form>
    </template>
    <div v-else class="success-message" role="status">
      <span class="success-icon" aria-hidden="true">✓</span>
      <h1 id="recovery-title">Senha alterada!</h1>
      <p>Agora você pode entrar com sua nova senha.</p>
    </div>
    <a class="back-link" href="#/login">← Voltar para o login</a>
  </section>
</template>
