"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { DashboardWidget } from "@/types";

function MetricWidget({ config }: { config: Record<string, unknown> }) {
  const value = config.value as string || "—";
  const change = config.change as string || "";
  const period = config.period as string || "";
  const color = config.color as string || "green";

  const isPositive = change.startsWith("+") || color === "green";
  const isNegative = change.startsWith("-") || color === "red";

  return (
    <div className="flex h-full flex-col items-center justify-center gap-2">
      <div className="text-3xl font-bold text-primary">{value}</div>
      {change && (
        <div className={`flex items-center gap-1 text-sm font-medium ${isPositive ? "text-green-600" : isNegative ? "text-red-600" : "text-yellow-600"}`}>
          {isPositive ? <TrendingUp className="h-4 w-4" /> : isNegative ? <TrendingDown className="h-4 w-4" /> : <Minus className="h-4 w-4" />}
          {change}
        </div>
      )}
      {period && <div className="text-xs text-muted-foreground">{period}</div>}
    </div>
  );
}

function PieChartWidget({ config }: { config: Record<string, unknown> }) {
  const data = (config.data as Array<{ label: string; value: number }>) || [];
  if (data.length === 0) return <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No data</div>;

  const total = data.reduce((sum, d) => sum + d.value, 0);
  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4", "#84cc16"];

  return (
    <div className="flex h-full items-center gap-6 px-4">
      <svg viewBox="0 0 100 100" className="h-40 w-40 flex-shrink-0">
        {(() => {
          let cumulative = 0;
          return data.map((d, i) => {
            const pct = d.value / total;
            const startAngle = cumulative * 2 * Math.PI;
            cumulative += pct;
            const endAngle = cumulative * 2 * Math.PI;
            const largeArc = pct > 0.5 ? 1 : 0;
            const x1 = 50 + 40 * Math.sin(startAngle);
            const y1 = 50 - 40 * Math.cos(startAngle);
            const x2 = 50 + 40 * Math.sin(endAngle);
            const y2 = 50 - 40 * Math.cos(endAngle);
            return (
              <path
                key={i}
                d={`M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArc} 1 ${x2} ${y2} Z`}
                fill={colors[i % colors.length]}
                stroke="white"
                strokeWidth="0.5"
              />
            );
          });
        })()}
      </svg>
      <div className="flex flex-col gap-1.5">
        {data.map((d, i) => (
          <div key={i} className="flex items-center gap-2 text-xs">
            <div className="h-2.5 w-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: colors[i % colors.length] }} />
            <span className="text-muted-foreground">{d.label}</span>
            <span className="font-medium ml-auto">{d.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BarChartWidget({ config }: { config: Record<string, unknown> }) {
  const queryRef = config.query_ref as string || "";
  return (
    <div className="flex h-full flex-col items-center justify-center gap-2">
      <div className="flex h-32 items-end gap-2">
        {[65, 45, 80, 55, 70, 90, 40, 75, 60, 85].map((h, i) => (
          <div key={i} className="w-6 rounded-t bg-primary/70 transition-all hover:bg-primary" style={{ height: `${h}%` }} />
        ))}
      </div>
      <div className="text-xs text-muted-foreground">{queryRef || "Bar Chart"}</div>
    </div>
  );
}

function LineChartWidget({ config }: { config: Record<string, unknown> }) {
  const queryRef = config.query_ref as string || "";
  const points = [20, 35, 25, 45, 40, 60, 55, 70, 65, 80, 75, 90];
  const pathD = points.map((y, i) => `${i === 0 ? "M" : "L"} ${i * (280 / (points.length - 1))} ${100 - y}`).join(" ");

  return (
    <div className="flex h-full flex-col items-center justify-center gap-2">
      <svg viewBox="0 0 280 100" className="h-32 w-full px-4">
        <path d={pathD} fill="none" stroke="#3b82f6" strokeWidth="2" />
        <path d={`${pathD} L 280 100 L 0 100 Z`} fill="url(#lineGradient)" opacity="0.2" />
        <defs>
          <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
      <div className="text-xs text-muted-foreground">{queryRef || "Line Chart"}</div>
    </div>
  );
}

function AreaChartWidget({ config }: { config: Record<string, unknown> }) {
  return <LineChartWidget config={{ ...config, query_ref: config.query_ref || "Area Chart" }} />;
}

function FunnelChartWidget({ config }: { config: Record<string, unknown> }) {
  const queryRef = config.query_ref as string || "";
  const stages = [
    { label: "Visits", width: 100, value: "285K" },
    { label: "Product View", width: 75, value: "142K" },
    { label: "Add to Cart", width: 50, value: "42K" },
    { label: "Checkout", width: 35, value: "21K" },
    { label: "Purchase", width: 25, value: "11K" },
  ];

  return (
    <div className="flex h-full flex-col items-center justify-center gap-1 px-4">
      {stages.map((s, i) => (
        <div key={i} className="flex w-full items-center gap-2">
          <div className="w-16 text-right text-xs text-muted-foreground">{s.label}</div>
          <div className="flex-1 flex justify-center">
            <div
              className="h-6 rounded bg-primary/70 flex items-center justify-center text-xs text-white font-medium"
              style={{ width: `${s.width}%` }}
            >
              {s.value}
            </div>
          </div>
        </div>
      ))}
      <div className="text-xs text-muted-foreground mt-1">{queryRef || "Conversion Funnel"}</div>
    </div>
  );
}

function TableWidget({ config }: { config: Record<string, unknown> }) {
  const queryRef = config.query_ref as string || "";
  return (
    <div className="flex h-full flex-col items-center justify-center gap-2">
      <div className="w-full overflow-hidden rounded border text-xs">
        <div className="grid grid-cols-4 gap-px bg-muted font-medium">
          <div className="bg-muted p-2">Name</div>
          <div className="bg-muted p-2">Value</div>
          <div className="bg-muted p-2">Change</div>
          <div className="bg-muted p-2">Status</div>
        </div>
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="grid grid-cols-4 gap-px">
            <div className="bg-background p-2 text-muted-foreground">Item {i}</div>
            <div className="bg-background p-2">—</div>
            <div className="bg-background p-2">—</div>
            <div className="bg-background p-2">—</div>
          </div>
        ))}
      </div>
      <div className="text-xs text-muted-foreground">{queryRef || "Data Table"}</div>
    </div>
  );
}

function renderWidget(widget: DashboardWidget) {
  let config: Record<string, unknown> = {};
  try {
    config = JSON.parse(widget.config);
  } catch {}

  switch (widget.type) {
    case "metric":
      return <MetricWidget config={config} />;
    case "pie_chart":
      return <PieChartWidget config={config} />;
    case "bar_chart":
      return <BarChartWidget config={config} />;
    case "line_chart":
      return <LineChartWidget config={config} />;
    case "area_chart":
      return <AreaChartWidget config={config} />;
    case "funnel_chart":
      return <FunnelChartWidget config={config} />;
    case "table":
      return <TableWidget config={config} />;
    default:
      return (
        <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
          {widget.type} widget
        </div>
      );
  }
}

export default function DashboardView() {
  const { id } = useParams();
  const router = useRouter();
  const [dash, setDash] = useState<{ name: string; description: string } | null>(null);
  const [widgets, setWidgets] = useState<DashboardWidget[]>([]);

  useEffect(() => {
    api.get<{ name: string; description: string }>(`/api/v1/dashboards/${id}`).then(setDash);
    api.get<DashboardWidget[]>(`/api/v1/dashboards/${id}/widgets`).then(setWidgets);
  }, [id]);

  if (!dash) return <div className="py-20 text-center text-muted-foreground">Loading...</div>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => router.push("/dashboards")}>
            <ArrowLeft className="mr-1 h-4 w-4" /> Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{dash.name}</h1>
            {dash.description && <p className="text-muted-foreground">{dash.description}</p>}
          </div>
        </div>
      </div>

      {widgets.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-20">
            <p className="text-muted-foreground">This dashboard is empty. Add widgets from query results.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-12 gap-4">
          {widgets.map((w) => (
            <Card key={w.id} className="overflow-hidden" style={{ gridColumn: `span ${Math.min(w.width, 12)}`, minHeight: `${w.height * 60}px` }}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">{w.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <div style={{ height: `${Math.max(w.height * 50, 100)}px` }}>
                  {renderWidget(w)}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
