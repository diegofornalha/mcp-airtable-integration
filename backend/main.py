from fastapi import FastAPI, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from fastapi_mcp.server import FastApiMCP
from datetime import datetime
import importlib.util
import os
import sys

# Modelo para a requisição MCP
class MCPRequest(BaseModel):
    message: Optional[str] = None
    messages: Optional[List[Dict[str, str]]] = None
    instructions: Optional[str] = None

# Cria a aplicação FastAPI
app = FastAPI(title="API MCP Local")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de ferramentas MCP disponíveis
mcp_tools = [
    {
        "name": "check_health",
        "description": "Check health of application. Returns 200 when OK, 500 when not."
    },
    {
        "name": "mcp_list_tools",
        "description": "Lista as ferramentas disponíveis no servidor MCP rodando localmente."
    },
    {
        "name": "mcp_query",
        "description": "Consulta o servidor MCP do aplicativo rodando localmente."
    },
    {
        "name": "mcp_query_stream",
        "description": "Consulta o servidor MCP do aplicativo com resposta em streaming."
    },
    {
        "name": "deploy_xtp",
        "description": "Realiza o deploy de um plugin XTP para a plataforma MCP.run."
    }
]

# Endpoint para verificar a saúde da aplicação
@app.get("/health")
async def check_health():
    return {"status": "OK"}

# Endpoint para listar as ferramentas disponíveis
@app.get("/tools")
async def list_tools():
    return {"tools": mcp_tools}

# Endpoint MCP para consultas
@app.post("/mcp/query")
async def mcp_query(request: MCPRequest):
    response = "Este é um exemplo de resposta do servidor MCP local."
    if request.message:
        response = f"Recebi sua mensagem: '{request.message}'"
    elif request.messages:
        response = f"Recebi {len(request.messages)} mensagens."
    
    return {"response": response}

# Endpoint para obter o horário do servidor
@app.get("/server-time")
async def get_server_time():
    """Obtém a hora atual do servidor."""
    return {"time": datetime.now().isoformat()}

# Rota raiz
@app.get("/")
async def root():
    return {"message": "Bem-vindo ao servidor MCP local"}

# Importação dinâmica do módulo XTP se disponível
try:
    from app.apis.xtp import router as xtp_router
    app.include_router(xtp_router, prefix="/api")
    print("Módulo XTP carregado com sucesso")
except ImportError as e:
    print(f"Aviso: Módulo XTP não pôde ser importado: {e}")
    # Tenta o caminho alternativo de importação
    try:
        # Adiciona o diretório atual ao path para importações relativas
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Verifica se o módulo existe no caminho app/apis/xtp/__init__.py
        xtp_module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "apis", "xtp", "__init__.py")
        if os.path.exists(xtp_module_path):
            spec = importlib.util.spec_from_file_location("xtp_module", xtp_module_path)
            xtp_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(xtp_module)
            
            # Verifica se o módulo tem um router
            if hasattr(xtp_module, "router"):
                app.include_router(xtp_module.router, prefix="/api")
                print("Módulo XTP carregado via importação dinâmica")
    except Exception as e:
        print(f"Erro ao carregar módulo XTP via importação dinâmica: {e}")

# Adicionar servidor MCP
mcp_server = FastApiMCP(
    fastapi=app,           # Aplicação FastAPI
    name="MCP Local API",  # Nome para o servidor MCP
)

# Montar o servidor MCP
mcp_server.mount(mount_path="/mcp-api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 