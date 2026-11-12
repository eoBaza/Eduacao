// Dados exclusivamente fictícios. Todas as alterações duram apenas até recarregar.
export const catalog = [
  { id: 1, nome_item: 'Caderno universitário' },
  { id: 2, nome_item: 'Lápis de escrever' },
  { id: 3, nome_item: 'Borracha' },
  { id: 4, nome_item: 'Caixa de lápis de cor' },
  { id: 5, nome_item: 'Mochila escolar' },
  { id: 6, nome_item: 'Régua de 30 cm' },
]
const user = { id_usuario: 10, nome: 'Instituto Aprender — Demonstração', gmail: 'instituto@example.com', tipo_usuario: 'J', cnpj_cpf: '00.000.000/0000-00', cep: '00000-000', endereco: 'Rua Exemplo', numero: '120', complemento: 'Sala 2' }
const material = (id, quantidade) => ({ id_item: id, nome_item: catalog.find(item => item.id === id).nome_item, quantidade })
const requests = [
  { id: 101, id_user_requerente: 20, id_user_apoiador: null, status: 'Criado Por Requerente', dt_criada: '2026-11-03T12:00:00', quantidade_meninas: 18, quantidade_meninos: 16, lista_itens: [material(1, 34), material(2, 68), material(3, 34)] },
  { id: 102, id_user_requerente: 30, id_user_apoiador: null, status: 'Criado Por Requerente', dt_criada: '2026-11-02T12:00:00', quantidade_meninas: 12, quantidade_meninos: 14, lista_itens: [material(4, 26), material(5, 26)] },
  { id: 103, id_user_requerente: 10, id_user_apoiador: null, status: 'Criado Por Requerente', dt_criada: '2026-11-01T12:00:00', quantidade_meninas: 20, quantidade_meninos: 15, lista_itens: [material(1, 35), material(6, 35)] },
  { id: 104, id_user_requerente: 10, id_user_apoiador: 40, status: 'Finalizada', dt_criada: '2026-10-28T12:00:00', quantidade_meninas: 10, quantidade_meninos: 10, lista_itens: [material(5, 20), material(2, 40)] },
]
export async function api(path, options = {}) {
  const route = path.split('?')[0]
  if (route === '/login/') return { Session_Code: 'demonstracao' }
  if (route === '/user/reset-password/') return { message: 'Demonstração concluída' }
  if (route === '/user/signup/') return { message: 'Cadastro simulado' }
  if (route === '/user/info/') return { ...user }
  if (route === '/user/tipo_usuario/') return [{ id: 1, nome: 'Físico', descricao: 'Pessoa física' }, { id: 2, nome: 'Jurídico', descricao: 'Instituição' }]
  if (route === '/list_itens') return catalog
  if (route === '/solicitacao/create/') {
    const data = JSON.parse(options.body)
    const created = { ...data, id: Math.max(...requests.map(item => item.id)) + 1, id_user_requerente: user.id_usuario, id_user_apoiador: null, status: 'Criado Por Requerente', dt_criada: '2026-11-03T15:00:00', lista_itens: data.lista_itens.map(item => material(item.id_item, item.quantidade)) }
    requests.push(created)
    return { ...created }
  }
  if (route.startsWith('/solicitacao/minha-solicitacao/')) return requests.filter(item => item.id_user_requerente === user.id_usuario && (route.includes('/pendente/') ? item.status !== 'Finalizada' : route.includes('/finalizada/') ? item.status === 'Finalizada' : true)).map(item => ({ ...item }))
  if (route === '/solicitacao/') return requests.filter(item => item.status === 'Criado Por Requerente').map(item => ({ ...item }))
  const match = route.match(/^\/solicitacao\/(\d+)\/(participar\/)?$/)
  if (match) {
    const item = requests.find(item => item.id === Number(match[1]))
    if (!item) throw new Error('Solicitação não encontrada nesta demonstração.')
    if (match[2]) { item.id_user_apoiador = user.id_usuario; item.status = 'Apoiada' }
    return { ...item }
  }
  throw new Error('Ação indisponível na apresentação.')
}
