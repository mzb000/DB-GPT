"use client";

import { useState, useEffect } from "react";
import { Sidebar } from "./sidebar";
import { Navbar } from "./navbar";

export function AppShell({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("sidebar-collapsed");
    if (stored === "true") setCollapsed(true);
  }, []);

  const toggle = () => {
    setCollapsed((prev) => {
      localStorage.setItem("sidebar-collapsed", String(!prev));
      return !prev;
    });
  };

  return (
    <div className="min-h-screen">
      <Sidebar collapsed={collapsed} onToggle={toggle} />
      <Navbar sidebarWidth={collapsed ? 64 : 224} />
      <main
        className="mt-14 p-6 transition-all duration-200"
        style={{ marginLeft: collapsed ? 64 : 224 }}
      >
        {children}
      </main>
    </div>
  );
}
