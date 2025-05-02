#!/bin/bash

# Cores para mensagens
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para imprimir mensagens
print_message() {
    echo -e "${2}${1}${NC}"
}

# Obter o diretório do script atual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"
print_message "Diretório de trabalho: $(pwd)" "$GREEN"

# Verifica se o arquivo main.py existe
if [ ! -f "main.py" ]; then
    print_message "Arquivo main.py não encontrado no diretório atual!" "$RED"
    print_message "Procurando main.py em outros diretórios..." "$YELLOW"
    
    if [ -f "/Users/agents/Desktop/mcp-cli/backend/main.py" ]; then
        cd "/Users/agents/Desktop/mcp-cli/backend"
        print_message "Encontrado em /Users/agents/Desktop/mcp-cli/backend/main.py" "$GREEN"
        print_message "Mudando para o diretório: /Users/agents/Desktop/mcp-cli/backend" "$GREEN"
    else
        print_message "Arquivo main.py não encontrado! Verifique se ele existe e está no lugar correto." "$RED"
        exit 1
    fi
fi

# Determina qual comando Python usar
PYTHON_CMD="python"
if ! command -v python &> /dev/null; then
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_message "Usando comando 'python3'" "$GREEN"
    else
        print_message "Python não encontrado. Instale o Python 3.8 ou superior." "$RED"
        exit 1
    fi
fi

# Verifica a versão do Python
python_version=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_message "Versão do Python: $python_version" "$GREEN"

# Define o caminho do ambiente virtual
VENV_DIR="../.venv"

# Verifica e ativa o ambiente virtual
venv_activated=0
if [ -f "../.venv/bin/activate" ]; then
    source "../.venv/bin/activate"
    VENV_DIR="../.venv"
    venv_activated=1
    print_message "Ambiente virtual ../.venv ativado" "$GREEN"
elif [ -f "../venv/bin/activate" ]; then
    source "../venv/bin/activate"
    VENV_DIR="../venv"
    venv_activated=1
    print_message "Ambiente virtual ../venv ativado" "$GREEN"
elif [ -f "/Users/agents/Desktop/mcp-cli/venv/bin/activate" ]; then
    source "/Users/agents/Desktop/mcp-cli/venv/bin/activate"
    VENV_DIR="/Users/agents/Desktop/mcp-cli/venv"
    venv_activated=1
    print_message "Ambiente virtual /Users/agents/Desktop/mcp-cli/venv ativado" "$GREEN"
elif [ -f "/Users/agents/Desktop/mcp-cli/.venv/bin/activate" ]; then
    source "/Users/agents/Desktop/mcp-cli/.venv/bin/activate"
    VENV_DIR="/Users/agents/Desktop/mcp-cli/.venv"
    venv_activated=1
    print_message "Ambiente virtual /Users/agents/Desktop/mcp-cli/.venv ativado" "$GREEN"
else
    print_message "Ambiente virtual não encontrado. Criando um novo ambiente virtual..." "$YELLOW"
    
    # Cria o ambiente virtual
    $PYTHON_CMD -m venv $VENV_DIR || {
        print_message "Falha ao criar ambiente virtual. Verifique se o módulo venv está instalado." "$RED"
        print_message "Tente instalar com: brew install python-venv" "$YELLOW"
        exit 1
    }
    
    # Ativa o ambiente virtual
    source "$VENV_DIR/bin/activate" || {
        print_message "Falha ao ativar o ambiente virtual." "$RED"
        exit 1
    }
    
    venv_activated=1
    print_message "Novo ambiente virtual criado e ativado em $VENV_DIR" "$GREEN"
fi

# Verifica se o pip está disponível
PIP_CMD="pip"
if ! command -v pip &> /dev/null; then
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        print_message "Usando comando 'pip3'" "$GREEN"
    else
        print_message "pip não encontrado no ambiente virtual. Instalando pip..." "$YELLOW"
        $PYTHON_CMD -m ensurepip --upgrade || {
            print_message "Falha ao instalar pip. Verifique sua instalação do Python." "$RED"
            exit 1
        }
        PIP_CMD="$PYTHON_CMD -m pip"
    fi
