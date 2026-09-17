<script setup>
import ThemeToggle from '../components/ThemeToggle.vue'
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
const props = defineProps({ id: String })
const isNew = computed(() => !props.id)
const loading = ref(true)
const busy = ref(false)
const error = ref('')
const success = ref('')
const user = ref(null)
const request = ref(null)
const items = ref([])
const quantities = ref({})
const materialSearch = ref('')
const catalogOpen = ref(false)
const selectedIds = ref([])
const selectionMessage = ref('')
const normalize = (text) => String(text).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
const selectedItems = computed(() => selectedIds.value.map(id => items.value.find(item => item.id === id)).filter(Boolean))
const availableItems = computed(() => items.value.filter(item => !selectedIds.value.includes(item.id) && normalize(item.nome_item).includes(normalize(materialSearch.value.trim()))))
const totalUnits = computed(() => selectedItems.value.reduce((total, item) => total + (Number(quantities.value[item.id]) || 0), 0))
function addMaterial(item) {
  if (selectedIds.value.includes(item.id)) return
  selectedIds.value.push(item.id)
  quantities.value[item.id] = 1
  selectionMessage.value = `${item.nome_item} adicionado à lista.`
}
function removeMaterial(item) {
  selectedIds.value = selectedIds.value.filter(id => id !== item.id)
  delete quantities.value[item.id]
  selectionMessage.value = `${item.nome_item} removido da lista.`
}
const girls = ref(0)
const boys = ref(0)
const canJoin = computed(() => request.value && request.value.status === 'Criado Por Requerente' && !request.value.id_user_apoiador && request.value.id_user_requerente !== user.value?.id_usuario)
async function load() {
  loading.value = true
  error.value = ''
  try {
    user.value = await api('/user/info/')
    if (isNew.value) {
      if (user.value.tipo_usuario === 'J') items.value = await api('/list_itens')
    } else request.value = await api(`/solicitacao/${props.id}/`)
  } catch (e) { error.value = e.message } finally { loading.value = false }
}
async function publish() {
  if (busy.value) return
  error.value = ''
  const list = selectedItems.value.map(item => ({ id_item: item.id, quantidade: Number(quantities.value[item.id]) }))
  if (list.some(item => !Number.isInteger(item.quantidade) || item.quantidade < 1)) { error.value = 'Informe uma quantidade inteira maior que zero para cada material.'; return }
  if (!list.length) { error.value = 'Informe a quantidade de pelo menos um material.'; return }
  if (Number(girls.value) + Number(boys.value) < 1) { error.value = 'Informe pelo menos uma criança.'; return }
  busy.value = true
  try {
    const result = await api('/solicitacao/create/', { method: 'POST', body: JSON.stringify({ lista_itens: list, quantidade_meninas: Number(girls.value), quantidade_meninos: Number(boys.value) }) })
    window.location.hash = `/solicitacao/${result.id}`
  } catch (e) { error.value = e.message } finally { busy.value = false }
}
async function join() {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try {
    request.value = await api(`/solicitacao/${props.id}/participar/`, { method: 'POST' })
    success.value = 'Sua participação foi confirmada. Você agora é o apoiador desta solicitação!'
  } catch (e) { error.value = e.message } finally { busy.value = false }
}
onMounted(load)
</script>
<template>
  <main class="request-page">
    <header class="request-page-header"><a href="#/home" class="brand-name">Educ<span class="brand-accent">Ação</span></a><div class="header-actions"><a class="back-link" href="#/home">← Voltar ao início</a><ThemeToggle /></div></header>
    <section class="request-page-panel">
      <h1>{{ isNew ? 'Abrir solicitação' : `Solicitação #${id}` }}</h1>
      <p v-if="loading" role="status">Carregando informações…</p>
      <template v-else-if="isNew && user">
        <p v-if="user.tipo_usuario !== 'J'">A abertura de solicitações está disponível para contas de instituições. Você pode explorar as listas e participar como apoiador.</p>
        <form v-else @submit.prevent="publish">
          <p class="login-description">Selecione os materiais e informe quantas unidades sua instituição precisa.</p>
          <fieldset :disabled="busy">
            <h2 class="form-subtitle">Crianças atendidas</h2>
            <div class="form-grid"><div class="field"><label for="girls">Quantidade de meninas</label><input id="girls" v-model="girls" type="number" min="0" step="1" required /></div><div class="field"><label for="boys">Quantidade de meninos</label><input id="boys" v-model="boys" type="number" min="0" step="1" required /></div></div>
            <h2 class="form-subtitle">Lista de materiais</h2>
            <p v-if="!items.length">Nenhum material disponível no catálogo.</p>
            <template v-else>
              <div class="material-picker">
                <label for="material-search" class="picker-label">Adicionar material</label>
                <div class="picker-search"><input id="material-search" v-model="materialSearch" type="search" placeholder="Busque por caderno, lápis, borracha…" @keydown.enter.prevent @keydown.esc="catalogOpen = false; materialSearch = ''" /><button type="button" :aria-expanded="catalogOpen" aria-controls="material-results" @click="catalogOpen = !catalogOpen">{{ catalogOpen ? 'Fechar catálogo' : 'Ver catálogo' }}</button></div>
                <div v-if="catalogOpen || materialSearch.trim()" id="material-results" class="catalog-results">
                  <p class="catalog-count" role="status">{{ availableItems.length }} materiais disponíveis</p>
                  <ul v-if="availableItems.length" class="catalog-list">
                    <li v-for="item in availableItems" :key="item.id"><span>{{ item.nome_item }}</span><button type="button" :aria-label="`Adicionar ${item.nome_item}`" @click="addMaterial(item)">＋ Adicionar</button></li>
                  </ul>
                  <p v-else class="picker-hint">Nenhum material disponível para esta busca. Tente outro nome ou confira os itens já adicionados.</p>
                </div>
              </div>
              <p class="selection-announcement" role="status">{{ selectionMessage }}</p>
              <div class="selected-heading"><h3>Sua lista</h3><span>{{ selectedItems.length }} materiais · {{ totalUnits }} unidades</span></div>
              <p v-if="!selectedItems.length" class="selection-empty">Sua lista ainda está vazia. Busque um material acima e toque em “Adicionar”.</p>
              <div v-for="item in selectedItems" :key="item.id" class="selected-material"><label :for="`material-${item.id}`">{{ item.nome_item }}</label><div class="selected-controls"><div><label class="quantity-label" :for="`material-${item.id}`">Quantidade</label><input :id="`material-${item.id}`" v-model="quantities[item.id]" type="number" min="1" step="1" required inputmode="numeric" /></div><button type="button" class="remove-material" :aria-label="`Remover ${item.nome_item}`" @click="removeMaterial(item)">Remover</button></div></div>
            </template>
            <button class="submit-button" :disabled="!selectedItems.length" type="submit">{{ busy ? 'Publicando…' : 'Publicar solicitação' }}</button>
          </fieldset>
        </form>
      </template>
      <template v-else-if="request">
        <p class="request-status">{{ request.status }}</p>
        <dl class="request-facts"><div><dt>Instituição solicitante</dt><dd>#{{ request.id_user_requerente }}</dd></div><div><dt>Publicada em</dt><dd>{{ new Date(request.dt_criada).toLocaleDateString('pt-BR') }}</dd></div><div><dt>Meninas</dt><dd>{{ request.quantidade_meninas }}</dd></div><div><dt>Meninos</dt><dd>{{ request.quantidade_meninos }}</dd></div></dl>
        <h2 class="form-subtitle">Materiais solicitados</h2>
        <ul class="detail-materials"><li v-for="(item, index) in request.lista_itens" :key="index"><strong>{{ item.nome_item || item.nome || `Material #${item.id_item || index + 1}` }}</strong><span>Quantidade: {{ item.quantidade ?? 'Não informada' }}</span></li></ul>
        <div class="participation-section"><p v-if="success" role="status">{{ success }}</p><template v-else><h2 class="form-subtitle">Faça parte desta ação</h2><p v-if="canJoin">Ao participar, você assume o apoio à lista de materiais desta instituição.</p><p v-else-if="request.id_user_apoiador === user?.id_usuario">Você já participa desta solicitação como apoiador.</p><p v-else-if="request.id_user_requerente === user?.id_usuario">Esta solicitação foi criada por sua instituição.</p><p v-else>Esta solicitação não está mais disponível para novos apoios.</p></template><button v-if="canJoin" class="submit-button" :disabled="busy" @click="join">{{ busy ? 'Confirmando…' : 'Quero participar como apoiador' }}</button></div>
      </template>
      <p v-if="error" class="error-message" role="alert">{{ error }}</p>
      <button v-if="error && !busy" class="visibility-button" @click="load">Recarregar informações</button>
    </section>
  </main>
