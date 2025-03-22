# Integração MCP-Airtable

Este repositório contém scripts e configurações para integrar o MCP (Model Communication Protocol) com o Airtable para gerenciamento de tarefas.

## Sobre o projeto

A integração permite:
- Criar tarefas no Airtable via linha de comando
- Listar tarefas existentes 
- Integrar com chat interativo para criar tarefas via comandos de linguagem natural
- Usar o MCP (Model Communication Protocol) para comunicação entre modelos de linguagem e o Airtable

## Configuração inicial

1. Clone este repositório
2. Instale as dependências:
   ```bash
   # Dependências JavaScript
   npm install
   
   # Dependências Python
   pip install -r requirements.txt
   ```
3. Copie o arquivo `.env.example` para `.env` e configure suas chaves:
   ```bash
   cp .env.example .env
   ```
4. Edite o arquivo `.env` e adicione:
   - Sua chave API do Airtable
   - ID da sua base Airtable
   - ID da tabela de tarefas

## Scripts disponíveis

### Criação de tarefas

**Usando Python:**
```bash
python src/criar_tarefa_teste.py "Nome da tarefa" "Descrição opcional" "2023-12-31" "Em progresso"
```

**Usando Node.js:**
```bash
node src/criar_tarefa_airtable.js "Nome da tarefa" "Descrição opcional"
```

**Usando MCP diretamente:**
```bash
node src/teste_airtable_npx.js
```

### Listagem de tarefas

```bash
python src/listar_tarefas.py
```

## Configuração do MCP

Para configurar o servidor MCP do Airtable, adicione o seguinte ao seu arquivo `~/.cursor/mcp.json`:

```json
{
  "airtable-server": {
    "command": "node",
    "args": [
      "./caminho/para/seu/repo/src/load_env_and_run_server.js"
    ]
  }
}
```

## Chat interativo

O script `chat_interativo.py` permite criar tarefas usando comandos de linguagem natural. Exemplos:

- "criar tarefa Estudar Python"
- "crie uma tarefa com título Reunião de equipe"
- "nova tarefa: Revisar documentação"

## Licença

MIT 