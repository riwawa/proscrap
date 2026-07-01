"use client";

import { useEffect, useState } from "react";
import { listarMovimentacoes, type Processo, type Movimentacao } from "@/lib/api";

interface Props {
  processo: Processo;
  onFechar: () => void;
}

export function TimelineModal({ processo, onFechar }: Props) {
  const [movimentacoes, setMovimentacoes] = useState<Movimentacao[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function carregar() {
      try {
        const data = await listarMovimentacoes(processo.id);
        setMovimentacoes(data);
      } catch {
        setErro("Não foi possível carregar as movimentações.");
      } finally {
        setLoading(false);
      }
    }
    carregar();
  }, [processo.id]);

  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === "Escape") onFechar();
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onFechar]);

  function formatarDataHora(raw: string) {
    return new Date(raw).toLocaleString("pt-BR", {
      day: "2-digit", month: "2-digit", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  }

  return (
    <div
      className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onFechar(); }}
    >
      <div className="bg-white rounded-xl border border-gray-200 w-full max-w-xl max-h-[80vh] flex flex-col shadow-xl">
        <div className="px-5 py-4 border-b border-gray-100 flex items-start justify-between gap-4">
          <div className="min-w-0">
            {processo.apelido && (
              <p className="text-sm font-semibold text-gray-800 truncate">{processo.apelido}</p>
            )}
            <p className="text-xs font-mono text-gray-400 truncate">{processo.numero_cnj}</p>
            <p className="text-xs text-gray-400 uppercase tracking-wide mt-0.5">{processo.tribunal_alias}</p>
          </div>
          <button onClick={onFechar} className="text-gray-400 hover:text-gray-600 transition-colors text-xl leading-none shrink-0" aria-label="Fechar">×</button>
        </div>

        <div className="overflow-y-auto flex-1 px-5 py-4">
          {loading && <p className="text-sm text-gray-400 text-center py-8">Carregando movimentações...</p>}
          {erro && <p className="text-sm text-red-500 text-center py-8">{erro}</p>}
          {!loading && !erro && movimentacoes.length === 0 && (
            <p className="text-sm text-gray-400 text-center py-8">Nenhuma movimentação registrada.</p>
          )}
          {!loading && !erro && movimentacoes.length > 0 && (
            <div>
              <p className="text-xs text-gray-400 mb-4">
                {movimentacoes.length} movimentação{movimentacoes.length !== 1 ? "ões" : ""} — mais recente primeiro
              </p>
              {movimentacoes.map((mov, idx) => (
                <div key={mov.id} className="flex gap-3">
                  <div className="flex flex-col items-center">
                    <div className="w-2 h-2 rounded-full bg-blue-400 mt-1 shrink-0" />
                    {idx < movimentacoes.length - 1 && (
                      <div className="w-px flex-1 bg-gray-100 mt-1" />
                    )}
                  </div>
                  <div className="pb-4 min-w-0 flex-1">
                    <p className="text-sm font-medium text-gray-800 leading-tight">{mov.nome_movimento}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {formatarDataHora(mov.data_hora)}
                      {mov.codigo_movimento && (
                        <span className="font-mono ml-2 text-gray-300">#{mov.codigo_movimento}</span>
                      )}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}