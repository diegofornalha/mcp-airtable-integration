# Integração MCP-Airtable

Este repositório contém scripts e ferramentas para integração entre o MCP (Model Communication Protocol) e o Airtable para gerenciamento de tarefas.

## Soluções Implementadas

### 1. Integração do servidor MCP para Airtable

Adicionamos suporte ao servidor MCP para Airtable, permitindo que modelos de linguagem possam criar e gerenciar tarefas diretamente. A configuração deve ser adicionada ao arquivo `~/.cursor/mcp.json`:

```json
{
  "airtable-server": {
    "command": "npx",
    "args": [
      "-y",
      "@smithery/cli@latest",
      "run",
      "airtable-server",
      "--config",
      "{\"airtableApiKey\":\"patniDQMmniKrjPoy.d81e30b3f466457908966ef8bcd5bfc96ac0c40bf5267ef423376e149ec28450\"}"
    ]
  }
}
```

### 2. Scripts para gerenciamento de tarefas no Airtable

Criamos scripts para gerenciar tarefas no Airtable:

1. Script Python para criar tarefas via API REST do Airtable
2. Script JavaScript usando NPX para chamar o servidor MCP para criação de tarefas
3. Modificações no script de chat interativo para permitir a criação de tarefas via comandos diretos ou via ferramentas do LLM

## Dados do Airtable

- Base ID: `appt2CRa7k9cUASRJ`
- Nome da tabela: Tasks
- Campos: Task (nome), Notes (descrição), Status, Deadline

## Como criar tarefas

### Via scripts

```bash
# Python
python src/criar_tarefa_teste.py "Nome da tarefa"

# JavaScript
node src/criar_tarefa_airtable.js "Nome da tarefa"

# NPX direto
node src/teste_airtable_npx.js
```

### Via chat interativo

No chat interativo, você pode usar:

1. Comando direto: `criar tarefa Comprar leite`
2. Frase natural: `crie uma tarefa com título Reunião com cliente`
3. Pedir ao modelo para criar uma tarefa

## Troubleshooting

Se tiver problemas com o MCP ou NPX, verifique:

1. Se o NPX está instalado
2. Se o servidor MCP está configurado corretamente
3. Se a chave de API do Airtable é válida 