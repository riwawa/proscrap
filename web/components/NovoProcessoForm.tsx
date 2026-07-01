"use client";

import { useState } from "react";

interface Props {
  onCadastrar: (numeroCnj: string, apelido?: string) => Promise<void>;
}

export function NovoProcessoForm({ onCadastrar }: Props) {
  const [numeroCnj, setNumeroCnj] = useState("");
  const [apelido, setApelido] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [aberto, setAberto] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!numeroCnj.trim()) return;
    setLoading(true);
    setErro(null);
    try {
      await onCadastrar(numeroCnj.trim(), apelido.trim() || undefined);
      setNumeroCnj("");
      setApelido("");
      setAberto(false);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Erro ao cadastrar processo.";
      try {
        const json = JSON.parse(message);
        setErro(json.detail ?? message);
      } catch {
        setErro(message);
      }
    } finally {
      setLoading(false);
    }
  }

  if (!aberto) {
    return (
      <button
        onClick={() => setAberto(true)}
        className="w-full border border-dashed border-gray-300 rounded-lg py-3 text-sm text-gray-400 hover:border-blue-400 hover:text-blue-500 transition-colors"
      >
        + Adicionar processo
      </button>
    );
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white">
      <h2 className="text-sm font-semibold text-gray-800 mb-3">Adicionar processo</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="text-xs text-gray-500 block mb-1">Número CNJ <span className="text-red-500">*</span></label>
          <input
            type="text"
            value={numeroCnj}
            onChange={(e) => setNumeroCnj(e.target.value)}
            placeholder="0000000-00.0000.0.00.0000"
            className="w-full text-sm font-mono border border-gray-200 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400 transition-colors"
            required
          />
        </div>
        <div>
          <label className="text-xs text-gray-500 block mb-1">Apelido (opcional)</label>
          <input
            type="text"
            value={apelido}
            onChange={(e) => setApelido(e.target.value)}
            placeholder="Ex: Ação de cobrança cliente X"
            className="w-full text-sm border border-gray-200 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400 transition-colors"
          />
        </div>
        {erro && <p className="text-xs text-red-500">{erro}</p>}
        <div className="flex gap-2 pt-1">
          <button type="submit" disabled={loading} className="text-sm bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors font-medium disabled:opacity-40">
            {loading ? "Cadastrando..." : "Cadastrar"}
          </button>
          <button type="button" onClick={() => { setAberto(false); setErro(null); }} className="text-sm text-gray-500 hover:text-gray-700 px-4 py-2 rounded-md hover:bg-gray-100 transition-colors">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}