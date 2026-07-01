"use client";

import { useEffect, useState } from "react";
import { listarProcessos, cadastrarProcesso, type Processo } from "@/lib/api";
import { ProcessoCard } from "@/components/ProcessoCard";
import { NovoProcessoForm } from "@/components/NovoProcessoForm";
import { TimelineModal } from "@/components/TimelineModal";

export default function Home() {
  const [processos, setProcessos] = useState<Processo[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [processoSelecionado, setProcessoSelecionado] = useState<Processo | null>(null);

  async function carregar() {
    try {
      setErro(null);
      const data = await listarProcessos();
      setProcessos(data);
    } catch {
      setErro("Não foi possível conectar ao backend. Verifique se o servidor está rodando.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { carregar(); }, []);

  async function handleCadastrar(numeroCnj: string, apelido?: string) {
    await cadastrarProcesso(numeroCnj, apelido);
    await carregar();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-sm font-semibold text-gray-900 tracking-tight">PROSCRAP</h1>
            <p className="text-xs text-gray-400 mt-0.5">Acompanhamento processual via API Pública CNJ</p>
          </div>
          <span className="text-xs font-mono text-gray-400 bg-gray-100 px-2 py-1 rounded">v1</span>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-8 space-y-6">
        <NovoProcessoForm onCadastrar={handleCadastrar} />

        <section>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Processos monitorados</h2>
            <span className="text-xs text-gray-400 font-mono">{processos.length} processo{processos.length !== 1 ? "s" : ""}</span>
          </div>

          {loading && <p className="text-sm text-gray-400 text-center py-10">Carregando...</p>}

          {erro && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">{erro}</p>
          )}

          {!loading && !erro && processos.length === 0 && (
            <div className="text-sm text-gray-400 py-10 text-center border border-dashed border-gray-200 rounded-lg">
              Nenhum processo cadastrado. Adicione um número CNJ acima.
            </div>
          )}

          {!loading && !erro && processos.length > 0 && (
            <div className="space-y-2">
              {processos.map((p) => (
                <ProcessoCard
                key={p.id}
                processo={p}
                onVerTimeline={() => setProcessoSelecionado(p)}
                onSincronizado={carregar}
                onRemovido={carregar}
                />
              ))}
            </div>
          )}
        </section>
      </main>

      {processoSelecionado && (
        <TimelineModal processo={processoSelecionado} onFechar={() => setProcessoSelecionado(null)} />
      )}
    </div>
  );
}