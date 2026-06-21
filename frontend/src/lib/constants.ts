export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const DATASOURCE_TYPES = [
  { value: "postgresql", label: "PostgreSQL" },
  { value: "mysql", label: "MySQL" },
  { value: "sqlite", label: "SQLite" },
  { value: "mssql", label: "SQL Server" },
] as const;

export interface NavItem {
  href: string;
  label: string;
  icon: string;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

export const NAV_GROUPS: NavGroup[] = [
  {
    label: "Main",
    items: [
      { href: "/chat", label: "Chat", icon: "MessageSquare" },
    ],
  },
  {
    label: "Data",
    items: [
      { href: "/datasources", label: "Data Sources", icon: "Database" },
      { href: "/queries", label: "Query History", icon: "History" },
    ],
  },
  {
    label: "Tools",
    items: [
      { href: "/skills", label: "Skills", icon: "Zap" },
      { href: "/dashboards", label: "Dashboards", icon: "LayoutDashboard" },
      { href: "/reports", label: "Reports", icon: "FileText" },
    ],
  },
  {
    label: "System",
    items: [
      { href: "/settings", label: "Settings", icon: "Settings" },
    ],
  },
];

export const NAV_ITEMS = NAV_GROUPS.flatMap((g) => g.items);
