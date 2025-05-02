# Implementação do Backend MCP e Solução de Problemas

## Entendimento do Projeto

O projeto consiste em um servidor backend MCP (Model Context Protocol) implementado com FastAPI que permite:

- Expor ferramentas para modelos de linguagem como Claude ou GPT
- Processar requisições MCP via API REST
- Gerenciar a comunicação entre os LLMs e as ferramentas

## Problemas Encontrados

### 1. Dependência do Databutton

O arquivo `main.py` original tinha uma dependência crítica:

```python
from databutton_app.mw.auth_mw import AuthConfig, get_authorized_user
```

- Problema: O pacote databutton na versão 0.38.34 não estava disponível publicamente
- Consequência: O servidor não inicializava corretamente

### 2. Conflitos de Portas

- Ao tentar iniciar o servidor, encontramos o erro: "address already in use"
- Identificamos que outros processos Python estavam usando a porta 8000
- Verificamos com `lsof -i :8000` e encontramos processos conflitantes

### 3. Conflitos de Dependências

No arquivo `requirements.txt` original:
- A versão específica do databutton (0.38.34) não estava disponível
- Havia conflito entre a versão do fastapi requerida pelo databutton e a versão mais recente

## Abordagem de Solução

Adotamos uma abordagem progressiva para resolver os problemas:

1. **Arquivos de Teste**
   - Criamos `basic_server.py`: Um servidor FastAPI mínimo para testar o ambiente
   - Criamos `debug_server.py`: Servidor com mensagens de debug para identificar problemas

2. **Simplificação de Dependências**
   - Criamos `requirements-essencial.txt` com apenas as dependências críticas
   - Removemos a dependência do databutton

3. **Reimplementação do Servidor MCP**
   - Criamos `main.py`: Uma versão simplificada do servidor MCP sem dependências problemáticas
   - Implementamos os mesmos endpoints MCP do original, mas com código limpo

4. **Mudança de Porta**
   - Alteramos a porta de 8000 para 9000 para evitar conflitos

## Decisão de Arquivos

### Qual arquivo manter?

**Recomendação: Manter o `main.py`**

- É uma implementação funcional do servidor MCP
- Não depende do databutton, evitando o problema principal
- Implementa todos os endpoints essenciais (health, tools, mcp/query)
- Usa o modelo Pydantic para validação de requisições
- Roda na porta 9000 para evitar conflitos

Os outros arquivos (`basic_server.py` e `debug_server.py`) foram apenas etapas intermediárias para diagnóstico e podem ser removidos.

## Detalhes da Implementação no main.py

1. **Endpoints Implementados:**
   - `/health`: Verificação de status do servidor
   - `/tools`: Lista as ferramentas MCP disponíveis
   - `/mcp/query`: Endpoint principal para processamento de consultas MCP
   - `/`: Endpoint raiz para verificação básica

2. **Modelos de Dados:**
   - `MCPRequest`: Modelo Pydantic para validação das requisições MCP

3. **Configurações:**
   - CORS habilitado para permitir requisições de qualquer origem
   - Porta 9000 para evitar conflitos

## Como Executar o Servidor

O script `run.sh` foi atualizado para usar o novo arquivo:

```bash
#!/bin/bash
source ../.venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 9000 --reload
```

Para executar:
```bash
cd backend
./run.sh
```

## Por que da mudança de porta 8000 para 9000?

A mudança foi necessária porque:

1. Identificamos que havia processos Python anteriores usando a porta 8000
2. Ao tentar iniciar o servidor na porta 8000, recebíamos o erro:
   ```
   ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
   ```
3. Mesmo após tentar matar os processos com `kill -9`, em algumas situações a porta permanecia bloqueada
4. A porta 9000 estava livre e é uma alternativa comum para serviços web de desenvolvimento

## Conclusão

O servidor MCP agora é funcional com o `main.py`, evitando a dependência problemática do databutton. A implementação mantém todas as funcionalidades essenciais para um servidor MCP, permitindo que o Cursor ou outros clientes MCP possam se conectar e utilizar as ferramentas expostas.

A abordagem seguiu princípios de engenharia de software de isolar problemas e construir soluções incrementais até obter um sistema funcional. 