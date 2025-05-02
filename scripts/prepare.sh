#!/bin/bash

echo "Preparando ambiente para compilação do plugin..."

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "Erro: Node.js não está instalado. Por favor, instale o Node.js."
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "Erro: npm não está instalado. Por favor, instale o npm."
    exit 1
fi

# Instalar dependências
echo "Instalando dependências..."
npm install typescript@latest --save-dev
npm install

echo "Ambiente preparado com sucesso!"
exit 0 