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
  const [mobileOpen, setMobileOpen] = useState(false);
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

  const sidebarWidth = collapsed ? 64 : 224;

  return (
    <div className="min-h-screen">
      <Sidebar
        collapsed={collapsed}
        onToggle={toggle}
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
      />
      <Navbar
        sidebarWidth={sidebarWidth}
        onMobileMenuToggle={() => setMobileOpen((o) => !o)}
      />
      <CommandPalette />
      <ShortcutsDialog />
      <main className="mt-14 p-4 transition-all duration-200 md:p-6 md:ml-56" style={{ marginLeft: undefined }}>
        {children}
      </main>
      <style>{`
        @media (min-width: 768px) {
          main { margin-left: ${sidebarWidth}px !important; }
        }
      `}</style>
    </div>
  );
}
