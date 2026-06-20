"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataTable } from "./data-table";
import { BarChart } from "@/components/charts/bar-chart";

interface Props {
  columns: string[];
  rows: unknown[][];
}

export function ResultViewer({ columns, rows }: Props) {
  const numericCol = columns.find((_, i) => rows.length > 0 && typeof rows[0][i] === "number");
  const catCol = columns.find((c) => c !== numericCol);
  const chartData = catCol && numericCol
    ? rows.map((row) => ({ [catCol]: row[columns.indexOf(catCol)], [numericCol]: row[columns.indexOf(numericCol)] }))
    : [];

  return (
    <Tabs defaultValue="table">
      <TabsList>
        <TabsTrigger value="table">Table</TabsTrigger>
        {chartData.length > 0 && <TabsTrigger value="chart">Chart</TabsTrigger>}
      </TabsList>
      <TabsContent value="table">
        <DataTable columns={columns} rows={rows} />
      </TabsContent>
      {chartData.length > 0 && (
        <TabsContent value="chart">
          <div className="h-72">
            <BarChart data={chartData} xKey={catCol!} yKey={numericCol!} />
          </div>
        </TabsContent>
      )}
    </Tabs>
  );
}
