"use client";

import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

const shortcuts = [
  { keys: "Ctrl + K", action: "Open search" },
  { keys: "Ctrl + N", action: "New chat" },
  { keys: "Ctrl + B", action: "Toggle sidebar" },
  { keys: "Ctrl + D", action: "Toggle dark mode" },
  { keys: "?", action: "Show shortcuts" },
];

export function ShortcutsDialog() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handler = () => setOpen(true);
    document.addEventListener("open-shortcuts-dialog", handler);
    return () => document.removeEventListener("open-shortcuts-dialog", handler);
  }, []);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Keyboard Shortcuts</DialogTitle>
        </DialogHeader>
        <div className="space-y-2">
          {shortcuts.map((s) => (
            <div key={s.keys} className="flex items-center justify-between rounded-md border px-3 py-2">
              <span className="text-sm">{s.action}</span>
              <div className="flex gap-1">
                {s.keys.split(" + ").map((key) => (
                  <kbd
                    key={key}
                    className="rounded border bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground"
                  >
                    {key}
                  </kbd>
                ))}
              </div>
            </div>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}
