# Documentação do Módulo databutton_app

## Visão Geral

O módulo `databutton_app` é um componente de autenticação e autorização para aplicações FastAPI integradas com o Databutton. Sua principal função é fornecer middleware (mw) para autenticação de usuários através de tokens JWT (JSON Web Tokens).

## Estrutura do Módulo

```
databutton_app/
└── mw/
    ├── __init__.py
    └── auth_mw.py
```

O módulo está organizado da seguinte forma:
- **mw/**: Subpacote de middleware
  - **auth_mw.py**: Implementa funcionalidades de autenticação e autorização

## Funcionalidades Principais

### 1. Autenticação com JWT

O módulo implementa um sistema de autenticação baseado em JWT (JSON Web Tokens) que:
- Verifica tokens JWT recebidos em requisições HTTP e conexões WebSocket
- Valida assinaturas usando chaves obtidas de um servidor JWKS (JSON Web Key Set)
- Verifica audiência e outros campos do token

### 2. Modelos de Dados

#### AuthConfig

```python
class AuthConfig(BaseModel):
    jwks_url: str      # URL do serviço JWKS para verificação de chaves
    audience: str      # Audiência esperada nos tokens
    header: str        # Nome do cabeçalho HTTP que contém o token
```

#### User

```python
class User(BaseModel):
    sub: str           # Identificador único do usuário (subject)
    user_id: str | None = None
    name: str | None = None
    picture: str | None = None
    email: str | None = None
```

### 3. Funções Principais

#### get_authorized_user

Esta é a função central do middleware. Quando usada como dependência em rotas FastAPI, ela:
1. Extrai o token de autenticação da requisição
2. Verifica a validade do token
3. Retorna informações do usuário autenticado
4. Lança exceções apropriadas em caso de falha

```python
def get_authorized_user(request: HTTPConnection) -> User:
    # Extrai, valida o token e retorna o usuário
    # ou lança exceção de não autorizado
```

#### authorize_request e authorize_websocket

Funções específicas para extrair e validar tokens de diferentes tipos de conexões:
- `authorize_request`: Para requisições HTTP padrão
- `authorize_websocket`: Para conexões WebSocket

## Integração com FastAPI

O módulo é projetado para ser usado como uma dependência em rotas FastAPI:

```python
from fastapi import Depends
from databutton_app.mw.auth_mw import get_authorized_user, User

@app.get("/protected-route")
async def protected_endpoint(user: User = Depends(get_authorized_user)):
    return {"message": f"Olá, {user.name or user.sub}!"}
```

## Configuração

Para utilizar este middleware, é necessário configurar a aplicação FastAPI com um objeto AuthConfig:

```python
from databutton_app.mw.auth_mw import AuthConfig

# Na inicialização da aplicação
app.state.auth_config = AuthConfig(
    jwks_url="https://www.googleapis.com/service_accounts/v1/jwk/...",
    audience="seu-projeto-id",
    header="authorization"
)
```

## Formato do Token Databutton

Os tokens Databutton seguem um formato específico:

```
dbtk-v1-[dados codificados]
```

### Componentes do Token

Ao decodificar a parte dos dados do token, obtemos informações importantes:

- **ver**: Versão do token (geralmente "1")
- **keyId**: Identificador da chave de API (ex: "dbtk-1-14b67SDi4Aqw")
- **appId**: Identificador único da aplicação Databutton (ex: "02163e37-eae4-47fb-b08f-750f32322499")
- **env**: Ambiente de execução (ex: "prodx" para produção)
- **type**: Tipo de autenticação (ex: "fb" para Firebase)
- **tok**: Token de autenticação Firebase codificado

Estas informações são utilizadas pelo middleware para:
1. Identificar a aplicação correta
2. Verificar o ambiente de execução
3. Determinar o método de autenticação
4. Validar o token junto ao serviço apropriado (Firebase neste caso)

## Observações Importantes

1. **Segurança**: Este módulo é crítico para a segurança da aplicação, pois controla o acesso a recursos protegidos.

2. **Dependência externa**: Depende de serviços JWKS externos para validação de chaves.

3. **Cache de chaves**: Implementa cache de clientes JWKS e chaves de assinatura para melhorar o desempenho.

4. **Suporte a protocolos**: Oferece suporte tanto para requisições HTTP quanto WebSocket.

## Uso no Projeto

No contexto do projeto MCP-CLI, este módulo é utilizado pelo arquivo `main.py` original para proteção de rotas da API. A dependência `get_authorized_user` é injetada nas rotas que requerem autenticação.

---

**Nota**: Este módulo depende do pacote `databutton` que não está mais sendo utilizado na versão atual do projeto. A implementação simplificada atual (`main.py`) não utiliza autenticação para facilitar o desenvolvimento e testes locais. 