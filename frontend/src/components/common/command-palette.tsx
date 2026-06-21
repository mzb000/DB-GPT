"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import * as VisuallyHidden from "@radix-ui/react-visually-hidden";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api-client";
import {
  Search, Database, History, Zap, LayoutDashboard, FileText,
} from "lucide-react";

interface SearchResult {
  type: string;
  id: string;
  title: string;
  subtitle: string;
}

const typeConfig: Record<string, { icon: React.ReactNode; label: string; href: (id: string) => string }> = {
  datasource: { icon: <Database className="h-4 w-4" />, label: "Data Source", href: () => "/datasources" },
  query: { icon: <History className="h-4 w-4" />, label: "Query", href: () => "/queries" },
  skill: { icon: <Zap className="h-4 w-4" />, label: "Skill", href: () => "/skills" },
  dashboard: { icon: <LayoutDashboard className="h-4 w-4" />, label: "Dashboard", href: (id) => `/dashboards/${id}` },
  report: { icon: <FileText className="h-4 w-4" />, label: "Report", href: () => "/reports" },
};

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const search = useCallback(async (term: string) => {
    if (!term.trim()) {
      setResults([]);
      return;
    }
    setLoading(true);
    try {
      const data = await api.get<SearchResult[]>(`/api/v1/search?q=${encodeURIComponent(term)}`);
      setResults(data);
      setSelectedIndex(0);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => search(query), 300);
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [query, search]);

  const navigate = (result: SearchResult) => {
    const config = typeConfig[result.type];
    if (config) {
      router.push(config.href(result.id));
    }
    setOpen(false);
    setQuery("");
    setResults([]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && results[selectedIndex]) {
      e.preventDefault();
      navigate(results[selectedIndex]);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => { setOpen(o); if (!o) { setQuery(""); setResults([]); } }}>
      <DialogContent className="overflow-hidden p-0 sm:max-w-lg [&>button:last-child]:hidden">
        <VisuallyHidden.Root><DialogTitle>Search</DialogTitle></VisuallyHidden.Root>
        <div className="flex items-center border-b px-3">
          <Search className="mr-2 h-4 w-4 shrink-0 text-muted-foreground" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search data sources, queries, dashboards..."
            className="border-0 px-0 shadow-none focus-visible:ring-0"
            autoFocus
          />
          <kbd className="ml-2 shrink-0 rounded border bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">
            ESC
          </kbd>
        </div>
        <div className="max-h-[300px] overflow-y-auto">
          {loading && (
            <div className="py-6 text-center text-sm text-muted-foreground">Searching...</div>
          )}
          {!loading && query && results.length === 0 && (
            <div className="py-6 text-center text-sm text-muted-foreground">No results found.</div>
          )}
          {!loading && !query && (
            <div className="py-6 text-center text-sm text-muted-foreground">
              Type to search across all your data...
            </div>
          )}
          {results.map((result, i) => {
            const config = typeConfig[result.type];
            return (
              <button
                key={`${result.type}-${result.id}`}
                onClick={() => navigate(result)}
                className={`flex w-full items-center gap-3 px-4 py-2.5 text-left text-sm transition-colors ${
                  i === selectedIndex ? "bg-accent text-accent-foreground" : "hover:bg-accent/50"
                }`}
              >
                <span className="shrink-0 text-muted-foreground">{config?.icon}</span>
                <div className="flex-1 overflow-hidden">
                  <div className="truncate font-medium">{result.title}</div>
                  {result.subtitle && (
                    <div className="truncate text-xs text-muted-foreground">{result.subtitle}</div>
                  )}
                </div>
                <Badge variant="secondary" className="shrink-0 text-[10px]">
                  {config?.label}
                </Badge>
              </button>
            );
          })}
        </div>
      </DialogContent>
    </Dialog>
  );
}
