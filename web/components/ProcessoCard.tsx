"use client";

import { useState } from "react";
import { type Processo, sincronizarProcesso, removerProcesso } from "@/lib/api";

interface Props {
  processo: Processo;
  onVerTimeline: () => void;
  onSincronizado: () => void;
  onRemovido: () => void;
}

export function ProcessoCard({ processo, onVerTimeline, onSincronizado, onRemovido }: Props) {
  const [sincronizando, setSincronizando] = useState(false);
  const [removendo, setRemovendo] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [confirmarRemover, setConfirmarRemover] = useState(false);

  async function handleSincronizar() {
    setSincronizando(true);
    setFeedback(null);
    try {
      const resultado = await sincronizarProcesso(processo.id);
      if (resultado.status === "no_change") {
        setFeedback("Sem novidades");
      } else {
        setFeedback(`${resultado.movimentacoes_novas} nova(s)`);
        onSincronizado();
      }
    } catch {
      setFeedback("Erro");
    } finally {
      setSincronizando(false);
      setTimeout(() => setFeedback(null), 3000);
    }
  }

  async function handleRemover() {
    setRemovendo(true);
    try {
      await removerProcesso(processo.id);
      onRemovido();
    } catch {
      setFeedback("Erro ao remover");
      setRemovendo(false);
      setConfirmarRemover(false);
    }
  }

  const ultimaConsulta = processo.ultima_consulta_em
    ? new Date(processo.ultima_consulta_em).toLocaleString("pt-BR", {
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit",
      })
    : "Nunca consultado";

  return (
    <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 flex items-center justify-between gap-4 hover:border-gray-300 transition-colors">
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 flex-wrap">
          {processo.apelido && (
            <span className="text-sm font-medium text-gray-800 truncate">{processo.apelido}</span>
          )}
          <span className="text-xs font-mono text-gray-400 truncate">{processo.numero_cnj}</span>
          <span className="text-xs bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded uppercase tracking-wide shrink-0">{processo.tribunal_alias}</span>
        </div>
        <p className="text-xs text-gray-400 mt-0.5">Última consulta: {ultimaConsulta}</p>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        {feedback && <span className="text-xs text-gray-400">{feedback}</span>}

        {confirmarRemover ? (
          <>
            <span className="text-xs text-gray-500">Remover?</span>
            <button
              onClick={handleRemover}
              disabled={removendo}
              className="text-xs text-red-500 hover:text-red-700 px-2 py-1 rounded hover:bg-red-50 transition-colors disabled:opacity-40"
            >
              {removendo ? "Removendo..." : "Confirmar"}
            </button>
            <button
              onClick={() => setConfirmarRemover(false)}
              className="text-xs text-gray-400 hover:text-gray-600 px-2 py-1 rounded hover:bg-gray-100 transition-colors"
            >
              Cancelar
            </button>
          </>
        ) : (
          <>
            <button
              onClick={handleSincronizar}
              disabled={sincronizando}
              className="text-xs text-gray-400 hover:text-gray-700 px-2 py-1 rounded hover:bg-gray-100 transition-colors disabled:opacity-40"
            >
              {sincronizando ? "Consultando..." : "Sincronizar"}
            </button>
            <button
              onClick={onVerTimeline}
              className="text-xs bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700 transition-colors font-medium"
            >
              Ver movimentações
            </button>
            <button
              onClick={() => setConfirmarRemover(true)}
              className="text-xs text-gray-300 hover:text-red-400 px-2 py-1 rounded hover:bg-red-50 transition-colors"
            >
              ×
            </button>
          </>
        )}
      </div>
    </div>
  );
}