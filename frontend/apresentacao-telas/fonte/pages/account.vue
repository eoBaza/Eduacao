<script setup>
import { ref, onMounted } from 'vue'
import ThemeToggle from '../components/ThemeToggle.vue'
import { api } from '../api'

const usuario = ref(null)
const loading = ref(true)
const error = ref('')

async function carregarUsuario() {
  loading.value = true
  error.value = ''

  try {
    usuario.value = await api('/user/info/', {
      method: 'GET'
    })
  } catch (e) {
    console.error('Erro ao carregar usuário:', e)

    error.value = e.message || 'Não foi possível carregar os dados da conta.'
  } finally {
    loading.value = false
  }
}

function tipoConta(tipo) {
  const tipos = {
    F: 'Pessoa física',
    J: 'Instituição',
    M: 'Mista'
  }

  return tipos[tipo] ?? tipo ?? '—'
}

onMounted(() => {
  carregarUsuario()
})
</script>

<template>
  <main class="request-page">

    <header class="request-page-header">
      <a href="#/home" class="brand-name">
        Educ<span class="brand-accent">Ação</span>
      </a>

      <div class="header-actions">
        <a class="back-link" href="#/home">
          ← Voltar ao início
        </a>

        <ThemeToggle />
      </div>
    </header>

    <section
      class="request-page-panel"
      aria-labelledby="account-title"
    >

      <div class="account-intro">
        <span class="account-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <circle
              cx="12"
              cy="8"
              r="4"
              stroke="currentColor"
              stroke-width="1.5"
            />

            <path
              d="M4 21v-2a8 8 0 0 1 16 0v2"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
        </span>

        <div>
          <h1 id="account-title">Minha conta</h1>
          <p>Suas informações em um só lugar.</p>
        </div>
      </div>

      <!-- Carregando -->
      <p
        v-if="loading"
        class="account-notice"
      >
        Carregando informações...
      </p>

      <!-- Erro -->
      <p
        v-else-if="error"
        class="account-notice"
        role="alert"
      >
        {{ error }}
      </p>

      <!-- Dados -->
      <template v-else-if="usuario">

        <section
          class="account-section"
          aria-label="Dados da conta"
        >
          <h2>Dados da conta</h2>

          <dl class="account-fields">

            <div>
              <dt>Nome / instituição</dt>
              <dd>{{ usuario.nome || '—' }}</dd>
            </div>

            <div>
              <dt>E-mail</dt>
              <dd>{{ usuario.gmail || '—' }}</dd>
            </div>

            <div>
              <dt>Tipo de conta</dt>
              <dd>{{ tipoConta(usuario.tipo_usuario) }}</dd>
            </div>

            <div>
              <dt>CPF / CNPJ</dt>
              <dd>{{ usuario.cnpj_cpf || '—' }}</dd>
            </div>

          </dl>
        </section>

        <section
          class="account-section"
          aria-label="Endereço"
        >
          <h2>Endereço</h2>

          <dl class="account-fields">

            <div>
              <dt>CEP</dt>
              <dd>{{ usuario.cep || '—' }}</dd>
            </div>

            <div>
              <dt>Endereço</dt>
              <dd>{{ usuario.endereco || '—' }}</dd>
            </div>

            <div>
              <dt>Número</dt>
              <dd>{{ usuario.numero || '—' }}</dd>
            </div>

            <div>
              <dt>Complemento</dt>
              <dd>{{ usuario.complemento || '—' }}</dd>
            </div>

          </dl>
        </section>

      </template>

    </section>

  </main>
</template>

<style scoped>
.account-intro {
  display: flex;
  align-items: center;
  gap: 16px;
}

.account-intro h1 {
  margin: 0 0 6px;
}

.account-intro p {
  margin: 0;
  font-size: 13px;
  color: var(--palette-728168);
}

.account-icon {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: var(--palette-edf3e1);
  color: var(--palette-597547);
}

.account-icon svg {
  width: 26px;
  height: 26px;
}

/* Seções */

.account-section {
  margin-top: 32px;
}

.account-section + .account-section {
  margin-top: 30px;
  padding-top: 28px;
  border-top: 1px solid var(--palette-e7ebdf);
}

.account-section h2 {
  margin: 0 0 24px;
  font-family: Manrope, sans-serif;
  font-size: 16px;
  font-weight: 600;
}

/* Campos */

.account-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 64px;
  row-gap: 28px;
  margin: 0;
}

.account-fields > div {
  min-width: 0;
}

.account-fields dt {
  margin: 0 0 10px;
  font-size: 12px;
  color: var(--palette-728168);
}

.account-fields dd {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: var(--palette-253d33);
  overflow-wrap: anywhere;
}

/* Loading / erro */

.account-notice {
  margin: 26px 0;
  padding: 14px 16px;
  background: var(--palette-f7f8f2);
  border-radius: 10px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--palette-67765c);
}

/* Mobile */

@media (max-width: 540px) {
  .account-fields {
    grid-template-columns: 1fr;
    row-gap: 22px;
  }

  .account-intro {
    gap: 12px;
  }

  .account-icon {
    width: 46px;
    height: 46px;
  }

  .account-section {
    margin-top: 28px;
  }
}
</style>