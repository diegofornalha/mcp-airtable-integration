#!/usr/bin/env node

/**
 * Script para testar a criação de tarefas no Airtable usando o MCP diretamente.
 */

const { execSync } = require('child_process');

// Configuração do Airtable
const base_id = "appt2CRa7k9cUASRJ";
const table_id = "tblUatmXxgQnqEUDB";

// Dados da tarefa
const taskData = {
  Nome: "Tarefa de teste via NPX",
  Descrição: "Esta tarefa foi criada diretamente pelo NPX",
  Status: "Pendente",
  "Data de Vencimento": new Date().toISOString().split('T')[0],
  Prioridade: "Média"
};

// Comando para criar a tarefa
const apiKey = "patniDQMmniKrjPoy.d81e30b3f466457908966ef8bcd5bfc96ac0c40bf5267ef423376e149ec28450";
const command = `npx -y @smithery/cli@latest run airtable-server --config '{"airtableApiKey":"${apiKey}"}' -- create_record --parameters '{"base_id":"${base_id}","table_id":"${table_id}","fields":${JSON.stringify(taskData)}}'`;

console.log("Criando tarefa no Airtable...");
console.log(`Base: ${base_id}, Tabela: ${table_id}`);
console.log(`Dados: ${JSON.stringify(taskData, null, 2)}`);

try {
  const output = execSync(command, { encoding: 'utf8' });
  console.log("Resultado:");
  console.log(output);
  console.log("Tarefa criada com sucesso!");
} catch (error) {
  console.error("Erro ao criar tarefa:");
  console.error(error.message);
  
  if (error.stdout) {
    console.log("Saída padrão:");
    console.log(error.stdout);
  }
  
  if (error.stderr) {
    console.log("Saída de erro:");
    console.log(error.stderr);
  }
}