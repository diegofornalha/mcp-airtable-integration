"""
API MCP para integração com o plugin XTP.

Este módulo fornece endpoints para simulação de funcionalidades MCP.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, List, Any, Union
import logging
import json
from .conversation_manager import Conversation, Message, ConversationManager, ConversationSummary
import os
import subprocess
from fastapi import BackgroundTasks

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["mcp"])

# Modelos de dados
class ToolSchema(BaseModel):
    type: str
    properties: Dict[str, Any] = {}
    description: Optional[str] = None

class Tool(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class ToolsResponse(BaseModel):
    tools: List[Tool]

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    content: str
    error: Optional[str] = None

class LoginRequest(BaseModel):
    token: Optional[str] = None

class LoginResponse(BaseModel):
    status: str
    message: str

class SearchServletsRequest(BaseModel):
    q: str

class SearchServletsResponse(BaseModel):
    results: List[Dict[str, Any]]

class ProfileResponse(BaseModel):
    profiles: List[Dict[str, Any]]

class SetProfileRequest(BaseModel):
    profile: str

class SetProfileResponse(BaseModel):
    status: str
    message: str

# Novos modelos de dados para gerenciamento de conversas
class ConversationRequest(BaseModel):
    id: Optional[str] = None
    messages: List[Dict[str, Any]]
    title: Optional[str] = None

class ConversationResponse(BaseModel):
    id: str
    status: str
    message: str
    is_too_long: bool = False
    conversation_stats: Optional[Dict[str, Any]] = None

class ConversationActionRequest(BaseModel):
    conversation_id: str
    action: str  # "truncate", "summarize", "split"
    params: Optional[Dict[str, Any]] = None

class ConversationActionResponse(BaseModel):
    status: str
    message: str
    result: Any = None

# Novos modelos para gerenciamento de XTP (antigos endpoints /api/xtp/*)
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

# Funções auxiliares para XTP
def get_project_root():
    """Retorna o caminho da raiz do projeto"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))

def get_plugin_dir():
    """Retorna o caminho do diretório do plugin"""
    # Agora retorna o diretório databutton-test na nova estrutura organizada
    return os.path.join(get_project_root(), "databutton-test")

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
@router.get("/tools", response_model=ToolsResponse)
async def list_tools():
    """
    Lista todas as ferramentas disponíveis no servidor local.
    
    Retorna:
        ToolsResponse: Lista de ferramentas
    """
    tools = [
        Tool(
            name="check_health",
            description="Verifica a saúde do servidor FastAPI.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="mcp_query",
            description="Consulta o servidor MCP.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta a ser enviada ao servidor MCP"
                    },
                    "context": {
                        "type": "object",
                        "description": "Contexto adicional para a consulta"
                    }
                }
            }
        ),
        Tool(
            name="mcp_query_stream",
            description="Consulta o servidor MCP com resposta em streaming.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta a ser enviada ao servidor MCP em modo streaming"
                    },
                    "context": {
                        "type": "object",
                        "description": "Contexto adicional para a consulta streaming"
                    }
                }
            }
        )
    ]
    
    return ToolsResponse(tools=tools)

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Consulta o servidor MCP.
    
    Args:
        request: Os dados da consulta
    
    Retorna:
        QueryResponse: Resposta da consulta
    """
    try:
        return QueryResponse(
            content=f"Resposta para consulta: {request.query}",
        )
    except Exception as e:
        logger.exception(f"Erro na consulta: {str(e)}")
        return QueryResponse(
            content="",
            error=str(e)
        )

@router.post("/query/stream")
async def query_stream(request: QueryRequest):
    """
    Consulta o servidor MCP com resposta em streaming.
    
    Args:
        request: Os dados da consulta
    
    Retorna:
        StreamingResponse: Resposta da consulta em streaming
    """
    try:
        return QueryResponse(
            content=f"Resposta streaming para consulta: {request.query}",
        )
    except Exception as e:
        logger.exception(f"Erro na consulta streaming: {str(e)}")
        return QueryResponse(
            content="",
            error=str(e)
        )

@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Função para login no MCP.run.
    
    Args:
        request: Dados de login
    
    Retorna:
        LoginResponse: Resultado do login
    """
    return LoginResponse(
        status="success",
        message="Login simulado com sucesso"
    )

@router.post("/search/servlets", response_model=SearchServletsResponse)
async def search_servlets(request: SearchServletsRequest):
    """
    Função para pesquisar servlets no MCP.run.
    
    Args:
        request: Termos de pesquisa
    
    Retorna:
        SearchServletsResponse: Resultados da pesquisa
    """
    return SearchServletsResponse(
        results=[
            {
                "name": "Exemplo Servlet",
                "description": f"Servlet de exemplo relacionado a: {request.q}",
                "owner": "usuario_exemplo",
                "id": "srv_example123"
            }
        ]
    )