fi

# Instala dependências se necessário
print_message "Verificando dependências..." "$GREEN"

# Verifica se fastapi e uvicorn estão instalados
if ! $PYTHON_CMD -c "import fastapi" &> /dev/null || ! $PYTHON_CMD -c "import uvicorn" &> /dev/null; then
    print_message "Dependências básicas faltando. Instalando..." "$YELLOW"
    if [ -f "requirements-essencial.txt" ]; then
        $PIP_CMD install -r requirements-essencial.txt
    else
        $PIP_CMD install fastapi uvicorn[standard]
    fi
fi

# Tenta instalar fastapi-mcp se não estiver presente
if ! $PYTHON_CMD -c "import fastapi_mcp" &> /dev/null; then
    print_message "Tentando instalar fastapi-mcp..." "$YELLOW"
    $PIP_CMD install fastapi-mcp || {
        print_message "Aviso: Não foi possível instalar fastapi-mcp. O servidor continuará sem ele." "$YELLOW"
        print_message "Talvez seja necessário instalar manualmente com: pip install git+https://github.com/tadata-org/fastapi_mcp.git" "$YELLOW"
        
        # Tenta clonar e instalar do repositório Git se pip falhar
        if command -v git &> /dev/null; then
            print_message "Tentando instalar fastapi-mcp do repositório Git..." "$YELLOW"
            TMP_DIR=$(mktemp -d)
            git clone https://github.com/tadata-org/fastapi_mcp.git "$TMP_DIR" && \
            cd "$TMP_DIR" && \
            $PIP_CMD install . && \
            cd "$SCRIPT_DIR" && \
            print_message "fastapi-mcp instalado com sucesso do GitHub!" "$GREEN" || \
            print_message "Falha ao instalar fastapi-mcp do GitHub. O servidor continuará sem ele." "$YELLOW"
            rm -rf "$TMP_DIR"
        fi
    }
fi

# Verifica se as dependências básicas foram instaladas
if ! $PYTHON_CMD -c "import fastapi, uvicorn" &> /dev/null; then
    print_message "Falha ao instalar dependências básicas. Verifique os erros acima." "$RED"
    exit 1
else
    print_message "Dependências básicas instaladas com sucesso!" "$GREEN"
fi

# Função para verificar se a porta está disponível
port_available() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 1
    else
        return 0
    fi
}

# Tenta usar a porta 8000 primeiro (mesma usada no main.py)
PORT=8000
if ! port_available $PORT; then
    print_message "Porta $PORT em uso, tentando porta 9000..." "$YELLOW"
    PORT=9000
    if ! port_available $PORT; then
        print_message "Porta $PORT em uso, tentando porta 9001..." "$YELLOW"
        PORT=9001
        if ! port_available $PORT; then
            print_message "Porta $PORT em uso, tentando porta 9002..." "$YELLOW"
            PORT=9002
            if ! port_available $PORT; then
                print_message "Todas as portas tentadas estão em uso. Por favor, encerre algum processo ou especifique outra porta." "$RED"
                exit 1
            fi
        fi
    fi
fi

print_message "Iniciando servidor FastAPI+MCP na porta $PORT..." "$GREEN"
print_message "API estará disponível em: http://127.0.0.1:$PORT" "$GREEN"
print_message "Swagger UI: http://127.0.0.1:$PORT/docs" "$GREEN"
print_message "MCP API: http://127.0.0.1:$PORT/mcp-api" "$GREEN"
print_message "Para encerrar, pressione CTRL+C" "$YELLOW"

print_message "Comando: uvicorn main:app --host 127.0.0.1 --port $PORT --reload" "$GREEN"
uvicorn main:app --host 127.0.0.1 --port $PORT --reload 
