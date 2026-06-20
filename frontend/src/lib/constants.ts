export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const DATASOURCE_TYPES = [
  { value: "postgresql", label: "PostgreSQL" },
  { value: "mysql", label: "MySQL" },
  { value: "sqlite", label: "SQLite" },
  { value: "mssql", label: "SQL Server" },
] as const;

export const NAV_ITEMS = [
  { href: "/chat", label: "Chat", icon: "MessageSquare" },
  { href: "/datasources", label: "Data Sources", icon: "Database" },
  { href: "/queries", label: "Query History", icon: "History" },
  { href: "/skills", label: "Skills", icon: "Zap" },
  { href: "/dashboards", label: "Dashboards", icon: "LayoutDashboard" },
  { href: "/reports", label: "Reports", icon: "FileText" },
  { href: "/settings", label: "Settings", icon: "Settings" },
] as const;
