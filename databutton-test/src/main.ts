import { CallToolRequest, CallToolResult, ListToolsResult, Content, ContentType, ToolDescription } from "./pdk";

// URL base do servidor FastAPI
const API_BASE_URL = "http://localhost:8000";

// Interface para o objeto Http que o Extism fornece
declare const Http: new () => {
  get(url: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
  post(url: string, body: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
};

/**
 * Implementa a chamada às ferramentas do servidor FastAPI
 */
export function callImpl(input: CallToolRequest): CallToolResult {
  const toolName = input.params.name;
  const args = input.params.arguments || {};
  
  try {
    // HTTP cliente simples do runtime do Extism
    const http = new Http();
    let response;
    
    switch (toolName) {
      case 'check_health':
        // Responder diretamente sem chamar o servidor local
        return {
          content: [
            {
              type: ContentType.Text,
              text: JSON.stringify({ status: "OK" })
            }
          ],
          isError: false
        };
        
      case 'mcp_list_tools':
        response = http.get(`${API_BASE_URL}/api/mcp/tools`);
        break;
        
      case 'mcp_query':
        response = http.post(
          `${API_BASE_URL}/api/mcp/query`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'mcp_query_stream':
        response = http.post(
          `${API_BASE_URL}/api/mcp/query/stream`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'mcp_run_login':
        response = http.post(
          `${API_BASE_URL}/api/mcp/auth/login`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'mcp_run_search_servlets':
        response = http.post(
          `${API_BASE_URL}/api/mcp/search/servlets`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'mcp_run_get_profiles':
        response = http.get(`${API_BASE_URL}/api/mcp/profiles`);
        break;
        
      case 'mcp_run_set_profile':
        response = http.post(
          `${API_BASE_URL}/api/mcp/profiles/set`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      // Novos casos para funções XTP
      case 'xtp_check_status':
        response = http.get(`${API_BASE_URL}/api/mcp/xtp/status`);
        break;
        
      case 'xtp_login':
        response = http.post(
          `${API_BASE_URL}/api/mcp/xtp/login`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'xtp_build_plugin':
        response = http.post(
          `${API_BASE_URL}/api/mcp/xtp/build`,
          JSON.stringify({}),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'xtp_deploy_plugin':
        response = http.post(
          `${API_BASE_URL}/api/mcp/xtp/deploy`,
          JSON.stringify(args),
          { 'Content-Type': 'application/json' }
        );
        break;
        
      case 'xtp_list_plugins':
        let pluginsUrl = `${API_BASE_URL}/api/mcp/xtp/plugins`;
        if (args.extension_point) {
          pluginsUrl += `?extension_point=${encodeURIComponent(args.extension_point)}`;
        }
        response = http.get(pluginsUrl);
        break;
        
      case 'xtp_get_plugin_info':
        if (!args.plugin_name) {
          return {
            content: [
              {
                type: ContentType.Text,
                text: JSON.stringify({ error: "Nome do plugin não fornecido" })
              }
            ],
            isError: true
          };
        }
        
        let pluginUrl = `${API_BASE_URL}/api/mcp/xtp/plugin/${encodeURIComponent(args.plugin_name)}`;
        if (args.extension_point) {
          pluginUrl += `?extension_point=${encodeURIComponent(args.extension_point)}`;
        }
        response = http.get(pluginUrl);
        break;
      
      default:
        return {
          content: [
            {
              type: ContentType.Text,
              text: JSON.stringify({ error: `Ferramenta desconhecida: ${toolName}` })
            }
          ],
          isError: true
        };
    }
    
    // Processar resposta da API
    if (response.status >= 400) {
      return {
        content: [
          {
            type: ContentType.Text,
            text: JSON.stringify({ 
              error: `Erro na chamada da API: ${response.status}`,
              body: textDecoder.decode(response.body)
            })
          }
        ],
        isError: true
      };
    }
    
    return {
      content: [
        {
          type: ContentType.Text,
          text: textDecoder.decode(response.body)
        }
      ],
      isError: false
    };
  } catch (error) {
    return {
      content: [
        {
          type: ContentType.Text,
          text: JSON.stringify({ error: String(error) })
        }
      ],
      isError: true
    };
  }
}

/**
 * Descreve as ferramentas disponíveis neste plugin
 */
export function describeImpl(): ListToolsResult {
  return {
    tools: [
      {
        name: "check_health",
        description: "Verifica a saúde do servidor FastAPI.",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "mcp_list_tools",
        description: "Lista todas as ferramentas disponíveis no servidor local.",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "mcp_query",
        description: "Consulta o servidor MCP.",
        inputSchema: {
          type: "object",
          properties: {
            query: { 
              type: "string",
              description: "Consulta a ser enviada ao servidor MCP"
            },
            context: { 
              type: "object",
              description: "Contexto adicional para a consulta"
            }
          }
        }
      },
      {
        name: "mcp_query_stream",
        description: "Consulta o servidor MCP com resposta em streaming.",
        inputSchema: {
          type: "object",
          properties: {
            query: { 
              type: "string",
              description: "Consulta a ser enviada ao servidor MCP em modo streaming"
            },
            context: { 
              type: "object",
              description: "Contexto adicional para a consulta streaming"
            }
          }
        }
      },
      {
        name: "mcp_run_login",
        description: "Função para login no MCP.run",
        inputSchema: {
          type: "object",
          properties: {
            token: { 
              type: "string",
              description: "Token de autenticação para o MCP.run"
            }
          }
        }
      },
      {
        name: "mcp_run_search_servlets",
        description: "Função para pesquisar servlets no MCP.run",
        inputSchema: {
          type: "object",
          properties: {
            q: { 
              type: "string",
              description: "Termo de pesquisa para encontrar servlets"
            }
          }
        }
      },
      {
        name: "mcp_run_get_profiles",
        description: "Função para obter perfis do usuário no MCP.run",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "mcp_run_set_profile",
        description: "Função para definir o perfil ativo no MCP.run",
        inputSchema: {
          type: "object",
          properties: {
            profile: { 
              type: "string",
              description: "Nome do perfil a ser ativado"
            }
          }
        }
      },
      // Novas ferramentas XTP
      {
        name: "xtp_check_status",
        description: "Verifica o status da instalação XTP.",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "xtp_login",
        description: "Faz login na plataforma XTP.",
        inputSchema: {
          type: "object",
          properties: {
            token: { 
              type: "string",
              description: "Token de autenticação para o XTP (opcional)"
            }
          }
        }
      },
      {
        name: "xtp_build_plugin",
        description: "Compila o plugin Databutton.",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "xtp_deploy_plugin",
        description: "Faz o deploy do plugin Databutton para o MCP.run.",
        inputSchema: {
          type: "object",
          properties: {
            token: { 
              type: "string",
              description: "Token XTP para autenticação (opcional)"
            },
            plugin_name: { 
              type: "string",
              description: "Nome do plugin (padrão: 'databutton')"
            },
            extension_point: { 
              type: "string",
              description: "ID do extension point (padrão: 'ext_01je4jj1tteaktf0zd0anm8854')"
            }
          }
        }
      },
      {
        name: "xtp_list_plugins",
        description: "Lista os plugins disponíveis do usuário.",
        inputSchema: {
          type: "object",
          properties: {
            extension_point: { 
              type: "string",
              description: "ID do extension point para filtrar (opcional)"
            }
          }
        }
      },
      {
        name: "xtp_get_plugin_info",
        description: "Obtém informações sobre um plugin específico.",
        inputSchema: {
          type: "object",
          properties: {
            plugin_name: { 
              type: "string",
              description: "Nome do plugin"
            },
            extension_point: { 
              type: "string",
              description: "ID do extension point (opcional)"
            }
          }
        }
      }
    ]
  };
}

// Decoder para converter ArrayBuffer para string
const textDecoder = new TextDecoder();

// Adicionando novas funções para trabalhar com os endpoints XTP (agora no namespace MCP)
/**
 * Verifica o status da instalação XTP
 */
export function xtp_check_status(): string {
  const http = new Http();
  const response = http.get(`${API_BASE_URL}/api/mcp/xtp/status`);
  
  if (response.status !== 200) {
    return JSON.stringify({
      status: 'error',
      message: `Erro ao verificar status XTP: ${response.status}`,
      data: response.body ? new TextDecoder().decode(response.body) : null
    });
  }
  
  return new TextDecoder().decode(response.body);
}

/**
 * Faz login na plataforma XTP
 */
export function xtp_login(input: string): string {
  const http = new Http();
  const payload = input ? JSON.parse(input) : {};
  
  const response = http.post(
    `${API_BASE_URL}/api/mcp/xtp/login`,
    JSON.stringify(payload),
    { 'Content-Type': 'application/json' }
  );
  
  return new TextDecoder().decode(response.body);
}

/**
 * Compila o plugin Databutton
 */
export function xtp_build_plugin(): string {
  const http = new Http();
  
  const response = http.post(
    `${API_BASE_URL}/api/mcp/xtp/build`,
    JSON.stringify({}),
    { 'Content-Type': 'application/json' }
  );
  
  return new TextDecoder().decode(response.body);
}

/**
 * Faz o deploy do plugin Databutton
 */
export function xtp_deploy_plugin(input: string): string {
  const http = new Http();
  const payload = input ? JSON.parse(input) : {};
  
  const response = http.post(
    `${API_BASE_URL}/api/mcp/xtp/deploy`,
    JSON.stringify(payload),
    { 'Content-Type': 'application/json' }
  );
  
  return new TextDecoder().decode(response.body);
}

/**
 * Lista os plugins disponíveis
 */
export function xtp_list_plugins(input: string): string {
  const http = new Http();
  const params = input ? JSON.parse(input) : {};
  
  let url = `${API_BASE_URL}/api/mcp/xtp/plugins`;
  if (params.extension_point) {
    url += `?extension_point=${encodeURIComponent(params.extension_point)}`;
  }
  
  const response = http.get(url);
  
  return new TextDecoder().decode(response.body);
}

/**
 * Obtém informações sobre um plugin específico
 */
export function xtp_get_plugin_info(input: string): string {
  const http = new Http();
  const params = JSON.parse(input);
  
  if (!params.plugin_name) {
    return JSON.stringify({
      status: 'error',
      message: 'Nome do plugin não fornecido'
    });
  }
  
  let url = `${API_BASE_URL}/api/mcp/xtp/plugin/${encodeURIComponent(params.plugin_name)}`;
  if (params.extension_point) {
    url += `?extension_point=${encodeURIComponent(params.extension_point)}`;
  }
  
  const response = http.get(url);
  
  return new TextDecoder().decode(response.body);
}
