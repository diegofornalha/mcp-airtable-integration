# Este arquivo serve como a API para interagir com o agente no playground.
# Usuários podem criar endpoints adicionais para ferramentas que ficarão automaticamente disponíveis para o agente.

import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, AsyncGenerator
import databutton as db
from openai import AsyncOpenAI
from datetime import datetime
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from openai.types.responses import ResponseTextDeltaEvent
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from app.env import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Desabilitar tracing
set_tracing_disabled(True)

# Obter a chave da API OpenAI de forma segura
try:
    OPENAI_API_KEY = db.secrets.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Chave da API OpenAI não configurada.")
except Exception as e:
    logger.error(f"Falha ao obter a chave da API OpenAI: {str(e)}")
    raise HTTPException(status_code=500, detail="Erro interno: Problema na configuração da chave da API")

router = APIRouter(prefix="/chat")

# Prompt padrão do sistema com a data atual
SYSTEM_PROMPT = f"""
Você é um assistente útil que pode responder perguntas sobre este aplicativo.
Este aplicativo é um modelo para trabalhar com o Model Context Protocol (MCP).
A data de hoje é {datetime.now().strftime('%B %d, %Y')}.
Use as ferramentas disponíveis para ajudar os usuários a entender o aplicativo.
"""

class MessageItem(BaseModel):
    role: str  # "user" ou "assistant"
    content: str

class MCPRequest(BaseModel):
    message: Optional[str] = Field(default=None, description="Uma única mensagem para enviar ao agente")
    messages: Optional[List[MessageItem]] = Field(default=None, description="Lista de mensagens com papéis e conteúdo")
    stream: Optional[bool] = Field(default=False, description="Se a resposta deve ser transmitida em streaming")
    instructions: Optional[str] = Field(default=None, description="Instruções personalizadas para substituir o prompt padrão")

    @root_validator(pre=True)
    def check_message_or_messages(cls, values):
        message, messages = values.get("message"), values.get("messages")
        if message is None and messages is None:
            raise ValueError("É necessário fornecer 'message' ou 'messages'")
        return values

class MCPResponse(BaseModel):
    response: str

class ToolSchema(BaseModel):
    name: str
    description: str

class ListToolResponse(BaseModel):
    tools: List[ToolSchema]

@router.get("/tools", response_model=ListToolResponse)
async def mcp_list_tools():
    """
    Lista as ferramentas disponíveis no servidor MCP rodando localmente.
    Ferramentas começando com 'mcp_' são excluídas da resposta.
    """
    try:
        async with MCPServerSse(
            name="Local MCP Server",
            params={"url": os.environ.get("INTERNAL_MCP_SSE_URL", "http://localhost:9000/internal/sse")},
        ) as mcp_server:
            tools = await mcp_server.list_tools()
            # Filtra e simplifica a lista de ferramentas
            tool_list = [
                ToolSchema(name=tool.name, description=tool.description)
                for tool in tools if not tool.name.startswith("mcp_")
            ]
            return ListToolResponse(tools=tool_list)
    except Exception as e:
        logger.error(f"Falha ao listar ferramentas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Falha ao listar ferramentas: {str(e)}")

@router.post("/query", response_model=MCPResponse)
async def mcp_query(body: MCPRequest):
    """
    Consulta o servidor MCP do aplicativo rodando localmente.

    Este endpoint cria uma conexão com um servidor MCP local e executa um agente que interage com as ferramentas fornecidas por esse servidor.

    Parâmetros:
    - message: A mensagem a ser enviada ao agente
    - messages: Lista opcional de mensagens com papel e conteúdo
    - instructions: Instruções personalizadas opcionais para substituir o prompt padrão

    Retorna:
    - response: A resposta do agente
    """
    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        async with MCPServerSse(
            name="Local MCP Server",
            params={"url": os.environ.get("INTERNAL_MCP_SSE_URL", "http://localhost:9000/internal/sse")},
        ) as mcp_server:
            agent = Agent(
                name="Assistant",
                instructions=body.instructions if body.instructions else SYSTEM_PROMPT,
                mcp_servers=[mcp_server],
                model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=client),
                model_settings=ModelSettings(tool_choice="auto"),
            )
            if body.messages:
                input_messages = [{"role": msg.role, "content": msg.content} for msg in body.messages]
                result = await Runner.run(starting_agent=agent, input=input_messages)
            else:
                result = await Runner.run(starting_agent=agent, input=body.message)
            return MCPResponse(response=result.final_output)
    except Exception as e:
        logger.error(f"Falha na consulta MCP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Falha na consulta MCP: {str(e)}")

@router.post("/query/stream", tags=["stream"])
async def mcp_query_stream(body: MCPRequest):
    """
    Consulta o servidor MCP do aplicativo com resposta em streaming.

    Este endpoint cria uma conexão com um servidor MCP local e transmite a resposta do agente em tempo real.

    Parâmetros:
    - message: A mensagem a ser enviada ao agente
    - messages: Lista opcional de mensagens com papel e conteúdo
    - instructions: Instruções personalizadas opcionais para substituir o prompt padrão

    Retorna:
    - Uma resposta em streaming com a saída do agente
    """
    async def generate_response() -> AsyncGenerator[str, None]:
        try:
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            async with MCPServerSse(
                name="Local MCP Server",
                params={"url": os.environ.get("INTERNAL_MCP_SSE_URL", "http://localhost:9000/internal/sse")},
            ) as mcp_server:
                agent = Agent(
                    name="Assistant",
                    instructions=body.instructions if body.instructions else SYSTEM_PROMPT,
                    mcp_servers=[mcp_server],
                    model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=client),
                    model_settings=ModelSettings(tool_choice="auto"),
                )
                if body.messages:
                    input_messages = [{"role": msg.role, "content": msg.content} for msg in body.messages]
                    result = Runner.run_streamed(agent, input=input_messages)
                else:
                    result = Runner.run_streamed(agent, input=body.message)
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        if event.data.delta:
                            yield event.data.delta
        except Exception as e:
            logger.error(f"Falha na consulta MCP em streaming: {str(e)}")
            yield f"Erro: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")