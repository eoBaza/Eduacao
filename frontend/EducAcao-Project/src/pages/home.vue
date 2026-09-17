<script setup>
import ThemeToggle from '../components/ThemeToggle.vue'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { api } from '../api'

const props = defineProps({ mine: Boolean })
const emit = defineEmits(['logout'])
const requests = ref([])
const loading = ref(true)
const error = ref('')
const search = ref('')
const menu = ref(null)
function closeMenu() { if (menu.value) menu.value.open = false }
function closeOutside(event) { if (!menu.value?.contains(event.target)) closeMenu() }
function closeOnEscape(event) { if (event.key === 'Escape' && menu.value?.open) { closeMenu(); menu.value.querySelector('summary').focus() } }
function openRequest() { closeMenu(); window.location.hash = '/solicitacao/nova' }
let controller
const isOpen = (request) => request.status === 'Criado Por Requerente'
const children = (request) => request.quantidade_meninas + request.quantidade_meninos
const visibleRequests = computed(() => requests.value.filter((request) => {
  const term = search.value.trim().toLocaleLowerCase('pt-BR')
  const matches = `solicitação ${request.id} instituição ${request.id_user_requerente} ${JSON.stringify(request.lista_itens)}`.toLocaleLowerCase('pt-BR').includes(term)
  return matches && (props.mine || isOpen(request))
}))
const dateLabel = (date) => new Date(date).toLocaleDateString('pt-BR')
async function loadRequests() {
  loading.value = true
  error.value = ''

  try {
    const endpoint = props.mine
      ? '/solicitacao/minha-solicitacao/'
      : '/solicitacao/'

    const data = await api(endpoint)

    if (!Array.isArray(data)) {
      throw new Error('A API não retornou uma lista de solicitações.')
    }

    requests.value = data.sort(
      (a, b) => new Date(b.dt_criada) - new Date(a.dt_criada)
    )

  } catch (e) {
    console.error('Erro ao carregar solicitações:', e)

    error.value =
      'Não foi possível carregar as solicitações. Tente novamente.'

  } finally {
    loading.value = false
  }
}
onMounted(() => {
  loadRequests()
  document.addEventListener('click', closeOutside)
  document.addEventListener('keydown', closeOnEscape)
})
onUnmounted(() => {
  controller?.abort()
  document.removeEventListener('click', closeOutside)
  document.removeEventListener('keydown', closeOnEscape)
})
</script>

