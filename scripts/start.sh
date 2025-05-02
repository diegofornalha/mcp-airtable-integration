#!/bin/bash

# Função para verificar se um comando existe
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Função para verificar se um processo está rodando
process_running() {
  pgrep -f "$1" >/dev/null 2>&1
}

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica e inicia o servidor FastAPI se não estiver rodando
if ! process_running "python.*main.py"; then
  echo -e "${YELLOW}Servidor FastAPI não está rodando. Iniciando...${NC}"
  
  # Verifica se o diretório backend existe
  if [ -d "./backend" ]; then
    cd ./backend || exit 1
    
    # Verifica se o script run.sh existe
    if [ -f "./run.sh" ]; then
      chmod +x ./run.sh
      ./run.sh &
      echo -e "${GREEN}Servidor FastAPI iniciado em background${NC}"
    else
      echo -e "${RED}Erro: arquivo run.sh não encontrado em ./backend${NC}"
      exit 1
    fi
    
    cd ..
  else
    echo -e "${RED}Erro: diretório backend não encontrado${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}Servidor FastAPI já está rodando${NC}"
fi

# Verificar e instalar dependências Node.js
if [ -f "./install.sh" ]; then
  echo -e "${YELLOW}Verificando dependências...${NC}"
  chmod +x ./install.sh
  ./install.sh
  if [ $? -ne 0 ]; then
    echo -e "${RED}Erro: falha na verificação de dependências.${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}Aviso: arquivo install.sh não encontrado, pulando verificação de dependências.${NC}"
fi

# Compilar o plugin se não existir
if [ ! -f "./dist/plugin.js" ]; then
  echo -e "${YELLOW}Plugin não compilado. Compilando...${NC}"
  npm run build
  if [ $? -ne 0 ]; then
    echo -e "${RED}Erro: falha na compilação do plugin.${NC}"
    exit 1
  fi
fi

# Iniciar o servidor Node.js
echo -e "${YELLOW}Iniciando servidor Node.js...${NC}"
npm start

echo -e "${GREEN}Todos os serviços foram iniciados!${NC}" 