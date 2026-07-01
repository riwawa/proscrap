import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ProScrap",
  description: "Acompanhamento de processos via API Pública DataJud (CNJ)",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="bg-gray-50 text-gray-900 min-h-screen">{children}</body>
    </html>
  );
}