<template>
  <div class="home-shell">
    <header class="app-header">
      <div class="header-start">
      <details ref="menu" class="nav-dropdown">
        <summary aria-label="Abrir menu de navegação"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></summary>
        <nav aria-label="Navegação principal">
          <a href="#/home" :aria-current="!mine ? 'page' : undefined" @click="closeMenu">Início</a>
          <a href="#/minha-conta" @click="closeMenu">Minha conta</a>
          <a href="#/minhas-solicitacoes" :aria-current="mine ? 'page' : undefined" @click="closeMenu">Minhas solicitações</a>
          <button @click="openRequest">Abrir solicitação</button>
          <button class="logout-option" @click="emit('logout')">Sair da conta</button>
        </nav>
      </details>
      <a class="brand-name" href="#/home" aria-label="EducAção — início">
        <span class="brand-symbol" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M12 6.5C9 4.8 6 4.5 3 5v14c3-.5 6-.2 9 1.5 3-1.7 6-2 9-1.5V5c-3-.5-6-.2-9 1.5Zm0 0v14" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></span>
        <span>Educ<span class="brand-accent">Ação</span></span>
      </a>
      </div>
      <div class="header-actions"><button class="primary-link create-button" @click="openRequest"><span aria-hidden="true">＋</span> Abrir solicitação</button><ThemeToggle /></div>
    </header>

    <main class="home-content">
      <section v-if="!mine" class="welcome-panel" aria-labelledby="home-title">
        <div>
          <p class="eyebrow">BOAS-VINDAS AO EDUCAÇÃO</p>
          <h1 id="home-title">Venha ajudar apoiando<br /><span>quem precisa de material escolar.</span></h1>
          <p>Uma pequena contribuição pode fazer parte de uma grande conquista. Encontre uma solicitação aberta e conheça a lista de materiais.</p>
          <a class="primary-link" href="#requests" @click.prevent="$refs.requestsSection.scrollIntoView({ behavior: 'smooth' })">Explorar solicitações <span aria-hidden="true">↓</span></a>
        </div>
        <div class="school-art" aria-hidden="true"><span class="art-orbit"></span><span class="art-book"></span><span class="art-pencil"></span><span class="art-star">✳</span></div>
      </section>

      <section v-else class="my-requests-heading"><p class="eyebrow">SUAS AÇÕES NO EDUCAÇÃO</p><h1>Minhas solicitações</h1><p>Acompanhe as listas que você criou e a situação de cada pedido.</p></section>
      <div class="home-columns">
        <section id="requests" ref="requestsSection" class="requests-section" aria-labelledby="requests-title" :aria-busy="loading">
          <div class="section-heading"><div><p class="eyebrow">{{ mine ? 'SEUS PEDIDOS' : 'CADA MATERIAL CONTA' }}</p><h2 id="requests-title">{{ mine ? 'Solicitações que criei' : 'Solicitações abertas' }}</h2></div><button class="quiet-button" :disabled="loading" @click="loadRequests">Atualizar ↻</button></div>
          <div class="request-filters">
            <label class="search-box"><span class="sr-only">Buscar solicitação, instituição ou material</span><input v-model="search" type="search" placeholder="Buscar solicitação ou material" /></label>

          </div>
          <div v-if="loading" class="list-state" role="status"><span class="spinner"></span><p>Buscando solicitações…</p></div>
          <div v-else-if="error" class="list-state" role="alert"><h3>Vamos tentar de novo?</h3><p>{{ error }}</p><button class="quiet-button" @click="loadRequests">Tentar novamente</button></div>
          <div v-else-if="!visibleRequests.length" class="list-state" role="status"><span class="empty-symbol" aria-hidden="true">≡</span><h3>{{ search.trim() ? 'Nenhuma solicitação encontrada' : (mine ? 'Você ainda não criou solicitações' : 'Nenhuma solicitação aberta no momento') }}</h3><p>{{ search.trim() ? 'Tente buscar outro material ou solicitação.' : (mine ? 'Use Abrir solicitação para cadastrar sua primeira lista de materiais.' : 'Novos pedidos de outras instituições aparecerão aqui assim que forem cadastrados.') }}</p></div>
          <div v-else class="request-list">
            <article v-for="request in visibleRequests" :key="request.id" class="request-card">
              <div class="request-meta"><span>Solicitação #{{ request.id }}</span><span class="status-badge" :class="{ open: isOpen(request) }">{{ isOpen(request) ? 'Aguardando apoio' : request.status }}</span></div>
              <h3>Lista de materiais · Instituição #{{ request.id_user_requerente }}</h3>
              <p class="request-description">{{ children(request) }} crianças · {{ request.lista_itens.length }} itens na lista</p>
              <a class="request-details-link" :href="`#/solicitacao/${request.id}`" :aria-label="`Ver solicitação ${request.id}`">Ver solicitação <span aria-hidden="true">→</span></a>
              <p class="request-date">Publicada em {{ dateLabel(request.dt_criada) }}</p>
            </article>
          </div>
        </section>

      </div>
      <footer class="home-footer">Juntos, levando material escolar a quem precisa.</footer>
    </main>

  </div>
</template>

