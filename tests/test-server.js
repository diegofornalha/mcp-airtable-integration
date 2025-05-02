// Servidor Express simples para testar as novas funcionalidades de gerenciamento de conversas
import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3001;
const API_BASE_URL = 'http://localhost:8000';

// Verificar o tamanho da conversa
app.post('/api/conversation/check', async (req, res) => {
  try {
    const response = await fetch(`${API_BASE_URL}/mcp/conversation/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Erro ao verificar tamanho da conversa:', error);
    res.status(500).json({ 
      status: 'error', 
      message: `Erro ao verificar tamanho da conversa: ${error.message}` 
    });
  }
});

// Executar ação na conversa
app.post('/api/conversation/action', async (req, res) => {
  try {
    const response = await fetch(`${API_BASE_URL}/mcp/conversation/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Erro ao executar ação na conversa:', error);
    res.status(500).json({ 
      status: 'error', 
      message: `Erro ao executar ação na conversa: ${error.message}` 
    });
  }
});

// Listar conversas
app.get('/api/conversation/list', async (req, res) => {
  try {
    const response = await fetch(`${API_BASE_URL}/mcp/conversation/list`);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Erro ao listar conversas:', error);
    res.status(500).json({ 
      status: 'error', 
      message: `Erro ao listar conversas: ${error.message}` 
    });
  }
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`Servidor de teste rodando na porta ${PORT}`);
}); 