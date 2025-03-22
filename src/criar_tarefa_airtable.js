#!/usr/bin/env node

/**
 * Script para criar uma tarefa no Airtable usando o MCP
 * 
 * Uso: node criar_tarefa_airtable.js "Nome da tarefa" "Descrição opcional"
 */

const axios = require('axios');
const { execSync } = require('child_process');

// Configuração
const config = {
  baseId: "appt2CRa7k9cUASRJ",
  tableName: "Tasks",
  apiKey: "patniDQMmniKrjPoy.d81e30b3f466457908966ef8bcd5bfc96ac0c40bf5267ef423376e149ec28450",
  airtableApiUrl: "https://api.airtable.com/v0"
};

/**
 * Cria uma tarefa no Airtable
 * @param {string} taskName - Nome da tarefa
 * @param {string} description - Descrição da tarefa (opcional)
 * @param {string} deadline - Data de vencimento (opcional, formato YYYY-MM-DD)
 * @param {string} status - Status da tarefa (opcional, padrão: "Not started")
 */
async function criarTarefa(taskName, description = null, deadline = null, status = "Not started") {
  if (!taskName) {
    console.error("Erro: Nome da tarefa é obrigatório");
    process.exit(1);
  }

  // Configura dados da tarefa
  const taskData = {
    records: [
      {
        fields: {
          Task: taskName,
          Status: status
        }
      }
    ],
    typecast: true
  };

  // Adiciona campos opcionais se fornecidos
  if (description) {
    taskData.records[0].fields.Notes = description;
  }

  if (deadline) {
    taskData.records[0].fields.Deadline = deadline;
  } else {
    // Usa a data atual como padrão
    taskData.records[0].fields.Deadline = new Date().toISOString().split('T')[0];
  }

  try {
    console.log(`Criando tarefa: ${taskName}`);
    console.log("Dados:", JSON.stringify(taskData, null, 2));

    // Faz a requisição para a API do Airtable
    const response = await axios({
      method: 'post',
      url: `${config.airtableApiUrl}/${config.baseId}/${config.tableName}`,
      headers: {
        'Authorization': `Bearer ${config.apiKey}`,
        'Content-Type': 'application/json'
      },
      data: taskData
    });

    // Mostra resultado
    console.log("\n✅ Tarefa criada com sucesso!");
    console.log(`ID: ${response.data.records[0].id}`);
    console.log(`Criada em: ${response.data.records[0].createdTime}`);
    console.log(`Campos: ${JSON.stringify(response.data.records[0].fields, null, 2)}`);

    return response.data;
  } catch (error) {
    console.error("\n❌ Erro ao criar tarefa:");
    
    if (error.response) {
      console.error(`Status: ${error.response.status}`);
      console.error(`Mensagem: ${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      console.error(error.message);
    }
    
    process.exit(1);
  }
}

// Função principal
(async () => {
  try {
    // Obtém argumentos da linha de comando
    const taskName = process.argv[2];
    const description = process.argv[3] || `Tarefa criada via script JS: ${taskName}`;
    const deadline = process.argv[4] || null;
    const status = process.argv[5] || "Not started";

    // Cria a tarefa
    await criarTarefa(taskName, description, deadline, status);
  } catch (error) {
    console.error("Erro não tratado:", error);
    process.exit(1);
  }
})();