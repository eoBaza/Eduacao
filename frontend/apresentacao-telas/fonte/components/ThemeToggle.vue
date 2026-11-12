<script setup>
import { ref } from 'vue'

const dark = ref(document.documentElement.dataset.theme === 'dark')
function toggleTheme() {
  dark.value = !dark.value
  const theme = dark.value ? 'dark' : 'light'
  document.documentElement.dataset.theme = theme
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark.value ? '#141719' : '#f7f8f2')
  try { localStorage.setItem('educacao.theme', theme) } catch { /* A alternância funciona mesmo sem armazenamento. */ }
}
</script>

<template>
    <button type="button" class="theme-toggle" :aria-pressed="dark" aria-label="Modo escuro" :title="dark ? 'Ativar modo claro' : 'Ativar modo escuro'" @click="toggleTheme">
      <svg v-if="!dark" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 14A8.5 8.5 0 0 1 10 4a8.5 8.5 0 1 0 10 10Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
      <svg v-else viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
</template>

<style scoped>
.theme-toggle{display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;width:44px;height:44px;padding:10px;border:1px solid var(--theme-border);border-radius:50%;background:transparent;color:var(--theme-muted);cursor:pointer}
.theme-toggle:hover{background:var(--theme-soft);color:var(--theme-text)}.theme-toggle svg{width:20px;height:20px}
</style>
