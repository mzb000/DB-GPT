"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, LineChart, PieChart } from "recharts";

type ChartType = "bar" | "line" | "pie";

interface Props {
  type: ChartType;
  data: Record<string, unknown>[];
  xKey: string;
  yKey: string;
  title?: string;
}

export function ChartContainer({ type, data, xKey, yKey, title }: Props) {
  return (
    <Card>
      {title && <CardHeader className="pb-2"><CardTitle className="text-sm">{title}</CardTitle></CardHeader>}
      <CardContent>
        <div className="h-64">
          {data.length === 0 ? (
            <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No data</div>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
}
