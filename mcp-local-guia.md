# Guia do MCP Local (Model Context Protocol)

## O que é o MCP?

O MCP (Model Context Protocol) é um protocolo que permite a modelos de linguagem (LLMs) como Claude, GPT e outros, acessarem ferramentas externas em tempo real. Este protocolo padroniza a comunicação entre os modelos e serviços externos, permitindo que os LLMs executem ações no mundo real como buscar informações, interagir com bancos de dados ou manipular sistemas.

## MCP Local no Projeto

Seu projeto implementa um servidor MCP local que permite:

1. Definir ferramentas personalizadas para LLMs
2. Conectar essas ferramentas ao ambiente do Cursor (ou outros clientes MCP)
3. Expandir as capacidades de IA conversacional com funcionalidades específicas do seu aplicativo

## Arquitetura do Sistema MCP Local

### Componentes Principais

1. **Servidor Backend FastAPI**
   - Implementa o protocolo MCP
   - Define e expõe ferramentas através de endpoints REST
   - Gerencia a comunicação entre os LLMs e as ferramentas

2. **Frontend**
   - Interface de usuário para interagir com o sistema
   - Exibe resultados das interações com o LLM e ferramentas MCP

3. **Protocolo Websocket**
   - Permite comunicação bidirecional em tempo real
   - Facilita a troca de mensagens entre o LLM e as ferramentas

## Ferramentas MCP Disponíveis

Seu projeto local implementa as seguintes ferramentas MCP:

- **check_health**: Verifica a saúde do aplicativo
- **mcp_list_tools**: Lista todas as ferramentas disponíveis no servidor
- **mcp_query**: Consulta o servidor MCP com uma mensagem
- **mcp_query_stream**: Consulta o servidor MCP com resposta em streaming

## Como Configurar o MCP com Cursor

Para que o Cursor (IDE) reconheça seu servidor MCP local:

1. Crie um arquivo de configuração no diretório do projeto:

```
.cursor/mcp.json
```

2. Configure o arquivo com o caminho para o seu servidor MCP local:

```json
{
    "mcpServers": {
        "local-mcp-server": {
            "command": "/bin/bash",
            "args": ["-c", "cd /Users/agents/Desktop/mcp-cli/backend && source ../.venv/bin/activate && uvicorn main:app"]
        }
    }
}
```

3. Reinicie o Cursor para carregar a nova configuração

## Fluxo de Comunicação MCP

1. **Inicialização**:
   - O servidor MCP é iniciado (backend FastAPI)
   - O cliente MCP (Cursor) se conecta ao servidor através da configuração em `mcp.json`

2. **Comunicação**:
   - O LLM (dentro do Cursor) recebe uma solicitação do usuário
   - O LLM determina que precisa de uma ferramenta externa
   - A solicitação é enviada ao servidor MCP
   - O servidor processa a solicitação usando a ferramenta apropriada
   - O resultado é retornado ao LLM
   - O LLM incorpora o resultado em sua resposta

## Desenvolvimento de Novas Ferramentas MCP

Para adicionar uma nova ferramenta ao seu servidor MCP local:

1. Defina a função da ferramenta no backend FastAPI:

```python
@app.post("/nova_ferramenta")
async def nova_ferramenta(params: ParamsModel):
    # Implemente a lógica da ferramenta
    resultado = fazer_algo(params.input)
    return {"resultado": resultado}
```

2. Registre a ferramenta no protocolo MCP:

```python
ferramenta = {
    "nome": "nova_ferramenta",
    "descricao": "Esta ferramenta faz algo útil",
    "parametros": {
        "input": "O valor de entrada para a ferramenta"
    }
}
mcp_tools.append(ferramenta)
```

3. Reinicie o servidor para disponibilizar a nova ferramenta

## Testes e Depuração

Para testar seu servidor MCP local:

1. Inicie o servidor backend:
```bash
cd backend
./run.sh
```

2. Verifique se o servidor está funcionando:
```bash
curl http://127.0.0.1:8000/health
```

3. Liste as ferramentas disponíveis:
```bash
curl http://127.0.0.1:8000/tools
```

4. Para testar uma ferramenta específica, envie uma requisição POST com os parâmetros apropriados

## Integração com Aplicações Externas

Seu servidor MCP local pode ser integrado com outras aplicações além do Cursor:

1. **Aplicações Web**: Conecte através de chamadas de API
2. **Outros LLMs**: Configure outros modelos para usar seu servidor MCP
3. **Ferramentas CLI**: Crie scripts que interagem com seu servidor MCP

## Considerações de Segurança

1. **Autenticação**: Considere adicionar autenticação para proteger seu servidor MCP
2. **Validação de Entrada**: Verifique cuidadosamente os parâmetros recebidos
3. **Limitação de Recursos**: Implemente limites de uso para evitar sobrecarga

## Recursos Adicionais

- [Documentação oficial do MCP](https://docs.cursor.com/context/model-context-protocol)
- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Guia de desenvolvimento de ferramentas para LLMs](https://docs.anthropic.com/claude/docs/tool-use)

---

Este documento fornece uma visão geral do servidor MCP local em seu projeto. Para informações mais detalhadas sobre implementações específicas, consulte o código-fonte e os comentários no diretório `backend/`. 