<style scoped>
.home-shell{min-height:100svh}.app-header{background:var(--palette-fff);border-bottom:1px solid var(--palette-e3e8dc);padding:20px max(24px,calc((100vw - 1120px)/2));display:flex;align-items:center;justify-content:space-between;gap:16px}.app-header .brand-name{font-size:25px;text-decoration:none}.app-header .brand-symbol{width:36px;height:36px;border-radius:11px}.current-page{color:var(--palette-35583e);text-decoration:none;border-bottom:2px solid var(--palette-718e51);padding:14px 0}.quiet-button{background:none;border:0;color:var(--palette-4c6545);font-size:13px;min-height:44px;padding:10px 4px}.quiet-button:disabled{opacity:.5;cursor:wait}.home-content{max-width:1168px;margin:auto;padding:36px 24px}.welcome-panel{background:var(--palette-eaf0df);border:1px solid var(--palette-e0e7d3);border-radius:20px;padding:36px 40px;display:flex;align-items:center;justify-content:space-between;gap:28px;overflow:hidden}.eyebrow{font-size:10px!important;font-weight:650;letter-spacing:1.7px;color:var(--palette-61754e);margin:0 0 16px!important}.welcome-panel h1{font-size:36px;line-height:1.25;font-weight:600;letter-spacing:-1.5px}.welcome-panel h1 span{color:var(--palette-728650)}.welcome-panel p{font-size:14px;line-height:1.8;max-width:490px;color:var(--palette-67745e)}.primary-link{display:inline-flex;gap:24px;align-items:center;background:#2f513e;color:#fff;text-decoration:none;padding:14px 19px;border-radius:9px;font-size:13px;margin-top:12px;min-height:48px}.school-art{position:relative;width:220px;height:200px;flex-shrink:0}.art-orbit{position:absolute;width:190px;height:190px;inset:0;border-radius:50%;border:1px solid #cbd6b9;background:#e1e9d3}.art-book{position:absolute;width:115px;height:145px;border-radius:7px 14px 14px 7px;background:#6a8250;border-left:10px solid #4b653b;transform:rotate(-14deg);left:27px;top:29px;box-shadow:5px 6px 0 #fafbf3,8px 9px 0 #bfcbaa}.art-book:after{content:'';position:absolute;width:56px;height:2px;background:#d4dfbd;top:40px;left:20px;box-shadow:0 10px 0 #d4dfbd}.art-pencil{position:absolute;width:18px;height:145px;background:#ceb976;transform:rotate(24deg);right:33px;top:54px;border-radius:4px 4px 9px 9px;border-bottom:14px solid #40533a}.art-star{position:absolute;right:5px;top:0;font-size:52px;color:#8fa569}.home-columns{margin-top:36px}.section-heading{display:flex;justify-content:space-between;gap:12px;align-items:center}.section-heading .eyebrow{font-size:9px!important;margin-bottom:8px!important}h2{font-family:Manrope,sans-serif;font-size:21px;letter-spacing:-.7px;margin:0}h3{font-size:15px;line-height:1.5;margin:12px 0}.request-filters{display:flex;gap:10px;margin:22px 0}.search-box{flex:1;min-width:0}.request-filters input,.request-filters select{width:100%;min-height:46px;padding:12px;border:1px solid var(--palette-dfe5d8);border-radius:8px;color:var(--palette-42563a);background:var(--palette-fff);font:inherit;font-size:14px}.request-filters select:focus-visible{outline:3px solid #719d4b;outline-offset:2px}.list-state{background:var(--palette-fff);border:1px dashed var(--palette-d9e0cf);border-radius:14px;padding:40px 24px;text-align:center}.list-state p{font-size:13px;color:var(--palette-73806a);line-height:1.8;max-width:350px;margin:12px auto}.list-state .spinner{display:inline-block;border-color:var(--palette-dae3cf);border-top-color:var(--palette-557144)}.empty-symbol{display:inline-grid;place-items:center;width:48px;height:48px;border-radius:13px;background:var(--palette-eff3e8);color:var(--palette-728a55);font-size:30px}.request-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start}.request-card{background:var(--theme-surface);border:1px solid var(--palette-e2e7d9);border-radius:14px;padding:23px;overflow-wrap:anywhere}.request-meta{display:flex;gap:12px;justify-content:space-between;align-items:center;font-size:11px;color:var(--palette-7c8575)}.status-badge{background:var(--palette-f1f2ed);border-radius:20px;padding:6px 10px;font-size:10px}.status-badge.open{background:var(--palette-edf3e1);color:var(--palette-567037)}.request-description,.request-date{font-size:12px;color:var(--palette-7c8575)}.request-date{font-size:10px;margin-bottom:0}.home-footer{text-align:center;font-size:11px;color:var(--palette-859077);padding:40px 0 5px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
@media(max-width:850px){.home-columns{grid-template-columns:1fr}.school-art{transform:scale(.8);width:170px}.welcome-panel{padding:30px}.welcome-panel h1{font-size:30px}}
@media(max-width:540px){.app-header{padding:15px 18px}.app-header .brand-name{font-size:22px;gap:8px}.home-content{padding:22px 16px}.welcome-panel{padding:27px 23px}.welcome-panel h1{font-size:28px}.school-art{display:none}h2{font-size:19px}.request-filters{flex-direction:column}.request-filters input,.request-filters select{font-size:16px}.request-card{padding:18px}.request-meta{align-items:start}.status-badge{max-width:160px}.home-columns{gap:24px}}

.header-start{display:flex;align-items:center;gap:18px;min-width:0}
.nav-dropdown{position:relative}
.nav-dropdown summary{display:grid;place-items:center;width:44px;height:44px;cursor:pointer;list-style:none;border:1px solid var(--palette-e3e8dc);border-radius:10px;background:var(--palette-fafbf7)}
.nav-dropdown summary::-webkit-details-marker{display:none}
.nav-dropdown summary:focus-visible{outline:3px solid #719d4b;outline-offset:3px}
.nav-dropdown nav{position:absolute;left:0;top:54px;z-index:10;display:grid;min-width:230px;padding:8px;background:var(--palette-fff);border:1px solid var(--palette-e3e8dc);border-radius:12px;box-shadow:0 12px 35px #253d331a}
.nav-dropdown nav a,.nav-dropdown nav button{display:flex;align-items:center;min-height:46px;padding:10px 13px;border:0;background:none;text-decoration:none;text-align:left;color:var(--palette-405738);font:inherit;font-size:13px;border-radius:6px}
.nav-dropdown nav a:hover,.nav-dropdown nav button:hover{background:var(--palette-f0f4e9)}
.nav-dropdown .logout-option{border-top:1px solid var(--palette-e8ecdf);border-radius:0;margin-top:5px}
.create-button{border:0;margin:0;gap:8px;white-space:nowrap}









@media(max-width:650px){.request-list{grid-template-columns:1fr}.app-header{flex-wrap:wrap;gap:12px}.header-start{gap:9px}.create-button{font-size:12px;padding:12px;min-height:44px}.app-header .brand-name{font-size:20px}.app-header .brand-symbol{display:none}.welcome-panel h1{font-size:27px}}
@media(max-width:360px){.create-button{width:100%;justify-content:center}}
.request-details-link{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:46px;margin:18px 0 8px;padding:12px 18px;border:1px solid #2f513e;border-radius:9px;background:#2f513e;color:#fff;font-size:13px;font-weight:600;text-decoration:none;transition:background .15s,border-color .15s}
.request-details-link:hover{background:#203f2d;border-color:#203f2d}
.request-details-link:active{background:#182f22}
.request-details-link:focus-visible{outline:3px solid #719d4b;outline-offset:3px}
@media(max-width:540px){.request-details-link{width:100%}}
.my-requests-heading{padding:12px 0}.my-requests-heading h1{font-size:30px}.my-requests-heading>p:last-child{font-size:14px;line-height:1.7;color:var(--palette-67745e)}
</style>
