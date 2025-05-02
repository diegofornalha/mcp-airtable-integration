"""
Gerenciador de Conversas para o MCP.

Este módulo fornece funcionalidades para gerenciar conversas longas,
incluindo detecção de tamanho, resumo e divisão de conversas.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definição dos modelos
class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class Conversation(BaseModel):
    id: str
    messages: List[Message]
    title: Optional[str] = None
    token_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ConversationSummary(BaseModel):
    id: str
    title: str
    message_count: int
    last_updated: Optional[str] = None
    is_truncated: bool = False

# Configurações
MAX_CONVERSATION_TOKENS = 4000  # Limite aproximado (ajustar conforme necessário)
MAX_CONVERSATION_MESSAGES = 30  # Limite de mensagens

class ConversationManager:
    """
    Gerenciador de conversas para lidar com conversas muito longas.
    """
    
    @staticmethod
    def check_conversation_length(conversation: Conversation) -> bool:
        """
        Verifica se uma conversa está muito longa.
        
        Args:
            conversation: A conversa a ser verificada
            
        Returns:
            bool: True se a conversa for muito longa, False caso contrário
        """
        # Verificação baseada em número de mensagens
        if len(conversation.messages) > MAX_CONVERSATION_MESSAGES:
            return True
            
        # Verificação baseada em tokens (se disponível)
        if conversation.token_count and conversation.token_count > MAX_CONVERSATION_TOKENS:
            return True
            
        # Estimativa grosseira de tokens baseada em caracteres (4 caracteres ~ 1 token)
        char_count = sum(len(msg.content) for msg in conversation.messages)
        estimated_tokens = char_count // 4
        
        return estimated_tokens > MAX_CONVERSATION_TOKENS
    
    @staticmethod
    def truncate_conversation(conversation: Conversation, keep_latest: int = 10) -> Conversation:
        """
        Trunca uma conversa mantendo apenas as mensagens mais recentes.
        
        Args:
            conversation: A conversa a ser truncada
            keep_latest: Número de mensagens mais recentes a manter
            
        Returns:
            Conversation: A conversa truncada
        """
        if len(conversation.messages) <= keep_latest:
            return conversation
            
        # Mantém apenas as mensagens mais recentes
        truncated = Conversation(
            id=conversation.id,
            title=conversation.title,
            messages=conversation.messages[-keep_latest:],
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
        
        # Adiciona uma mensagem de sistema no início informando sobre a truncagem
        system_msg = Message(
            role="system",
            content="Esta conversa foi truncada devido ao tamanho. As mensagens mais antigas foram removidas."
        )
        
        truncated.messages.insert(0, system_msg)
        return truncated
    
    @staticmethod
    def summarize_conversation(conversation: Conversation) -> str:
        """
        Cria um resumo da conversa.
        
        Args:
            conversation: A conversa a ser resumida
            
        Returns:
            str: Um resumo textual da conversa
        """
        # Implementação simplificada - na prática, usaria LLM para resumir
        msg_count = len(conversation.messages)
        roles = set(msg.role for msg in conversation.messages)
        
        summary = f"Conversa com {msg_count} mensagens entre {', '.join(roles)}.\n"
        
        # Adiciona o título se disponível
        if conversation.title:
            summary += f"Título: {conversation.title}\n"
            
        # Adiciona as primeiras e últimas mensagens como contexto
        if msg_count > 0:
            summary += f"\nPrimeira mensagem: {conversation.messages[0].content[:100]}...\n"
            summary += f"Última mensagem: {conversation.messages[-1].content[:100]}...\n"
            
        return summary
    
    @staticmethod
    def split_conversation(conversation: Conversation, max_messages_per_part: int = 15) -> List[Conversation]:
        """
        Divide uma conversa longa em várias conversas menores.
        
        Args:
            conversation: A conversa a ser dividida
            max_messages_per_part: Número máximo de mensagens por parte
            
        Returns:
            List[Conversation]: Lista de conversas divididas
        """
        if len(conversation.messages) <= max_messages_per_part:
            return [conversation]
            
        parts = []
        total_parts = (len(conversation.messages) + max_messages_per_part - 1) // max_messages_per_part
        
        for i in range(total_parts):
            start_idx = i * max_messages_per_part
            end_idx = min((i + 1) * max_messages_per_part, len(conversation.messages))
            
            part = Conversation(
                id=f"{conversation.id}_part{i+1}",
                title=f"{conversation.title or 'Conversa'} (Parte {i+1}/{total_parts})",
                messages=conversation.messages[start_idx:end_idx],
                created_at=conversation.created_at,
                updated_at=conversation.updated_at
            )
            
            parts.append(part)
            
        return parts
    
    @staticmethod
    def get_conversation_stats(conversation: Conversation) -> Dict[str, Any]:
        """
        Obtém estatísticas sobre a conversa.
        
        Args:
            conversation: A conversa a ser analisada
            
        Returns:
            Dict[str, Any]: Estatísticas da conversa
        """
        message_count = len(conversation.messages)
        
        # Contagem de mensagens por role
        role_counts = {}
        for msg in conversation.messages:
            role_counts[msg.role] = role_counts.get(msg.role, 0) + 1
            
        # Comprimento médio das mensagens
        avg_message_length = sum(len(msg.content) for msg in conversation.messages) / max(1, message_count)
        
        return {
            "message_count": message_count,
            "role_distribution": role_counts,
            "average_message_length": avg_message_length,
            "token_count": conversation.token_count or "Não disponível",
            "is_too_long": ConversationManager.check_conversation_length(conversation)
        } 