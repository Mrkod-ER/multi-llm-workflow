import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Multi-LLM Workflow Builder",
  description: "Visual DAG-based orchestration platform for chaining multiple LLM providers into intelligent workflows.",
  keywords: ["LLM", "AI", "workflow", "orchestration", "Ollama", "OpenAI", "DAG"],
  authors: [{ name: "Mrkod-ER" }],
};

export const viewport: Viewport = {
  themeColor: "#0d0b1e",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
