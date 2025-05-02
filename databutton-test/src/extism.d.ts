declare module '@extism/extism' {
  export class Http {
    constructor();
    
    /**
     * Executa uma requisição GET
     * @param url URL a ser requisitada
     * @param headers Cabeçalhos opcionais
     */
    get(url: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
    
    /**
     * Executa uma requisição POST
     * @param url URL a ser requisitada
     * @param body Corpo da requisição
     * @param headers Cabeçalhos opcionais
     */
    post(url: string, body: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
  }
}

// Definição global do Http
declare global {
  const Http: new () => {
    get(url: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
    post(url: string, body: string, headers?: Record<string, string>): { status: number; body: ArrayBuffer };
  };
}

// Funções exportadas do plugin
export function check_health(): string;
export function mcp_list_tools(): string;
export function mcp_query(input: string): string;
export function mcp_query_stream(input: string): string;
export function mcp_run_login(input: string): string;
export function mcp_run_search_servlets(input: string): string;
export function mcp_run_get_profiles(input: string): string;
export function mcp_run_set_profile(input: string): string;

// Novas funções para gerenciamento de conversas
export function mcp_check_conversation_length(input: string): string;
export function mcp_perform_conversation_action(input: string): string;
export function mcp_list_conversations(input: string): string; 