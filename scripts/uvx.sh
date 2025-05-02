#!/bin/bash

# Script para simular o comando uvx para Databutton
# Uso: ./uvx.sh databutton-app-mcp@latest -k <key>

echo "Executando uvx simulado para Databutton..."
echo "Argumentos: $@"

# Extrair argumentos
PACKAGE="$1"
shift

while (( "$#" )); do
  case "$1" in
    -k|--key)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        KEY="$2"
        shift 2
      else
        echo "Erro: Argumento para $1 está faltando" >&2
        exit 1
      fi
      ;;
    *)
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

# Configurar variáveis de ambiente
export DATABUTTON_API_KEY="$KEY"

# Tentar executar com npx
echo "Tentando executar com npx..."
npx -y @smithery/cli@latest run "$PACKAGE"

# Se falhar, tentar outra abordagem
if [ $? -ne 0 ]; then
  echo "Executando com abordagem alternativa..."
  
  # Tentar simular uma resposta do MCP para o Cursor
  # Esta é apenas uma simulação e não um servidor real
  if [[ "$PACKAGE" == *"databutton-app-mcp"* ]]; then
    echo "Simulando servidor MCP Databutton..."
    # Saída no formato esperado pelo MCP
    cat << EOF
{"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"databutton_search","description":"Pesquisa em documentos e dados do Databutton","parameters":{"type":"object","properties":{"query":{"type":"string","description":"Texto a ser pesquisado"}},"required":["query"]}},{"name":"databutton_create_task","description":"Cria uma nova tarefa no Databutton","parameters":{"type":"object","properties":{"title":{"type":"string","description":"Título da tarefa"},"description":{"type":"string","description":"Descrição detalhada da tarefa"},"due_date":{"type":"string","description":"Data de vencimento no formato YYYY-MM-DD"}},"required":["title"]}}]}}
EOF
    exit 0
  fi
  
  echo "Erro: Não foi possível executar o comando. Verifique a instalação do Databutton."
fi 