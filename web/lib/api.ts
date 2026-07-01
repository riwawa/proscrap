const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export interface Processo {
  id: string;
  numero_cnj: string;
  tribunal_alias: string;
  apelido: string | null;
  ativo: boolean;
  criado_em: string;
  ultima_consulta_em: string | null;
}

export interface Movimentacao {
  id: string;
  data_hora: string;
  codigo_movimento: number | null;
  nome_movimento: string;
  capturado_em: string;
}

export interface SincronizacaoResultado {
  status: "success" | "no_change" | "error";
  movimentacoes_novas: number;
  erro_detalhe: string | null;
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, options);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function listarProcessos(): Promise<Processo[]> {
  return apiFetch<Processo[]>("/processos");
}

export async function cadastrarProcesso(numeroCnj: string, apelido?: string): Promise<Processo> {
  return apiFetch<Processo>("/processos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ numero_cnj: numeroCnj, apelido }),
  });
}

export async function listarMovimentacoes(processoId: string): Promise<Movimentacao[]> {
  return apiFetch<Movimentacao[]>(`/processos/${processoId}/movimentacoes`);
}

export async function sincronizarProcesso(processoId: string): Promise<SincronizacaoResultado> {
  return apiFetch<SincronizacaoResultado>(`/processos/${processoId}/sincronizar`, {
    method: "POST",
  });
}

export async function removerProcesso(processoId: string): Promise<void> {
  await apiFetch<void>(`/processos/${processoId}`, { method: "DELETE" });
}