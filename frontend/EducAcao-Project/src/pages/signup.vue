<script setup>
import { reactive, ref } from 'vue'
import { api } from '../api'
const form = reactive({ nome: '', gmail: '', tipo_usuario: 'F', cnpj_cpf: '', senha: '', confirmation: '', cep: '', numero: '', complemento: '' })
const busy = ref(false)
const error = ref('')
const done = ref(false)
async function submit() {
  if (busy.value) return
  error.value = ''
  if (form.senha !== form.confirmation) { error.value = 'As senhas não coincidem.'; return }
  busy.value = true
  try {
    const query = new URLSearchParams({ cep: form.cep.replace(/\D/g, ''), numero: form.numero, complemento: form.complemento })
    await api(`/user/signup/?${query}`, { method: 'POST', body: JSON.stringify({ nome: form.nome.trim(), gmail: form.gmail.trim(), tipo_usuario: form.tipo_usuario, cnpj_cpf: form.cnpj_cpf.replace(/\D/g, ''), senha: form.senha }) })
    form.senha = form.confirmation = ''
    done.value = true
  } catch (e) { error.value = e.message } finally { busy.value = false }
}
</script>
<template>
  <section class="login-panel signup-panel">
    <h1>{{ done ? 'Conta criada!' : 'Faça parte do EducAção' }}</h1>
    <p class="login-description">{{ done ? 'Entre com seu e-mail e senha para começar.' : 'Cadastre-se para solicitar materiais ou apoiar uma instituição.' }}</p>
    <form v-if="!done" @submit.prevent="submit">
      <fieldset :disabled="busy">
        <div class="field"><label for="signup-type">Tipo de conta</label><select id="signup-type" v-model="form.tipo_usuario"><option value="F">Pessoa física · quero ajudar</option><option value="J">Instituição · solicitar ou ajudar</option></select></div>
        <div class="field"><label for="signup-name">{{ form.tipo_usuario === 'J' ? 'Nome da instituição' : 'Nome completo' }}</label><input id="signup-name" v-model="form.nome" autocomplete="name" maxlength="255" required /></div>
        <div class="field"><label for="signup-document">{{ form.tipo_usuario === 'J' ? 'CNPJ' : 'CPF' }}</label><input id="signup-document" v-model="form.cnpj_cpf" inputmode="numeric" :pattern="form.tipo_usuario === 'J' ? '[0-9]{14}' : '[0-9]{11}'" placeholder="Somente números" required /></div>
        <div class="field"><label for="signup-email">E-mail</label><input id="signup-email" v-model="form.gmail" type="email" autocomplete="email" required /></div>
        <div class="form-grid"><div class="field"><label for="signup-password">Senha</label><input id="signup-password" v-model="form.senha" type="password" autocomplete="new-password" required /></div><div class="field"><label for="signup-confirm">Confirmar senha</label><input id="signup-confirm" v-model="form.confirmation" type="password" autocomplete="new-password" required /></div></div>
        <h2 class="form-subtitle">Endereço</h2>
        <div class="form-grid"><div class="field"><label for="signup-cep">CEP</label><input id="signup-cep" v-model="form.cep" autocomplete="postal-code" inputmode="numeric" pattern="[0-9]{5}-?[0-9]{3}" placeholder="00000-000" required /></div><div class="field"><label for="signup-number">Número</label><input id="signup-number" v-model="form.numero" required /></div></div>
        <div class="field"><label for="signup-complement">Complemento (opcional)</label><input id="signup-complement" v-model="form.complemento" /></div>
        <p v-if="error" role="alert" class="error-message">{{ error }}</p>
        <button class="submit-button" type="submit">{{ busy ? 'Criando conta…' : 'Criar conta' }}</button>
      </fieldset>
    </form>
    <a class="back-link" href="#/login">{{ done ? 'Entrar na minha conta' : 'Já tenho conta · entrar' }}</a>
  </section>
</template>