@router.get("/profiles", response_model=ProfileResponse)
async def get_profiles():
    """
    Função para obter perfis do usuário no MCP.run.
    
    Retorna:
        ProfileResponse: Lista de perfis
    """
    return ProfileResponse(
        profiles=[
            {
                "id": "profile1",
                "name": "Default Profile",
                "isActive": True
            },
            {
                "id": "profile2",
                "name": "Dev Profile",
                "isActive": False
            }
        ]
    )

@router.post("/profiles/set", response_model=SetProfileResponse)
async def set_profile(request: SetProfileRequest):
    """
    Função para definir o perfil ativo no MCP.run.
    
    Args:
        request: Perfil a ser ativado
    
    Retorna:
        SetProfileResponse: Resultado da operação
    """
    return SetProfileResponse(
        status="success",
        message=f"Perfil {request.profile} ativado com sucesso"
    )

# Novos endpoints para gerenciamento de conversas
@router.post("/conversation/check", response_model=ConversationResponse)
async def check_conversation(request: ConversationRequest):
    """
    Verifica se uma conversa está muito longa.
    
    Args:
        request: Dados da conversa
    
    Retorna:
        ConversationResponse: Resultado da verificação
    """
    try:
        # Converte para nosso modelo de dados
        messages = [
            Message(
                role=msg.get("role", "user"),
                content=msg.get("content", ""),
                timestamp=msg.get("timestamp")
            )
            for msg in request.messages
        ]
        
        conversation = Conversation(
            id=request.id or "temp_conv_id",
            messages=messages,
            title=request.title
        )
        
        # Verifica se a conversa está muito longa
        is_too_long = ConversationManager.check_conversation_length(conversation)
        
        # Obtém estatísticas da conversa
        stats = ConversationManager.get_conversation_stats(conversation)
        
        return ConversationResponse(
            id=conversation.id,
            status="warning" if is_too_long else "ok",
            message="A conversa está muito longa e pode causar problemas de contexto." if is_too_long else "A conversa está dentro dos limites aceitáveis.",
            is_too_long=is_too_long,
            conversation_stats=stats
        )
    except Exception as e:
        logger.exception(f"Erro ao verificar conversa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar conversa: {str(e)}")

@router.post("/conversation/action", response_model=ConversationActionResponse)
async def perform_conversation_action(request: ConversationActionRequest):
    """
    Realiza uma ação em uma conversa (truncar, resumir ou dividir).
    
    Args:
        request: Dados da ação a ser realizada
    
    Retorna:
        ConversationActionResponse: Resultado da ação
    """
    try:
        # Simulação - em um ambiente real, buscaria a conversa no banco de dados
        # Para fins de demonstração, criamos uma conversa de exemplo
        messages = [
            Message(role="user", content=f"Mensagem de exemplo {i}") 
            for i in range(1, 40)
        ]
        
        conversation = Conversation(
            id=request.conversation_id,
            messages=messages,
            title="Conversa de exemplo"
        )
        
        result = None
        message = ""
        
        # Executa a ação solicitada
        if request.action == "truncate":
            keep_latest = request.params.get("keep_latest", 10) if request.params else 10
            result = ConversationManager.truncate_conversation(conversation, keep_latest)
            message = f"Conversa truncada para as {keep_latest} mensagens mais recentes."
        
        elif request.action == "summarize":
            result = ConversationManager.summarize_conversation(conversation)
            message = "Resumo da conversa gerado com sucesso."
        
        elif request.action == "split":
            max_messages = request.params.get("max_messages_per_part", 15) if request.params else 15
            result = ConversationManager.split_conversation(conversation, max_messages)
            message = f"Conversa dividida em {len(result)} partes."
        
        else:
            raise HTTPException(status_code=400, detail=f"Ação desconhecida: {request.action}")
        
        return ConversationActionResponse(
            status="success",
            message=message,
            result=result
        )
    except Exception as e:
        logger.exception(f"Erro ao executar ação na conversa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar ação na conversa: {str(e)}")

@router.get("/conversation/list", response_model=List[ConversationSummary])
async def list_conversations():
    """
    Lista as conversas do usuário.
    
    Retorna:
        List[ConversationSummary]: Lista de resumos das conversas
    """
    # Simulação - em um ambiente real, buscaria as conversas no banco de dados
    return [
        ConversationSummary(
            id="conv_1",
            title="Conversa de exemplo 1",
            message_count=15,
            last_updated="2023-06-01T12:00:00Z",
            is_truncated=False
        ),
        ConversationSummary(
            id="conv_2",
            title="Conversa de exemplo 2",
            message_count=35,
            last_updated="2023-06-02T15:30:00Z",
            is_truncated=True
        )
    ]

# Endpoints adicionados (anteriormente em /api/xtp)
@router.get("/xtp/status", response_model=DeployResponse)
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

