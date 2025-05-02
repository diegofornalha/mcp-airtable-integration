"""
Módulo para automação de deploy do servlet Databutton via XTP.

Este módulo fornece endpoints para gerenciar o ciclo de vida de plugins XTP,
automatizando os processos descritos no DEPLOY_GUIDE.md.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Response, status
import subprocess
import os
import json
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/xtp", tags=["xtp"])

# Modelos de dados
class DeployRequest(BaseModel):
    token: Optional[str] = None
    plugin_name: str = "databutton"
    extension_point: str = "ext_01je4jj1tteaktf0zd0anm8854"

class DeployResponse(BaseModel):
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None

class PluginInfo(BaseModel):
    name: str
    status: str
    version: Optional[str] = None
    created_at: Optional[str] = None
    tools: Optional[List[Dict[str, str]]] = None

# Funções auxiliares
def get_project_root():
    """Retorna o caminho da raiz do projeto"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))

def get_plugin_dir():
    """Retorna o caminho do diretório do plugin"""
    # Retorna o diretório raiz do projeto, pois os scripts estão na raiz
    return get_project_root()

async def run_command(cmd, cwd=None, env=None):
    """Executa um comando e retorna o resultado"""
    try:
        logger.info(f"Executando comando: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info(f"Comando executado com sucesso: {result.stdout.strip()}")
            return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
        else:
            logger.error(f"Erro ao executar comando: {result.stderr}")
            return {"success": False, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        logger.exception(f"Exceção ao executar comando: {str(e)}")
        return {"success": False, "stderr": str(e)}

# Endpoints
@router.get("/status", response_model=DeployResponse)
async def check_xtp_status():
    """
    Verifica se a CLI XTP está instalada e funcionando.
    
    Retorna:
        DeployResponse: Status da CLI XTP
    """
    result = await run_command(["xtp", "--version"])
    
    if result["success"]:
        return DeployResponse(
            status="ok", 
            message=f"XTP CLI instalado: {result['stdout'].strip()}"
        )
    else:
        return DeployResponse(
            status="error",
            message="XTP CLI não está funcionando corretamente",
            details={"error": result["stderr"]}
        )

@router.post("/login", response_model=DeployResponse)
async def xtp_login(token: Optional[str] = None):
    """
    Faz login na plataforma XTP.
    
    Args:
        token (str, opcional): Token XTP para autenticação. Se não fornecido,
                              tenta login interativo.
    
    Retorna:
        DeployResponse: Resultado do login
    """
    if token:
        # Usar token fornecido
        logger.info("Configurando token XTP")
        os.environ["XTP_TOKEN"] = token
        return DeployResponse(
            status="ok",
            message="Token XTP configurado com sucesso"
        )
    else:
        # Iniciar login interativo
        result = await run_command(["xtp", "login"])
        
        if result["success"]:
            return DeployResponse(
                status="ok",
                message="Login XTP realizado com sucesso"
            )
        else:
            return DeployResponse(
                status="error",
                message="Falha ao fazer login no XTP",
                details={"error": result["stderr"]}
            )

@router.post("/build", response_model=DeployResponse)
async def build_plugin():
    """
    Compila o plugin Databutton localmente.
    
    Este endpoint executa os passos:
    1. Executa prepare.sh para instalar dependências
    2. Executa npm run build para compilar o plugin
    
    Retorna:
        DeployResponse: Resultado da compilação
    """
    databutton_dir = get_plugin_dir()
    
    # Preparar o ambiente
    prepare_result = await run_command(
        ["bash", "prepare.sh"], 
        cwd=databutton_dir
    )
    
    if not prepare_result["success"]:
        return DeployResponse(
            status="error",
            message="Falha ao executar prepare.sh",
            details={"error": prepare_result["stderr"]}
        )
    
    # Compilar o plugin
    build_result = await run_command(
        ["npm", "run", "build"], 
        cwd=databutton_dir
    )
    
    if not build_result["success"]:
        return DeployResponse(
            status="error",
            message="Falha ao compilar o plugin",
            details={"error": build_result["stderr"]}
        )
    
    return DeployResponse(
        status="ok",
        message="Plugin compilado com sucesso",
        details={
            "prepare_output": prepare_result["stdout"],
            "build_output": build_result["stdout"]
        }
    )

@router.post("/deploy", response_model=DeployResponse)
async def deploy_plugin(background_tasks: BackgroundTasks, request: DeployRequest = None):
    """
    Faz o deploy do plugin Databutton para o MCP.run.
    
    Este endpoint executa os passos:
    1. Autentica na plataforma XTP (se token fornecido)
    2. Executa prepare.sh e npm run build
    3. Executa xtp plugin push
    
    Args:
        background_tasks: Gerenciador de tarefas em background do FastAPI
        request: Dados para o deploy
    
    Retorna:
        DeployResponse: Status inicial do deploy
    """
    # Configurar token se fornecido
    if request and request.token:
        os.environ["XTP_TOKEN"] = request.token
    
    # Iniciar o processo em background
    background_tasks.add_task(run_deploy_process, request.plugin_name if request else "databutton")
    
    return DeployResponse(
        status="started",
        message="Processo de deploy iniciado em segundo plano",
        details={
            "plugin_name": request.plugin_name if request else "databutton"
        }
    )

async def run_deploy_process(plugin_name: str = "databutton"):
    """
    Executa o processo completo de deploy.
    
    Args:
        plugin_name: Nome do plugin a ser publicado
    """
    databutton_dir = get_plugin_dir()
    
    try:
        # Executar prepare.sh
        prepare_result = await run_command(
            ["bash", "prepare.sh"], 
            cwd=databutton_dir
        )
        
        if not prepare_result["success"]:
            logger.error(f"Erro ao executar prepare.sh: {prepare_result['stderr']}")
            return
            
        # Executar npm run build
        build_result = await run_command(
            ["npm", "run", "build"], 
            cwd=databutton_dir
        )
        
        if not build_result["success"]:
            logger.error(f"Erro ao executar npm run build: {build_result['stderr']}")
            return
            
        # Executar xtp plugin push
        push_result = await run_command(
            ["xtp", "plugin", "push"], 
            cwd=databutton_dir
        )
        
        if not push_result["success"]:
            logger.error(f"Erro ao executar xtp plugin push: {push_result['stderr']}")
        else:
            logger.info(f"Deploy concluído com sucesso: {push_result['stdout']}")
            
    except Exception as e:
        logger.exception(f"Erro durante o processo de deploy: {str(e)}")

@router.get("/plugins", response_model=List[PluginInfo])
async def list_plugins(extension_point: str = "ext_01je4jj1tteaktf0zd0anm8854", show_inactive: bool = False):
    """
    Lista os plugins publicados na plataforma.
    
    Args:
        extension_point: ID do extension point
        show_inactive: Se True, mostra também plugins inativos
    
    Retorna:
        List[PluginInfo]: Lista de plugins publicados
    """
    result = await run_command([
        "xtp", "plugin", "list", 
        "--extension-point", extension_point
    ])
    
    if not result["success"]:
        raise HTTPException(
            status_code=500, 
            detail=f"Falha ao listar plugins: {result['stderr']}"
        )
    
    try:
        # Processar saída de texto, já que a saída JSON não é suportada
        plugins = []
        lines = result["stdout"].strip().split('\n')
        
        # Pular cabeçalho se existir
        start_idx = 0
        for i, line in enumerate(lines):
            if "name" in line.lower() and "status" in line.lower():
                start_idx = i + 1
                break
        
        # Processar linhas de plugins
        for line in lines[start_idx:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    plugin_info = PluginInfo(
                        name=parts[0],
                        status=parts[1],
                        version=parts[2] if len(parts) > 2 else None,
                        created_at=None
                    )
                    # Adicionar apenas plugins ativos se show_inactive for False
                    if show_inactive or plugin_info.version != "Inactive":
                        plugins.append(plugin_info)
            
        return plugins
    except Exception as e:
        logger.exception(f"Erro ao processar a saída: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao processar a resposta da CLI XTP: {str(e)}"
        )

@router.get("/plugin/{plugin_name}", response_model=PluginInfo)
async def get_plugin_info(plugin_name: str, extension_point: str = "ext_01je4jj1tteaktf0zd0anm8854"):
    """
    Obtém informações detalhadas sobre um plugin específico.
    
    Args:
        plugin_name: Nome do plugin
        extension_point: ID do extension point
    
    Retorna:
        PluginInfo: Informações do plugin
    """
    result = await run_command([
        "xtp", "plugin", "view",
        "--name", plugin_name,
        "--extension-point", extension_point
    ])
    
    if not result["success"]:
        raise HTTPException(
            status_code=404 if "not found" in result["stderr"].lower() else 500,
            detail=f"Falha ao obter informações do plugin: {result['stderr']}"
        )
    
    try:
        # Processar saída em formato de texto
        output = result["stdout"]
        plugin_info = PluginInfo(
            name=plugin_name,
            status="unknown",
            version="Installed",
            created_at=None,
            tools=[]
        )
        
        # Extrair informações baseadas em texto
        lines = output.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("Name:"):
                plugin_info.name = line.replace("Name:", "").strip()
            elif line.startswith("Owner:"):
                plugin_info.status = line.replace("Owner:", "").strip()
            elif line.startswith("Status:"):
                plugin_info.version = line.replace("Status:", "").strip()
            elif line.startswith("Updated At:"):
                plugin_info.created_at = line.replace("Updated At:", "").strip()
            
        # Extrair bindings como ferramentas
        tools = []
        binding_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("Bindings:"):
                binding_section = True
                continue
            if binding_section and line.startswith("-"):
                tool_name = line.replace("-", "").strip()
                tools.append({"name": tool_name, "description": f"Ferramenta {tool_name}"})
        
        plugin_info.tools = tools
        return plugin_info
    except Exception as e:
        logger.exception(f"Erro ao processar a saída: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao processar a resposta da CLI XTP: {str(e)}"
        ) 