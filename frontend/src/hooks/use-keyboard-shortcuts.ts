"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

interface ShortcutHandler {
  onToggleSidebar?: () => void;
  onToggleTheme?: () => void;
}

export function useKeyboardShortcuts({ onToggleSidebar, onToggleTheme }: ShortcutHandler = {}) {
  const router = useRouter();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      const mod = e.ctrlKey || e.metaKey;

      if (mod && e.key === "n") {
        e.preventDefault();
        router.push("/chat");
      }
      if (mod && e.key === "b") {
        e.preventDefault();
        onToggleSidebar?.();
      }
      if (mod && e.key === "d") {
        e.preventDefault();
        onToggleTheme?.();
      }
      if (e.key === "?" && !mod) {
        const event = new CustomEvent("open-shortcuts-dialog");
        document.dispatchEvent(event);
      }
    };

    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [router, onToggleSidebar, onToggleTheme]);
}
