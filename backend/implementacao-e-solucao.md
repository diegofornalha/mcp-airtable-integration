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

## Melhorias no Script de Execução

### Problemas com o script run.sh original

O script `run.sh` original apresentava várias limitações:

1. Não verificava a existência do arquivo `main.py`
2. Não detectava corretamente o comando Python (python vs python3)
3. Não criava ambiente virtual quando não encontrava um
4. Não lidava bem com falhas na instalação de dependências
5. Usava apenas a porta 9000, ignorando a porta 8000 do main.py

### Nova Implementação do run.sh

Implementamos um script `run.sh` mais robusto que:

1. **Detecção Inteligente de Ambiente**
   - Identifica automaticamente o diretório do script
   - Verifica a existência do arquivo `main.py` e navega para o diretório correto
   - Detecta automaticamente `python` ou `python3` e `pip` ou `pip3`

2. **Gerenciamento de Ambiente Virtual**
   - Verifica múltiplos caminhos para ambientes virtuais
   - Cria automaticamente um ambiente virtual quando não encontra nenhum
   - Fornece mensagens claras sobre qual ambiente está sendo usado

3. **Instalação Flexível de Dependências**
   - Separa a verificação de dependências básicas (fastapi, uvicorn) e opcionais (fastapi-mcp)
   - Usa `requirements-essencial.txt` quando disponível
   - Tenta múltiplas estratégias para instalar o pacote fastapi-mcp:
     - Instalação via pip padrão
     - Instalação direta do GitHub quando o pip falha

4. **Gestão Inteligente de Portas**
   - Tenta usar a porta 8000 primeiro (mesma do `main.py`)
   - Se ocupada, tenta as portas 9000, 9001 e 9002 em sequência
   - Exibe mensagens informativas sobre qual porta está sendo usada

5. **Melhor Experiência do Usuário**
   - Usa cores para destacar mensagens importantes
   - Fornece URLs para acessar diferentes endpoints
   - Fornece instruções claras para resolução de problemas

### Como Executar o Servidor com o Novo Script

```bash
cd backend
chmod +x run.sh  # Certifique-se que o script tem permissão de execução
./run.sh
```

O script agora:
1. Detecta automaticamente o ambiente e dependências
2. Instala os pacotes necessários
3. Identifica uma porta disponível
4. Inicia o servidor com mensagens claras

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
   - Compatibilidade com portas 8000 ou 9000

## Considerações sobre Portas

O `main.py` usa a porta 8000 por padrão, mas o script `run.sh` agora é inteligente o suficiente para:

1. Tentar a porta 8000 primeiro (mantendo consistência com o código)
2. Se ocupada, tentar portas alternativas (9000, 9001, 9002)
3. Exibir claramente qual porta está sendo usada

Isso resolve o problema de conflito de portas de forma elegante, mantendo a consistência entre o código e o script de execução.

## Conclusão

O servidor MCP agora é funcional com o `main.py`, evitando a dependência problemática do databutton. A implementação mantém todas as funcionalidades essenciais para um servidor MCP, permitindo que o Cursor ou outros clientes MCP possam se conectar e utilizar as ferramentas expostas.

Com o novo script `run.sh`, a execução do servidor é muito mais robusta, adaptável a diferentes configurações de ambiente, e fornece feedback claro ao usuário em cada etapa. Essa abordagem resolve todos os problemas identificados anteriormente e segue os princípios de engenharia de software de isolar problemas e construir soluções incrementais até obter um sistema funcional e fácil de usar. 