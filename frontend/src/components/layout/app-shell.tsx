"use client";

import { useState, useEffect, useCallback } from "react";
import { useTheme } from "next-themes";
import { Sidebar } from "./sidebar";
import { Navbar } from "./navbar";
import { CommandPalette } from "@/components/common/command-palette";
import { ShortcutsDialog } from "@/components/common/shortcuts-dialog";
import { useKeyboardShortcuts } from "@/hooks/use-keyboard-shortcuts";

export function AppShell({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    const stored = localStorage.getItem("sidebar-collapsed");
    if (stored === "true") setCollapsed(true);
  }, []);

  const toggle = useCallback(() => {
    setCollapsed((prev) => {
      localStorage.setItem("sidebar-collapsed", String(!prev));
      return !prev;
    });
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(theme === "dark" ? "light" : "dark");
  }, [theme, setTheme]);

  useKeyboardShortcuts({ onToggleSidebar: toggle, onToggleTheme: toggleTheme });

  return (
    <div className="min-h-screen">
      <Sidebar collapsed={collapsed} onToggle={toggle} />
      <Navbar sidebarWidth={collapsed ? 64 : 224} />
      <CommandPalette />
      <ShortcutsDialog />
      <main
        className="mt-14 p-6 transition-all duration-200"
        style={{ marginLeft: collapsed ? 64 : 224 }}
      >
        {children}
      </main>
    </div>
  );
}
