export async function api(path, options = {}) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 15000)
  try {
    const response = await fetch(`/api${path}`, {
      ...options,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${sessionStorage.getItem('educacao.session') || ''}`, ...options.headers },
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      if (response.status === 401) {
        sessionStorage.removeItem('educacao.session')
        window.location.hash = '/login'
      }
      throw new Error(typeof data?.detail === 'string' ? data.detail : 'Não foi possível concluir. Confira os dados e tente novamente.')
    }
    return data
  } catch (error) {
    if (error.name === 'AbortError' || error instanceof TypeError) throw new Error('Não foi possível conectar ao servidor. Tente novamente.')
    throw error
  } finally { clearTimeout(timeout) }
}
