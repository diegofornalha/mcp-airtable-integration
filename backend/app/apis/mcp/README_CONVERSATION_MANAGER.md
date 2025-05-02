# Gerenciador de Conversas MCP

Este módulo fornece funcionalidades para gerenciar conversas longas no MCP (Model Communication Protocol), incluindo detecção de tamanho, resumo e divisão de conversas.

## Problema

Quando as conversas com modelos de linguagem ficam muito longas, podem ocorrer problemas como:

1. **Limite de contexto excedido**: Os modelos têm um limite máximo de tokens que podem processar por vez
2. **Degradação de qualidade**: Com contextos muito grandes, a qualidade das respostas pode diminuir
3. **Maior latência**: Conversas longas exigem mais processamento e aumentam o tempo de resposta
4. **Custo mais alto**: Mais tokens significam maior custo por requisição

A mensagem de erro `Your conversation is too long. Please try creating a new conversation or shortening your messages` é um sintoma desse problema.

## Solução

O gerenciador de conversas implementa várias estratégias para lidar com conversas longas:

### 1. Detecção de conversas longas

O sistema verifica automaticamente se uma conversa está se aproximando ou excedendo os limites recomendados, baseado em:
- Contagem de mensagens
- Estimativa de tokens
- Tamanho em caracteres

### 2. Truncagem de conversas

Mantém apenas as mensagens mais recentes (mais relevantes) e descarta as mais antigas, preservando o contexto recente da conversa.

### 3. Resumo de conversas

Gera um resumo textual da conversa, capturando os pontos principais e permitindo que o modelo entenda o contexto geral sem precisar processar toda a conversa.

### 4. Divisão de conversas

Divide uma conversa longa em várias conversas menores, permitindo que o usuário continue a interação em uma nova conversa que mantém o contexto necessário.

## Componentes

### Modelos de dados

- `Message`: Representa uma mensagem individual na conversa
- `Conversation`: Representa uma conversa completa com várias mensagens
- `ConversationSummary`: Versão resumida de uma conversa para listagem

### Classes principais

- `ConversationManager`: Classe que implementa os métodos de gerenciamento de conversas

## API

### Endpoints

- **POST** `/mcp/conversation/check`: Verifica se uma conversa está muito longa
  - Recebe os dados da conversa
  - Retorna estatísticas e um indicador se a conversa é muito longa

- **POST** `/mcp/conversation/action`: Executa uma ação específica em uma conversa
  - Ações suportadas:
    - `truncate`: Trunca a conversa mantendo apenas as mensagens mais recentes
    - `summarize`: Gera um resumo textual da conversa
    - `split`: Divide a conversa em várias conversas menores

- **GET** `/mcp/conversation/list`: Lista todas as conversas do usuário

## Uso

### Verificar tamanho da conversa

```python
from app.apis.mcp.conversation_manager import Message, Conversation, ConversationManager

# Criar uma conversa
messages = [
    Message(role="user", content="Olá, como vai?"),
    Message(role="assistant", content="Estou bem, obrigado! Como posso ajudar?"),
    # ... mais mensagens
]

conversation = Conversation(
    id="conv_123",
    messages=messages,
    title="Minha conversa"
)

# Verificar se a conversa está muito longa
is_too_long = ConversationManager.check_conversation_length(conversation)

if is_too_long:
    # Obter estatísticas detalhadas
    stats = ConversationManager.get_conversation_stats(conversation)
    print(f"A conversa está muito longa! Estatísticas: {stats}")
    
    # Sugerir ações
    print("Sugestões:")
    print("1. Truncar a conversa")
    print("2. Resumir a conversa")
    print("3. Dividir a conversa")
```

### Truncar uma conversa

```python
# Manter apenas as 10 mensagens mais recentes
truncated = ConversationManager.truncate_conversation(conversation, keep_latest=10)
print(f"Conversa truncada: {len(truncated.messages)} mensagens")
```

### Resumir uma conversa

```python
# Gerar um resumo da conversa
summary = ConversationManager.summarize_conversation(conversation)
print(f"Resumo: {summary}")
```

### Dividir uma conversa

```python
# Dividir a conversa em partes com no máximo 15 mensagens cada
parts = ConversationManager.split_conversation(conversation, max_messages_per_part=15)
print(f"Conversa dividida em {len(parts)} partes")
```

## Configurações

Os limites padrão para detectar conversas longas são:

- `MAX_CONVERSATION_TOKENS`: 4000 tokens (aproximadamente)
- `MAX_CONVERSATION_MESSAGES`: 30 mensagens

Esses valores podem ser ajustados conforme necessário para diferentes modelos e casos de uso.

## Considerações futuras

- Implementação de resumo baseado em LLM para melhor qualidade
- Persistência de conversas em banco de dados
- Interface de usuário para gerenciamento de conversas
- Suporte para diferentes modelos e seus limites específicos 