// Teste das funções de gerenciamento de conversas
// Importação correta do node-fetch para versões mais recentes
import fetch from 'node-fetch';

// URL base do servidor de teste
const API_BASE_URL = 'http://localhost:3001';

/**
 * Função para verificar o tamanho de uma conversa
 */
async function testCheckConversationLength() {
  console.log('\n--- Teste: Verificar Tamanho da Conversa ---');
  try {
    // Cria uma conversa de exemplo com várias mensagens
    const messages = [];
    for (let i = 1; i <= 35; i++) {
      messages.push({
        role: i % 2 === 0 ? 'assistant' : 'user',
        content: `Esta é a mensagem de exemplo número ${i} para testar o limite de tamanho da conversa no MCP. Vamos adicionar algum conteúdo para aumentar o tamanho.`,
        timestamp: new Date().toISOString()
      });
    }

    const payload = {
      id: 'conv_test_1',
      messages: messages,
      title: 'Conversa de teste para verificação de tamanho'
    };

    const response = await fetch(`${API_BASE_URL}/api/conversation/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    console.log('Resultado da verificação de tamanho:');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Erro ao verificar tamanho da conversa:', error);
  }
}

/**
 * Função para testar as ações em conversas
 */
async function testConversationActions() {
  console.log('\n--- Teste: Ações na Conversa ---');
  try {
    // Testar ação de truncar
    console.log('\n> Ação: Truncar conversa');
    let payload = {
      conversation_id: 'conv_test_1',
      action: 'truncate',
      params: {
        keep_latest: 10
      }
    };

    let response = await fetch(`${API_BASE_URL}/api/conversation/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    let result = await response.json();
    console.log('Resultado da ação truncar:');
    console.log(JSON.stringify(result, null, 2));

    // Testar ação de resumir
    console.log('\n> Ação: Resumir conversa');
    payload = {
      conversation_id: 'conv_test_1',
      action: 'summarize'
    };

    response = await fetch(`${API_BASE_URL}/api/conversation/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    result = await response.json();
    console.log('Resultado da ação resumir:');
    console.log(JSON.stringify(result, null, 2));

    // Testar ação de dividir
    console.log('\n> Ação: Dividir conversa');
    payload = {
      conversation_id: 'conv_test_1',
      action: 'split',
      params: {
        max_messages_per_part: 10
      }
    };

    response = await fetch(`${API_BASE_URL}/api/conversation/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    result = await response.json();
    console.log('Resultado da ação dividir:');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Erro ao executar ações na conversa:', error);
  }
}

/**
 * Função para listar conversas
 */
async function testListConversations() {
  console.log('\n--- Teste: Listar Conversas ---');
  try {
    const response = await fetch(`${API_BASE_URL}/api/conversation/list`);
    const result = await response.json();
    console.log('Lista de conversas:');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Erro ao listar conversas:', error);
  }
}

// Executar os testes
async function runTests() {
  console.log('=== Teste do Gerenciador de Conversas MCP ===');
  
  await testCheckConversationLength();
  await testConversationActions();
  await testListConversations();
  
  console.log('\n=== Testes concluídos ===');
}

// Executar todos os testes
runTests(); 