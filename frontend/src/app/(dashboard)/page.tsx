"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PageHeader } from "@/components/common/page-header";
import {
  Database, History, Zap, LayoutDashboard, FileText,
  MessageSquare, Plus, ArrowRight, Activity,
} from "lucide-react";
import Link from "next/link";

interface Stats {
  datasources: number;
  queries: number;
  skills: number;
  dashboards: number;
  reports: number;
  recent_activity: Array<{
    type: string;
    title: string;
    status: string;
    created_at: string;
  }>;
}

const statCards = [
  { key: "queries", label: "Total Queries", icon: History, color: "text-blue-500", bg: "bg-blue-500/10" },
  { key: "datasources", label: "Data Sources", icon: Database, color: "text-green-500", bg: "bg-green-500/10" },
  { key: "dashboards", label: "Dashboards", icon: LayoutDashboard, color: "text-purple-500", bg: "bg-purple-500/10" },
  { key: "reports", label: "Reports", icon: FileText, color: "text-orange-500", bg: "bg-orange-500/10" },
  { key: "skills", label: "Skills", icon: Zap, color: "text-yellow-500", bg: "bg-yellow-500/10" },
] as const;

const quickActions = [
  { label: "New Chat", href: "/chat", icon: MessageSquare },
  { label: "Add Data Source", href: "/datasources", icon: Plus },
  { label: "View Dashboards", href: "/dashboards", icon: LayoutDashboard },
  { label: "Query History", href: "/queries", icon: History },
];

export default function OverviewPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<Stats>("/api/v1/analytics/stats")
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <PageHeader
        title="Overview"
        description="Your AI data assistant at a glance"
      />

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
          {Array.from({ length: 5 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="pt-6">
                <div className="h-16 animate-pulse rounded bg-muted" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : stats ? (
        <div className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
            {statCards.map((sc) => {
              const Icon = sc.icon;
              const value = stats[sc.key as keyof Stats] as number;
              return (
                <Card key={sc.key}>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">{sc.label}</p>
                        <p className="text-3xl font-bold">{value}</p>
                      </div>
                      <div className={`rounded-lg p-2.5 ${sc.bg}`}>
                        <Icon className={`h-5 w-5 ${sc.color}`} />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Activity className="h-4 w-4" /> Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent>
                {stats.recent_activity.length === 0 ? (
                  <p className="py-8 text-center text-sm text-muted-foreground">
                    No recent activity. Start by asking a question in the chat.
                  </p>
                ) : (
                  <div className="space-y-3">
                    {stats.recent_activity.map((item, i) => (
                      <div key={i} className="flex items-center gap-3 rounded-lg border p-3">
                        <History className="h-4 w-4 shrink-0 text-muted-foreground" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{item.title}</p>
                          <p className="text-xs text-muted-foreground">
                            {item.created_at ? new Date(item.created_at).toLocaleDateString() : ""}
                          </p>
                        </div>
                        <Badge variant={item.status === "completed" ? "success" : "warning"} className="shrink-0">
                          {item.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-3 sm:grid-cols-2">
                  {quickActions.map((action) => {
                    const Icon = action.icon;
                    return (
                      <Link key={action.href} href={action.href}>
                        <Button
                          variant="outline"
                          className="h-auto w-full justify-start gap-3 px-4 py-3"
                        >
                          <Icon className="h-4 w-4 text-primary" />
                          <span className="flex-1 text-left">{action.label}</span>
                          <ArrowRight className="h-3.5 w-3.5 text-muted-foreground" />
                        </Button>
                      </Link>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ) : null}
    </div>
  );
}
