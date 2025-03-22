# Integração do Airtable com MCP

Este documento apresenta as soluções implementadas para integrar o Airtable com o Model Communication Protocol (MCP) do Cursor.

## Soluções Implementadas

### 1. Integração do MCP do Airtable

Adicionamos o servidor MCP do Airtable ao arquivo de configuração do Cursor em `~/.cursor/mcp.json`.

### 2. Scripts para Gerenciamento de Tarefas no Airtable

#### 2.1 Criação de Tarefas via API REST

Criamos um script em Python para criar tarefas diretamente usando a API REST do Airtable.

#### 2.2 Criação de Tarefas via NPX e MCP

Criamos um script em JavaScript que usa o NPX para chamar o servidor MCP do Airtable.

#### 2.3 Integração com Chat Interativo

Modificamos o chat interativo para permitir a criação de tarefas através de comandos diretos ou ferramentas LLM.

### 3. Detalhes da Base do Airtable

- **Campos da Tabela**:
  - `Task` (Nome da tarefa)
  - `Status` (Not started, In progress, Done)
  - `Notes` (Descrição/notas)
  - `Deadline` (Data de vencimento)
  - `Owner` (Proprietário)

## Como Usar

### Criar Tarefa via Script

```bash
# Criar tarefa com valores padrão
python3 src/criar_tarefa_teste.py

# Criar tarefa com nome específico
python3 src/criar_tarefa_teste.py "Nome da Tarefa"

# Criar tarefa com nome e descrição
python3 src/criar_tarefa_teste.py "Nome da Tarefa" "Descrição detalhada"
```

### Criar Tarefa via Chat Interativo

1. Execute o chat interativo:
   ```bash
   python3 src/chat_interativo.py
   ```

2. Use o comando direto:
   ```
   criar tarefa Nome da minha tarefa
   ```

3. Ou peça ao assistente para criar uma tarefa através da conversa normal.

### Verificar Tarefas Criadas

Você pode verificar as tarefas criadas usando o script:

```bash
node src/listar_tarefas_airtable.js
```

## Scripts Disponíveis

- `criar_tarefa_teste.py` - Cria tarefas via API REST
- `listar_tarefas.py` - Lista tarefas (Python)
- `listar_tarefas_airtable.js` - Lista tarefas (JavaScript)
- `atualizar_tarefa.py` - Atualiza status de tarefas
- `concluir_tarefa.py` - Marca tarefas como concluídas
- `ajuda_airtable.py` - Script de ajuda para comandos
- `chat_interativo.py` - Chat interativo com criação de tarefas