#!/usr/bin/env python3
"""
Script para testar as funcionalidades do gerenciador de conversas.
"""

import sys
import os
from app.apis.mcp.conversation_manager import Message, Conversation, ConversationManager

def test_check_conversation_length():
    """Testa a verificação de tamanho de conversas."""
    print("\n=== Teste: Verificação de Tamanho da Conversa ===")
    
    # Cria uma conversa de teste com 35 mensagens
    messages = []
    for i in range(1, 36):
        messages.append(Message(
            role="user" if i % 2 else "assistant",
            content=f"Esta é a mensagem de exemplo {i} para testar o limite de tamanho da conversa."
        ))
    
    conversation = Conversation(
        id="conv_test_1",
        messages=messages,
        title="Conversa de teste"
    )
    
    # Verifica se a conversa está muito longa
    is_too_long = ConversationManager.check_conversation_length(conversation)
    stats = ConversationManager.get_conversation_stats(conversation)
    
    print(f"Conversa muito longa? {is_too_long}")
    print(f"Estatísticas da conversa: {stats}")
    
    return conversation

def test_truncate_conversation(conversation):
    """Testa a truncagem de conversas."""
    print("\n=== Teste: Truncagem de Conversa ===")
    
    # Trunca a conversa mantendo apenas as 10 mensagens mais recentes
    truncated = ConversationManager.truncate_conversation(conversation, keep_latest=10)
    
    print(f"Mensagens originais: {len(conversation.messages)}")
    print(f"Mensagens após truncagem: {len(truncated.messages)}")
    print(f"Primeira mensagem (sistema): {truncated.messages[0].content}")
    
    return truncated

def test_summarize_conversation(conversation):
    """Testa o resumo de conversas."""
    print("\n=== Teste: Resumo de Conversa ===")
    
    # Cria um resumo da conversa
    summary = ConversationManager.summarize_conversation(conversation)
    
    print("Resumo da conversa:")
    print(summary)

def test_split_conversation(conversation):
    """Testa a divisão de conversas."""
    print("\n=== Teste: Divisão de Conversa ===")
    
    # Divide a conversa em partes de 10 mensagens cada
    parts = ConversationManager.split_conversation(conversation, max_messages_per_part=10)
    
    print(f"Conversa dividida em {len(parts)} partes:")
    for i, part in enumerate(parts):
        print(f"Parte {i+1}: {len(part.messages)} mensagens, título: {part.title}")

def main():
    """Função principal."""
    print("Iniciando testes do gerenciador de conversas...\n")
    
    # Testa a verificação de tamanho
    conversation = test_check_conversation_length()
    
    # Testa a truncagem
    truncated_conversation = test_truncate_conversation(conversation)
    
    # Testa o resumo
    test_summarize_conversation(conversation)
    
    # Testa a divisão
    test_split_conversation(conversation)
    
    print("\nTestes concluídos com sucesso!")

if __name__ == "__main__":
    # Adiciona o diretório atual ao path para importações relativas
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main() 