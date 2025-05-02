# Implementação de Gerenciamento de Conversas Longas no MCP

## Problema Resolvido

O MCP (Model Communication Protocol) pode apresentar o erro `Your conversation is too long. Please try creating a new conversation or shortening your messages` quando uma conversa ultrapassa o limite de contexto suportado pelo modelo de linguagem.

## Solução Implementada

Desenvolvemos um sistema completo de gerenciamento de conversas que:

1. **Detecta automaticamente** quando uma conversa está próxima ou excedeu os limites recomendados
2. Oferece **três estratégias** para lidar com conversas longas:
   - **Truncagem**: Mantém apenas as mensagens mais recentes
   - **Resumo**: Gera um resumo textual da conversa
   - **Divisão**: Divide a conversa em várias partes menores

## Componentes Implementados

### 1. Módulo de Gerenciamento de Conversas (`conversation_manager.py`)

Contém as principais classes e lógica:
- `Message`: Representa uma mensagem individual
- `Conversation`: Representa uma conversa completa
- `ConversationManager`: Implementa métodos para gerenciar conversas

### 2. Endpoints de API (`__init__.py` no diretório `mcp`)

Adicionamos três novos endpoints:
- `/mcp/conversation/check`: Verifica se uma conversa está muito longa
- `/mcp/conversation/action`: Executa uma ação em uma conversa (truncar, resumir, dividir)
- `/mcp/conversation/list`: Lista todas as conversas do usuário

### 3. Interface do Cliente (`main.ts`)

Adicionamos novas funções para interagir com os endpoints:
- `mcp_check_conversation_length`: Verifica o tamanho da conversa
- `mcp_perform_conversation_action`: Executa ações na conversa
- `mcp_list_conversations`: Lista as conversas disponíveis

### 4. Configuração do Plugin (`build_plugin.js` e `extism.d.ts`)

Atualizamos os arquivos de configuração do plugin para incluir as novas funções.

### 5. Testes e Documentação

- Teste direto das funcionalidades (`test_conversation.py`)
- Documentação detalhada (`README_CONVERSATION_MANAGER.md`)

## Funcionamento

Quando uma conversa fica muito longa, o sistema:

1. Detecta automaticamente que a conversa excedeu os limites
2. Notifica o usuário sobre o problema
3. Oferece opções para resolver o problema:
   - Truncar a conversa (manter apenas mensagens recentes)
   - Resumir a conversa (gerar um resumo textual)
   - Dividir a conversa (criar múltiplas conversas menores)

## Próximos Passos

- Integrar com a interface do usuário para mostrar alertas e opções
- Implementar persistência de conversas em banco de dados
- Melhorar o algoritmo de resumo usando LLMs
- Ajustar os limites com base em diferentes modelos

## Benefícios

- Melhora significativa na experiência do usuário
- Evita erros de contexto muito longo
- Mantém a qualidade das respostas do modelo
- Reduz custos ao otimizar o uso de tokens 