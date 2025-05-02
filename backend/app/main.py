from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import uvicorn
from app.apis.mcp import router as mcp_router

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="MCP API Server",
    description="API para interação com MCP",
    version="0.1.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router MCP (agora contém também os endpoints XTP)
app.include_router(mcp_router, prefix="/api")

# Endpoint raiz
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "MCP API Server"}

# Endpoint de saúde
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "message": "Servidor em execução"}

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 