# Módulo XTP para Deploy Automatizado

Este módulo fornece uma API para automatizar o processo de deploy de plugins XTP para a plataforma MCP.run, substituindo os passos manuais descritos no DEPLOY_GUIDE.md.

## Funcionalidades

O módulo XTP expõe endpoints REST para:

- Verificar o status da CLI XTP
- Fazer login na plataforma XTP
- Compilar plugins localmente
- Publicar plugins na plataforma MCP.run
- Listar plugins publicados
- Obter informações detalhadas sobre plugins específicos

## Endpoints Disponíveis

### Verificação de Status

```
GET /api/xtp/status
```

Verifica se a CLI XTP está instalada e funcionando corretamente.

**Resposta de Exemplo:**
```json
{
  "status": "ok",
  "message": "XTP CLI instalado: XTP CLI 0.1.8"
}
```

### Login na Plataforma

```
POST /api/xtp/login
```

**Parâmetros (JSON):**
```json
{
  "token": "xtp0_SEU_TOKEN_AQUI"
}
```

**Resposta de Exemplo:**
```json
{
  "status": "ok",
  "message": "Token XTP configurado com sucesso"
}
```

### Compilação de Plugin

```
POST /api/xtp/build
```

Compila o plugin Databutton localmente, executando `prepare.sh` e `npm run build`.

**Resposta de Exemplo:**
```json
{
  "status": "ok",
  "message": "Plugin compilado com sucesso",
  "details": {
    "prepare_output": "...",
    "build_output": "..."
  }
}
```

### Deploy de Plugin

```
POST /api/xtp/deploy
```

**Parâmetros (JSON):**
```json
{
  "token": "xtp0_SEU_TOKEN_AQUI",
  "plugin_name": "databutton",
  "extension_point": "ext_01je4jj1tteaktf0zd0anm8854"
}
```

Inicia o processo de deploy em segundo plano, que inclui:
1. Login na plataforma (se token fornecido)
2. Compilação do plugin
3. Publicação do plugin

**Resposta de Exemplo:**
```json
{
  "status": "started",
  "message": "Processo de deploy iniciado em segundo plano",
  "details": {
    "plugin_name": "databutton"
  }
}
```

### Listar Plugins

```
GET /api/xtp/plugins
```

**Parâmetros (Query):**
- `extension_point` (opcional): ID do extension point (padrão: "ext_01je4jj1tteaktf0zd0anm8854")

**Resposta de Exemplo:**
```json
[
  {
    "name": "databutton",
    "status": "installed",
    "version": "ver_01jrvqy78eesaax1xk257br78w",
    "created_at": "2025-04-15T03:34:48.550Z"
  }
]
```

### Obter Informações de Plugin

```
GET /api/xtp/plugin/{plugin_name}
```

**Parâmetros (Path):**
- `plugin_name`: Nome do plugin

**Parâmetros (Query):**
- `extension_point` (opcional): ID do extension point

**Resposta de Exemplo:**
```json
{
  "name": "databutton",
  "status": "installed",
  "version": "ver_01jrvqy78eesaax1xk257br78w",
  "created_at": "2025-04-15T03:34:48.550Z",
  "tools": [
    {
      "name": "check_health",
      "description": "Verifica a saúde do servidor"
    },
    {
      "name": "mcp_run_login",
      "description": "Realiza login no MCP.run"
    }
  ]
}
```

## Exemplo de Uso com curl

### Verificar Status da CLI XTP

```bash
curl -X GET http://localhost:8000/api/xtp/status
```

### Fazer Login

```bash
curl -X POST http://localhost:8000/api/xtp/login \
  -H "Content-Type: application/json" \
  -d '{"token": "xtp0_SEU_TOKEN_AQUI"}'
```

### Compilar Plugin

```bash
curl -X POST http://localhost:8000/api/xtp/build
```

### Fazer Deploy

```bash
curl -X POST http://localhost:8000/api/xtp/deploy \
  -H "Content-Type: application/json" \
  -d '{"token": "xtp0_SEU_TOKEN_AQUI"}'
```

### Listar Plugins

```bash
curl -X GET http://localhost:8000/api/xtp/plugins
```

### Obter Informações de Plugin

```bash
curl -X GET http://localhost:8000/api/xtp/plugin/databutton
```

## Comparação com o Processo Manual

Este módulo automatiza os seguintes passos do `DEPLOY_GUIDE.md`:

1. **Instalação e autenticação da CLI XTP**
   - ✅ Verifica se a CLI está instalada
   - ✅ Permite autenticação via token

2. **Configuração e Publicação do Servlet**
   - ✅ Executa prepare.sh para instalar dependências
   - ✅ Compila o plugin com npm run build
   - ✅ Publica o plugin com xtp plugin push

3. **Verificação da Publicação**
   - ✅ Lista plugins publicados
   - ✅ Obtém informações detalhadas do plugin

## Considerações de Segurança

- O token XTP deve ser tratado como informação sensível
- Em produção, considere implementar autenticação para esses endpoints
- Os comandos são executados no servidor, portanto certifique-se de que o ambiente está devidamente protegido 