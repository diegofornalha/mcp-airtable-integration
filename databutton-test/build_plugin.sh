#!/bin/bash

# Verificar e instalar dependências
if [ -f "./install.sh" ]; then
  echo "Verificando dependências..."
  chmod +x ./install.sh
  ./install.sh
  if [ $? -ne 0 ]; then
    echo "Erro: falha na verificação de dependências."
    exit 1
  fi
else
  echo "Aviso: arquivo install.sh não encontrado, pulando verificação de dependências."
fi

# Configurar token XTP
export XTP_TOKEN=xtp0_AZY3SLzIcRi_TKCKJ7oaVgj1sFE4CmYGUhLzp3kFdTvrZ97sQEaAPw
echo "Token XTP configurado"

# Configurar guest key
export XTP_GUEST_KEY="replace-me-ce20c9db-4b8b-4e1d-9131-91275d4fd34b"
echo "Guest Key configurada"

# Compilar TypeScript
echo "Compilando TypeScript..."
mkdir -p dist
npx tsc 

# Verificar se a compilação foi bem-sucedida
if [ ! -f "dist/main.js" ]; then
  echo "Erro: compilação do TypeScript falhou. Verifique os erros acima."
  exit 1
fi

# Copiar o arquivo compilado
cp dist/main.js dist/plugin.js
echo "Arquivo plugin.js criado em dist/"

# Compilar o plugin com extism-js se disponível
if command -v extism-js >/dev/null 2>&1; then
  echo "Compilando plugin com extism-js..."
  extism-js package dist/main.js -o dist/plugin.wasm
  if [ -f "dist/plugin.wasm" ]; then
    echo "Plugin WebAssembly gerado com sucesso: dist/plugin.wasm"
  else
    echo "Aviso: falha ao gerar plugin WebAssembly."
  fi
else
  echo "Aviso: extism-js não encontrado, pulando geração de plugin WebAssembly."
fi

# Publicar o plugin
echo "Publicando plugin com XTP..."
xtp plugin push -f 

echo "Verificando se o plugin foi publicado..."
xtp plugin list | grep xfxacademy

echo "Processo concluído!" 