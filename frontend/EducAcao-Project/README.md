# Frontend EducAção

Login, recuperação de senha e home em Vue 3 e Vite, responsivos para celular e desktop.

```sh
npm install
npm run dev
```

Abra o endereço exibido pelo Vite. Para testar no smartphone, conecte-o à mesma rede e use o endereço `Network` exibido no terminal.

`npm run build` gera a versão de produção em `dist`.

## API

O servidor de desenvolvimento encaminha `/api` para `http://127.0.0.1:8000`. O formulário utiliza `POST /login/` com JSON `{ "gmail": "email@exemplo.com", "senha": "sua senha" }` e guarda `Session_Code` em `sessionStorage`. Credenciais inválidas retornam HTTP 401; dados inválidos retornam HTTP 422. Após o login, o usuário acessa `#/home`. A home consulta `GET /solicitacao/`, exibe os totais retornados, permite buscar e filtrar solicitações e expandir suas listas de materiais. Há estados de carregamento, erro e lista vazia. O botão Sair remove a sessão local; não existe endpoint de revogação no backend atual. A criação e o apoio a solicitações ainda não estão disponíveis nesta interface. A verificação de sessão no navegador controla a navegação; a autorização das rotas de dados deve ser feita no backend.

Na raiz do repositório, inicie a API em outro terminal (com o `.env` do banco configurado):

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir App --reload --port 8000
```

O navegador usa `/api/login/` no mesmo endereço do frontend, inclusive no celular. O Vite encaminha a chamada para `/login/` no FastAPI, sem necessidade de liberar CORS para o desenvolvimento.

Em produção, configure o servidor para encaminhar `/api` ao backend e use HTTPS. O proxy do Vite é somente para desenvolvimento.

As fontes usam Google Fonts, com fallback local para sans-serif.


## Cadastro e solicitações

- `POST /user/signup/`: cadastro, com CEP, número e complemento nos parâmetros e os demais dados no JSON. O endereço é criado pelo backend; não é necessário informar `id_endereco`.
- `GET /user/me/`: dados da conta identificada pela sessão Bearer.
- `POST /solicitacao/create/`: exige sessão de instituição. JSON com `lista_itens: [{id_item, quantidade}]`, `quantidade_meninas` e `quantidade_meninos`. A identidade do requerente e os nomes dos materiais são definidos pelo servidor.
- `GET /solicitacao/{id}/`: detalhes, com sessão Bearer.
- `POST /solicitacao/{id}/participar/`: registra o usuário da sessão como apoiador, impedindo apoio próprio e pedidos já assumidos. A solicitação deixa de aparecer na lista de pedidos abertos.

O cadastro depende da consulta de CEP e das regiões cadastradas no banco. Não houve alteração na estrutura das tabelas.
