<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { api } from '../api'
const form = reactive({ nome: '', gmail: '', id_tipo_usuario: '', cnpj_cpf: '', senha: '', confirmation: '', cep: '', numero: '', complemento: '' })
const accountTypes = ref([])
const typesLoading = ref(true)
const typesError = ref('')
const selectedType = computed(() => accountTypes.value.find(type => type.id === form.id_tipo_usuario))
const isInstitution = computed(() => selectedType.value?.nome.normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim().toLowerCase() === 'juridico')
async function loadAccountTypes() {
  typesLoading.value = true
  typesError.value = ''
  try {
    const data = await api('/user/tipo_usuario/')
    if (!Array.isArray(data) || data.some(type => !Number.isInteger(type.id) || typeof type.nome !== 'string')) {
      throw new Error('Não foi possível carregar os tipos de conta.')
    }
    accountTypes.value = data
    if (!data.length) typesError.value = 'Nenhum tipo de conta disponível no momento.'
    if (!data.some(type => type.id === form.id_tipo_usuario)) form.id_tipo_usuario = ''
  } catch (e) {
    accountTypes.value = []
    typesError.value = e.message
  } finally { typesLoading.value = false }
}
onMounted(loadAccountTypes)
const busy = ref(false)
const error = ref('')
const done = ref(false)
async function submit() {
  if (busy.value) return
  error.value = ''
  if (typesLoading.value || !selectedType.value) { error.value = 'Selecione um tipo de conta disponível.'; return }
  if (form.senha !== form.confirmation) { error.value = 'As senhas não coincidem.'; return }
  busy.value = true
  try {
    const query = new URLSearchParams({ cep: form.cep.replace(/\D/g, ''), numero: form.numero, complemento: form.complemento })
    await api(`/user/signup/?${query}`, { method: 'POST', body: JSON.stringify({ nome: form.nome.trim(), gmail: form.gmail.trim(), id_tipo_usuario: form.id_tipo_usuario, cnpj_cpf: form.cnpj_cpf.replace(/\D/g, ''), senha: form.senha }) })
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
        <div class="field">
          <label for="signup-type">Tipo de conta</label>
          <select id="signup-type" v-model="form.id_tipo_usuario" :disabled="typesLoading || !accountTypes.length" :aria-busy="typesLoading" required>
            <option disabled value="">{{ typesLoading ? 'Carregando tipos de conta…' : 'Selecione o tipo de conta' }}</option>
            <option v-for="type in accountTypes" :key="type.id" :value="type.id">{{ type.nome }}{{ type.descricao ? ` · ${type.descricao}` : '' }}</option>
          </select>
          <p v-if="typesError" role="alert" class="error-message">{{ typesError }}</p>
          <button v-if="typesError" type="button" @click="loadAccountTypes" :disabled="typesLoading">Tentar novamente</button>
        </div>
        <div class="field"><label for="signup-name">{{ isInstitution ? 'Nome da instituição' : 'Nome completo' }}</label><input id="signup-name" v-model="form.nome" :autocomplete="isInstitution ? 'organization' : 'name'" maxlength="255" required /></div>
        <div class="field"><label for="signup-document">{{ isInstitution ? 'CNPJ' : 'CPF' }}</label><input id="signup-document" v-model="form.cnpj_cpf" inputmode="numeric" :pattern="isInstitution ? '[0-9]{14}' : '[0-9]{11}'" placeholder="Somente números" required /></div>
        <div class="field"><label for="signup-email">E-mail</label><input id="signup-email" v-model="form.gmail" type="email" autocomplete="email" required /></div>
        <div class="form-grid"><div class="field"><label for="signup-password">Senha</label><input id="signup-password" v-model="form.senha" type="password" autocomplete="new-password" required /></div><div class="field"><label for="signup-confirm">Confirmar senha</label><input id="signup-confirm" v-model="form.confirmation" type="password" autocomplete="new-password" required /></div></div>
        <h2 class="form-subtitle">Endereço</h2>
        <div class="form-grid"><div class="field"><label for="signup-cep">CEP</label><input id="signup-cep" v-model="form.cep" autocomplete="postal-code" inputmode="numeric" pattern="[0-9]{5}-?[0-9]{3}" placeholder="00000-000" required /></div><div class="field"><label for="signup-number">Número</label><input id="signup-number" v-model="form.numero" required /></div></div>
        <div class="field"><label for="signup-complement">Complemento (opcional)</label><input id="signup-complement" v-model="form.complemento" /></div>
        <p v-if="error" role="alert" class="error-message">{{ error }}</p>
        <button class="submit-button" type="submit" :disabled="typesLoading || !selectedType">{{ busy ? 'Criando conta…' : 'Criar conta' }}</button>
      </fieldset>
    </form>
    <a class="back-link" href="#/login">{{ done ? 'Entrar na minha conta' : 'Já tenho conta · entrar' }}</a>
  </section>
</template>
