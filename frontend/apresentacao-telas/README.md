# Apresentação das telas do EducAção

Abra **index.html** com dois cliques e escolha a tela que deseja apresentar. Não precisa de Node, servidor, banco, backend ou internet para apresentar. Também é possível abrir cada HTML numerado diretamente. Para compartilhar, envie esta pasta ou apenas os nove arquivos HTML juntos.

- F11: tela cheia no navegador.
- Alt + seta para a esquerda: voltar ao índice após abrir uma tela (ou voltar na navegação).
- O botão de lua/sol das telas alterna o tema.
- Login: qualquer e-mail em formato válido e qualquer senha permitem demonstrar a entrada.
- Busca, filtros, catálogo e navegação funcionam. Cadastro, recuperação de senha, publicação e apoio são simulações em memória. Recarregar restaura os dados fictícios; nenhum dado é enviado ou salvo no backend.

## Telas incluídas

| Arquivo | Tela | Componente original |
| --- | --- | --- |
| 01-login.html | Login | index.vue |
| 02-cadastro.html | Cadastro | signup.vue |
| 03-recuperar-senha.html | Recuperar senha | forgot-password.vue |
| 04-inicio.html | Início | home.vue |
| 05-minha-conta.html | Minha conta | account.vue |
| 06-minhas-solicitacoes.html | Minhas solicitações | home.vue, com mine |
| 07-nova-solicitacao.html | Abrir solicitação | request.vue, sem id |
| 08-detalhes-solicitacao.html | Detalhes da solicitação | request.vue, com id |

## Análise e preparação

O frontend em `../EducAcao-Project` usa Vue 3, Vite e navegação pelo hash. Há seis componentes de página que produzem oito telas. A aplicação original exige sessão para as telas internas e consulta a API para dados de conta, tipos de cadastro, catálogo e solicitações.

Esta pasta contém uma cópia das telas atuais em `fonte`, preservando inclusive as alterações locais que já estavam no frontend. A apresentação dispensa autenticação real e substitui a API por exemplos fictícios. As telas e estilos originais foram preservados; apenas a cópia do controle de sessão e a camada de dados foram adaptadas. As fontes remotas foram retiradas do HTML gerado para permitir apresentação offline, usando a fonte sans-serif local como fallback. Isso pode alterar levemente a tipografia em relação ao frontend conectado.

O código do aplicativo original não foi modificado. Esta é uma fotografia das telas em 03/11/2026: futuras alterações do original não são sincronizadas automaticamente.

## Gerar novamente

Com as dependências do frontend original instaladas, execute na raiz do repositório:

```powershell
node frontend/apresentacao-telas/gerar.mjs
```

O comando recompila os arquivos de `fonte` nos HTML desta pasta. As dependências são usadas somente para gerar, nunca para apresentar.
