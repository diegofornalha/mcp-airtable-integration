# Guia Completo de Implantação no MCP.run

Este guia explica como implantar o servidor FastAPI+MCP e o servlet Databutton na plataforma MCP.run.

## Pré-requisitos

- Conta no MCP.run
- Node.js (versão 16 ou superior)
- npm ou yarn
- CLI XTP instalada
- Token de acesso XTP
- Git instalado (para versionamento)
- Servidor FastAPI+MCP em execução e acessível publicamente

## 1. Instalação da CLI XTP

A CLI XTP é necessária para compilar e publicar os plugins:

```bash
curl "https://static.dylibso.com/cli/install.sh" -s | bash
```

Verifique a instalação:

```bash
xtp --version
```

## 2. Autenticação na plataforma XTP

Há duas maneiras de autenticar:

### Método 1: Login interativo
Execute o comando de login:

```bash
xtp login
```

Isso abrirá uma janela do navegador para autenticação.

### Método 2: Token de acesso (recomendado para CI/CD)
Configure o token de acesso como variável de ambiente:

```bash
export XTP_TOKEN=xtp0_SEU_TOKEN_AQUI
```

Exemplo com o token usado anteriormente:

```bash
export XTP_TOKEN=xtp0_AZY3Jng7dEmxvi_W9TVu94Wpn-fTeXqc0imyr9Ybqu84hFcAvw1sFw
```

## 3. Publicação do Servlet Databutton

### 3.1 Configuração e Publicação

Para publicar o servlet Databutton, siga os passos abaixo:

```bash
# Entrar no diretório do plugin
cd databutton

# Instalar dependências e compilar
bash prepare.sh && npm run build

# Publicar o plugin
xtp plugin push
```

Após a publicação, o sistema executará simulações para validar o plugin. Você receberá uma mensagem de confirmação como:

```
✅ Version ver_XXXXXXXXX has been processed for Plugin 'databutton'
```

### 3.2 Ferramentas disponíveis no Servlet Databutton

O servlet disponibiliza as seguintes ferramentas:

#### Ferramentas MCP Locais
- `check_health` - Verifica a saúde do servidor
- `mcp_list_tools` - Lista as ferramentas disponíveis no servidor local
- `mcp_query` - Consulta o servidor MCP do aplicativo rodando localmente
- `mcp_query_stream` - Consulta o servidor MCP com resposta em streaming

#### Ferramentas MCP.run
- `mcp_run_login` - Realiza login no MCP.run
- `mcp_run_search_servlets` - Pesquisa por servlets disponíveis no MCP.run
- `mcp_run_get_profiles` - Lista todos os perfis disponíveis para o usuário atual
- `mcp_run_set_profile` - Define o perfil ativo

### 3.3 Verificando a publicação

Para verificar se o plugin foi publicado corretamente:

```bash
xtp plugin view --name 'databutton' --extension-point ext_01je4jj1tteaktf0zd0anm8854
```

Para instalar o servlet, visite:
```
https://mcp.run/diegofornalha/databutton
```

## 4. Configuração da Tarefa (Task)

1. Navegue até "Tasks" no seu perfil
2. Clique em "New Task" para criar uma nova tarefa
3. Configure conforme necessário:
   - Nome: `databutton-task`
   - Descrição: "Tarefa para interagir com o servidor MCP local"
   - Prompt: Instruções para o modelo de IA sobre como interagir com seu servidor

Exemplo de prompt:
```
Você é um assistente especializado em interagir com o servidor MCP local.
Sua tarefa é ajudar o usuário a:
1. Verificar a saúde do servidor
2. Listar as ferramentas disponíveis
3. Enviar consultas ao servidor
4. Obter o horário atual do servidor

Use as ferramentas do MCP Local para realizar essas tarefas e responda sempre em português.
```

## 5. Conexão via SSE (Server-Sent Events)

Após o registro, você receberá uma URL SSE no formato:

```
https://www.mcp.run/api/mcp/sse?nonce=XXXXX&username=XXXXX&exp=XXXXX&profile=XXXXX&sig=XXXXX
```

Exemplo:
```
https://www.mcp.run/api/mcp/sse?nonce=k_58SJd7XrcR2hb4juU-Uw&username=diegofornalhamcp&exp=1745208490844&profile=diegofornalhamcp%2Fnovo-mcp&sig=L-lJHEuNtdS5lb5HetsOQFFIYYJ729V9ADNrcODIxwk
```

Esta URL será usada para autenticar seu cliente MCP com o servidor.

## 6. Atualização do Servlet

Para atualizar o servlet após modificações:

1. Faça as alterações no código
2. Compile novamente:
   ```bash
   bash prepare.sh && npm run build
   ```
3. Publique a nova versão:
   ```bash
   xtp plugin push
   ```

O sistema criará automaticamente uma nova versão do plugin.

## 7. Teste e Uso

Após configurar a tarefa, você pode acessá-la através de:

