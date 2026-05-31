import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TitanOS - Personal AI Operating System",
  description: "世界上第一个能持续成长的个人AI操作系统",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