@router.post("/xtp/login", response_model=DeployResponse)
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

@router.post("/xtp/build", response_model=DeployResponse)
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

@router.post("/xtp/deploy", response_model=DeployResponse)
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
    
    # Iniciar processo de deploy em background
    background_tasks.add_task(
        run_deploy_process,
        plugin_name=request.plugin_name if request else "databutton"
    )
    
    return DeployResponse(
        status="pending",
        message="Processo de deploy iniciado em segundo plano"
    )

async def run_deploy_process(plugin_name: str = "databutton"):
    """
    Executa o processo completo de deploy do plugin.
    
    Args:
        plugin_name: Nome do plugin
    """
    try:
        databutton_dir = get_plugin_dir()
        
        # Preparar o ambiente
        prepare_result = await run_command(
            ["bash", "prepare.sh"], 
            cwd=databutton_dir
        )
        
        if not prepare_result["success"]:
            logger.error(f"Falha ao executar prepare.sh: {prepare_result['stderr']}")
            return
        
        # Compilar o plugin
        build_result = await run_command(
            ["npm", "run", "build"], 
            cwd=databutton_dir
        )
        
        if not build_result["success"]:
            logger.error(f"Falha ao compilar o plugin: {build_result['stderr']}")
            return
        
        # Fazer o deploy do plugin
        deploy_result = await run_command(
            ["xtp", "plugin", "push"], 
            cwd=databutton_dir
        )
        
        if deploy_result["success"]:
            logger.info(f"Plugin {plugin_name} implantado com sucesso")
        else:
            logger.error(f"Falha ao implantar o plugin: {deploy_result['stderr']}")
            
    except Exception as e:
        logger.exception(f"Erro no processo de deploy: {str(e)}")

@router.get("/xtp/plugins", response_model=List[PluginInfo])
async def list_plugins(extension_point: str = "ext_01je4jj1tteaktf0zd0anm8854", show_inactive: bool = False):
    """
    Lista todos os plugins do usuário.
    
    Args:
        extension_point: ID do extension point
        show_inactive: Se deve mostrar plugins inativos
    
    Retorna:
        List[PluginInfo]: Lista de plugins
    """
    try:
        result = await run_command(["xtp", "plugin", "list", "--json"])
        
        if not result["success"]:
            raise HTTPException(
                status_code=500, 
                detail=f"Falha ao listar plugins: {result['stderr']}"
            )
        
        try:
            plugins_data = json.loads(result["stdout"])
            plugins = []
            
            for plugin in plugins_data:
                # Filtrar pelo extension point
                if "extension_point_id" in plugin and plugin["extension_point_id"] == extension_point:
                    # Filtrar por status se necessário
                    if not show_inactive and "status" in plugin and plugin["status"] != "installed":
                        continue
                    
                    plugins.append(PluginInfo(
                        name=plugin.get("name", "Unknown"),
                        status=plugin.get("status", "Unknown"),
                        version=plugin.get("version", None),
                        created_at=plugin.get("created_at", None)
                    ))
            
            return plugins
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, 
                detail="Falha ao decodificar resposta JSON da CLI XTP"
            )
            
    except Exception as e:
        logger.exception(f"Erro ao listar plugins: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar plugins: {str(e)}"
        )

@router.get("/xtp/plugin/{plugin_name}", response_model=PluginInfo)
async def get_plugin_info(plugin_name: str, extension_point: str = "ext_01je4jj1tteaktf0zd0anm8854"):
    """
    Obtém informações sobre um plugin específico.
    
    Args:
        plugin_name: Nome do plugin
        extension_point: ID do extension point
    
    Retorna:
        PluginInfo: Informações do plugin
    """
    try:
        result = await run_command([
            "xtp", "plugin", "view", 
            "--name", plugin_name,
            "--extension-point", extension_point,
            "--json"
        ])
        
        if not result["success"]:
            raise HTTPException(
                status_code=404, 
                detail=f"Plugin não encontrado: {result['stderr']}"
            )
        
        try:
            plugin_data = json.loads(result["stdout"])
            
            # Obter a lista de ferramentas do plugin
            tools = []
            if "tools" in plugin_data:
                for tool in plugin_data["tools"]:
                    tools.append({
                        "name": tool.get("name", "Unknown"),
                        "description": tool.get("description", "")
                    })
            
            return PluginInfo(
                name=plugin_data.get("name", "Unknown"),
                status=plugin_data.get("status", "Unknown"),
                version=plugin_data.get("version", None),
                created_at=plugin_data.get("updated_at", None),
                tools=tools
            )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, 
                detail="Falha ao decodificar resposta JSON da CLI XTP"
            )
            
    except Exception as e:
        logger.exception(f"Erro ao obter informações do plugin: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao obter informações do plugin: {str(e)}"
        ) 