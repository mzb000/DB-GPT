"use client";

import { Sidebar } from "./sidebar";
import { Navbar } from "./navbar";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <Sidebar />
      <Navbar />
      <main className="ml-56 mt-14 p-6">{children}</main>
    </div>
  );
}
