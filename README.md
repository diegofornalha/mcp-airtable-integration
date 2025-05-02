# MCP Server Integration

Este projeto integra um servidor FastAPI com o protocolo MCP (Model Communication Protocol) e o expõe através de um servidor Node.js que usa o Extism para carregar e executar um plugin WebAssembly.

## Arquitetura

O projeto consiste em:

1. **Servidor FastAPI**: Implementa endpoints REST e MCP na porta 8000
2. **Plugin WebAssembly**: Usa TypeScript para criar um plugin que atua como proxy para o servidor FastAPI
3. **Servidor Node.js**: Carrega o plugin WebAssembly e expõe suas funcionalidades através de endpoints REST na porta 3000

## Configuração

### Configuração do Ambiente

1. Clone o repositório
2. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   PORT=3000
   MCP_API_KEY=seu_token_xtp
   MCP_API_URL=https://www.mcp.run/api
   ```

### Servidor FastAPI

1. Navegue até a pasta `backend`
2. Execute o servidor:
   ```bash
   cd backend
   ./run.sh
   ```
   O servidor estará disponível em:
   - http://localhost:8000/docs - Swagger UI
   - http://localhost:8000/redoc - ReDoc
   - http://localhost:8000/mcp-api - Servidor MCP

### Plugin WebAssembly

1. Compile o plugin:
   ```bash
   npm install
   npm run build
   ```

### Servidor Node.js

1. Inicie o servidor Node.js:
   ```bash
   npm start
   ```
   O servidor estará disponível em:
   - http://localhost:3000/health - Verificação de saúde
   - http://localhost:3000/api/mcp/tools - Lista de ferramentas MCP
   - http://localhost:3000/api/mcp/execute - Endpoint para executar ferramentas MCP

## Integração com MCP.run

Para integrar com a plataforma MCP.run:

1. Configure seu aplicativo na plataforma XTP/MCP.run:
   - Nome: `xfxacademy`
   - ID: `app_01jq5p4km8e27r1gvrvgrryvd8`
   - Token XTP: Configurado no arquivo `.env`
   - Guest Key: `replace-me-ce20c9db-4b8b-4e1d-9131-91275d4fd34b`

2. Crie uma tarefa na plataforma MCP.run que utilize seu servidor

Para instruções detalhadas sobre a implantação na plataforma MCP.run, consulte o [Guia Completo de Implantação](DEPLOY_GUIDE.md).

## Servlet Databutton

Este projeto inclui um servlet chamado "databutton" que pode ser publicado no MCP.run para interagir com o servidor local. Para publicar o servlet:

```bash
cd databutton
xtp plugin push
```

O servlet disponibiliza as seguintes ferramentas:

### Ferramentas MCP Locais
- `check_health` - Verifica a saúde do servidor
- `mcp_list_tools` - Lista as ferramentas disponíveis no servidor local
- `mcp_query` - Consulta o servidor MCP do aplicativo rodando localmente
- `mcp_query_stream` - Consulta o servidor MCP com resposta em streaming

### Ferramentas MCP.run
- `mcp_run_login` - Realiza login no MCP.run
- `mcp_run_search_servlets` - Pesquisa por servlets disponíveis no MCP.run
- `mcp_run_get_profiles` - Lista todos os perfis disponíveis para o usuário atual
- `mcp_run_set_profile` - Define o perfil ativo

Para instalar o servlet, visite: https://mcp.run/usuario/databutton (substitua "usuario" pelo seu nome de usuário)

## Endpoints Disponíveis

### Servidor FastAPI (Porto 8000)

- `GET /health` - Verifica o status do servidor
- `GET /tools` - Lista as ferramentas disponíveis
- `POST /mcp/query` - Endpoint para consultas MCP
- `GET /server-time` - Retorna o horário atual do servidor
- `GET /` - Rota principal
- `GET /mcp-api` - Servidor MCP gerado pelo FastAPI-MCP

### Servidor Node.js (Porto 3000)

- `GET /health` - Verifica o status do servidor
- `GET /api/mcp/tools` - Lista as ferramentas MCP
- `POST /api/mcp/execute` - Executa uma ferramenta MCP

## Tecnologias Utilizadas

- FastAPI - Framework web para Python
- Node.js - Ambiente de execução JavaScript
- Express.js - Framework web para Node.js
- Extism - Framework para plugins WebAssembly
- TypeScript - Linguagem de programação tipada baseada em JavaScript
- MCP - Model Communication Protocol