</template>

<style scoped>
.material-picker{padding:18px;background:var(--palette-f7f8f2);border:1px solid var(--palette-e3e8da);border-radius:12px}.picker-label{display:block;font-size:13px;font-weight:600;margin-bottom:10px}.picker-search{display:flex;gap:10px}.picker-search input{min-width:0;flex:1;border:1px solid var(--palette-dce3d3);border-radius:8px;padding:12px;font:inherit;font-size:16px;background:var(--theme-surface)}.picker-search button,.catalog-list button{min-height:44px;padding:10px 12px;border:1px solid var(--palette-d5dfc9);border-radius:8px;background:var(--theme-surface);color:var(--palette-42643e);font-size:12px}.catalog-results{margin-top:14px}.catalog-count,.picker-hint{font-size:12px;color:var(--palette-67765c);line-height:1.7}.catalog-list{list-style:none;padding:0;margin:0;max-height:240px;overflow-y:auto;overscroll-behavior:contain;scrollbar-gutter:stable}.catalog-list li{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 4px;border-top:1px solid var(--palette-e2e7d9);font-size:14px}.catalog-list li span{overflow-wrap:anywhere}.catalog-list button{flex-shrink:0}.selected-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:26px}.selected-heading h3{font-size:15px;margin:0}.selected-heading>span{font-size:11px;color:var(--palette-718166)}.selection-empty{padding:24px 18px;border:1px dashed var(--palette-dce3d3);border-radius:10px;font-size:13px;color:var(--palette-728168);line-height:1.7}.selected-material{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--palette-edf0e6);padding:16px 0}.selected-material>label{font-size:14px;overflow-wrap:anywhere}.selected-controls{display:flex;gap:12px;align-items:center;flex-shrink:0}.selected-controls input{width:88px;min-height:44px;border:1px solid var(--palette-dfe4da);border-radius:8px;padding:10px;font:inherit;font-size:16px}.remove-material{min-height:44px;border:0;background:none;font-size:12px;color:var(--palette-8b4c42);padding:8px}.selection-announcement{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
@media(max-width:540px){.picker-search{flex-direction:column}.material-picker{padding:14px}.selected-material{align-items:flex-start;flex-direction:column;gap:10px}.selected-controls{width:100%;justify-content:space-between}.selected-heading{align-items:flex-start;flex-direction:column;gap:6px}.catalog-list{max-height:220px}}
</style>