1. **Interface web**: `https://www.mcp.run/settings/tasks/[seu-perfil]/databutton/databutton-task`
2. **API REST**: `https://www.mcp.run/api/runs/[seu-perfil]/databutton/databutton-task?nonce=XXX&sig=XXX`
3. **Cliente SSE**: Através da URL SSE do seu perfil

## 8. Integração com Clientes

### 8.1 Cliente Web

Para integrar o servidor MCP com um cliente web, use a URL SSE fornecida:

```javascript
const eventSource = new EventSource('sua-url-sse-aqui');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received message:', data);
};

// Enviar uma consulta
function sendQuery(message) {
  fetch('sua-api-url/runs/diegofornalha/databutton/databutton-task', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input: message }),
  });
}
```

### 8.2 Cliente Python

Para integrar com Python, você pode usar o cliente Arcee CLI ou criar seu próprio cliente:

```python
import requests
import sseclient
import json

def create_sse_client(url):
    headers = {'Accept': 'text/event-stream'}
    response = requests.get(url, headers=headers, stream=True)
    return sseclient.SSEClient(response)

def listen_for_events(url):
    client = create_sse_client(url)
    for event in client.events():
        print(f"Received event: {event.data}")

# Iniciar a escuta em segundo plano
import threading
threading.Thread(target=listen_for_events, args=('sua-url-sse-aqui',)).start()

# Enviar uma consulta
def send_query(message):
    response = requests.post(
        'sua-api-url/runs/diegofornalha/databutton/databutton-task',
        json={'input': message}
    )
    return response.json()
```

## 9. Solução de Problemas

### Erros comuns

#### Erro de Conexão

Se você encontrar erros de conexão com o servidor SSE:

1. Verifique se a URL SSE está correta e não expirou
2. Certifique-se de que o servidor FastAPI+MCP está em execução
3. Verifique se há problemas de CORS ou firewall

#### Erro de Autenticação

Se você encontrar erros de autenticação:

1. Verifique se o token na URL SSE ainda é válido
2. Gere um novo token se necessário, acessando as configurações da sua tarefa

#### Erro de compilação

Se você encontrar erros durante a compilação:

```
Error: error generating plugin: dependency is not available: extism-js
```

Solução: Execute `bash prepare.sh` para instalar as dependências.

#### Erro de publicação

Se você encontrar erros ao publicar o plugin:

```
Error: Failed to push plugin: ...
```

Solução: Verifique se o plugin compilou corretamente e se você tem permissões.

### Problemas com a publicação do plugin

Ao tentar publicar o plugin, é possível encontrar diversos problemas. Aqui estão algumas soluções que implementamos:

#### 1. Falta de endpoints MCP no servidor FastAPI
Se ao testar o plugin você receber erros 404 nos endpoints `/api/mcp/tools` ou similares, é necessário implementar esses endpoints no servidor FastAPI. Criamos um exemplo de implementação em `backend/app/apis/mcp/__init__.py` que simula todas as funcionalidades necessárias.

#### 2. Problemas para gerar o arquivo WebAssembly
A compilação para WebAssembly pode ser problemática. Uma solução alternativa é usar o comando `xtp plugin init` para gerar um template de plugin válido:

```bash
xtp plugin init --extension-point ext_01je4jj1tteaktf0zd0anm8854 --name databutton --template TypeScript --path ./databutton
```

Em seguida, adapte o código do template para suas necessidades.

#### 3. Validação de schema falha
O XTP tem requisitos específicos para os schemas das ferramentas:
- Cada ferramenta deve ter um `inputSchema` com um `type` definido (geralmente "object")
- Cada propriedade no schema deve ter uma `description` detalhada
- Todos os schemas devem seguir o formato JSONSchema corretamente

Exemplo de schema válido:
```typescript
inputSchema: {
  type: "object",
  properties: {
    query: { 
      type: "string",
      description: "Consulta a ser enviada ao servidor MCP"
    }
  }
}
```

#### 4. Múltiplos plugins conflitantes
Se você tiver problemas com múltiplos plugins para o mesmo extension point, use o comando `xtp plugin unbind` para desvincular os plugins indesejados:

```bash
xtp plugin unbind --name plugin-indesejado
```

Em seguida, atualize o arquivo `xtp.toml` para garantir que está usando o nome correto do plugin:

```toml
name = "databutton"
```

#### 5. Testar localmente antes de publicar
Para depurar problemas, sempre teste o plugin localmente antes de publicar:
1. Verifique se os endpoints MCP estão funcionando corretamente
2. Teste cada endpoint individualmente com curl ou similar
3. Assegure-se de que o servidor FastAPI está rodando na porta correta

## 10. Recursos Adicionais

- [Documentação do MCP.run](https://www.mcp.run/docs)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do FastAPI-MCP](https://github.com/tadata-org/fastapi_mcp)
- [Documentação do XTP](https://docs.extism.org/cli)
- [Documentação MCP SSE](https://www.mcp.run/docs/sse) 