import { build } from '../EducAcao-Project/node_modules/vite/dist/node/index.js'
import vue from '../EducAcao-Project/node_modules/@vitejs/plugin-vue/dist/index.mjs'
import { writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = fileURLToPath(new URL('.', import.meta.url))
const screens = [
  ['01-login.html', 'Login', '/login', 'Entrada na plataforma.'],
  ['02-cadastro.html', 'Cadastro', '/cadastro', 'Cadastro de pessoa física ou instituição.'],
  ['03-recuperar-senha.html', 'Recuperar senha', '/esqueci-minha-senha', 'Formulário de recuperação do acesso.'],
  ['04-inicio.html', 'Início', '/home', 'Solicitações abertas e busca por materiais.'],
  ['05-minha-conta.html', 'Minha conta', '/minha-conta', 'Dados da instituição e endereço.'],
  ['06-minhas-solicitacoes.html', 'Minhas solicitações', '/minhas-solicitacoes', 'Pedidos com filtros de situação.'],
  ['07-nova-solicitacao.html', 'Abrir solicitação', '/solicitacao/nova', 'Catálogo de materiais e crianças atendidas.'],
  ['08-detalhes-solicitacao.html', 'Detalhes da solicitação', '/solicitacao/101', 'Materiais solicitados e participação como apoiador.'],
]
const result = await build({
  configFile: false, root,
  plugins: [vue()],
  resolve: { alias: { vue: path.resolve(root, '../EducAcao-Project/node_modules/vue/dist/vue.runtime.esm-bundler.js') } },
  define: { 'process.env.NODE_ENV': '"production"' },
  build: { write: false, cssCodeSplit: false, lib: { entry: path.join(root, 'fonte/main.js'), name: 'ApresentacaoEducAcao', fileName: 'apresentacao', cssFileName: 'apresentacao', formats: ['iife'] } },
})
const output = (Array.isArray(result) ? result[0] : result).output
const js = output.find(item => item.type === 'chunk').code.replace(/<\/script/gi, '<\\/script')
// Fontes externas são opcionais no projeto original. O pacote usa o fallback local para funcionar offline.
const css = output.filter(item => item.type === 'asset' && item.fileName.endsWith('.css')).map(item => String(item.source).replace(/@import\s+url\([^)]*\);?/g, '')).join('\n')
const head = title => `<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f8f2"><title>${title} | EducAção</title>`
for (const [file, title, route] of screens) {
  await writeFile(path.join(root, file), `${head(title)}<style>${css}</style></head><body data-route="${route}"><div id="app"></div><script>${js}</script></body></html>`)
}
const cards = screens.map(([file, title, , description], index) => `<a href="${file}"><span class="number">${String(index + 1).padStart(2, '0')}</span><h2>${title}</h2><p>${description}</p><span class="open">Apresentar tela →</span></a>`).join('')
await writeFile(path.join(root, 'index.html'), `${head('Apresentação das telas')}<style>
*{box-sizing:border-box}body{margin:0;background:#f7f8f2;color:#253d33;font:16px/1.6 Arial,sans-serif}main{max-width:1120px;margin:auto;padding:64px 24px}header{max-width:720px;margin-bottom:36px}.eyebrow{font-size:12px;letter-spacing:2px;color:#597547}h1{font-size:clamp(32px,5vw,52px);line-height:1.12;letter-spacing:-2px;margin:16px 0}h1 span{color:#597547}header p{color:#67745e}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}nav a{display:block;color:inherit;text-decoration:none;background:white;border:1px solid #e2e7d9;border-radius:18px;padding:26px}nav a:hover{border-color:#597547}a:focus-visible{outline:3px solid #597547;outline-offset:4px}.number{color:#728650;font-size:13px}h2{font-size:19px;margin:16px 0 8px}nav p{font-size:14px;min-height:46px;color:#67745e}.open{font-size:13px;font-weight:bold;color:#2f513e}footer{font-size:13px;color:#67745e;margin-top:32px}
</style></head><body><main><header><div class="eyebrow">APRESENTAÇÃO DO FRONTEND</div><h1>Educ<span>Ação</span><br>Telas desenvolvidas</h1><p>Oito telas para percorrer a experiência de conectar instituições a quem deseja ajudar com materiais escolares.</p><p>Selecione uma tela para apresentar. Use Alt + ← para voltar a este índice ou F11 para tela cheia.</p></header><nav aria-label="Telas disponíveis">${cards}</nav><footer>Demonstração com dados fictícios. Formulários e ações são simulados localmente; recarregar restaura os exemplos.</footer></main></body></html>`)
console.log(`Apresentação gerada: index.html + ${screens.length} telas independentes.`)
