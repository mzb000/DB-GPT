"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { exportCSV, exportJSON } from "@/lib/export";

interface Props {
  columns: string[];
  rows: unknown[][];
}

const COLORS = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4", "#ec4899", "#84cc16"];

function toChartData(columns: string[], rows: unknown[][]) {
  return rows.map((row) => {
    const item: Record<string, unknown> = {};
    columns.forEach((col, i) => { item[col] = row[i]; });
    return item;
  });
}

export function ResultDisplay({ columns, rows }: Props) {
  if (!columns || columns.length === 0) {
    return <p className="text-sm text-muted-foreground">No results</p>;
  }

  const chartData = toChartData(columns, rows);
  const numericCols = columns.filter((_, i) => rows.length > 0 && typeof rows[0][i] === "number");
  const categoryCol = columns.find((c) => !numericCols.includes(c));
  const firstNumeric = numericCols[0];

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Badge variant="secondary">{rows.length} rows</Badge>
        <Badge variant="secondary">{columns.length} columns</Badge>
        <div className="ml-auto flex gap-1">
          <Button variant="ghost" size="sm" className="h-7 gap-1 text-xs" onClick={() => exportCSV(columns, rows)}>
            <Download className="h-3 w-3" /> CSV
          </Button>
          <Button variant="ghost" size="sm" className="h-7 gap-1 text-xs" onClick={() => exportJSON(columns, rows)}>
            <Download className="h-3 w-3" /> JSON
          </Button>
        </div>
      </div>

      <Tabs defaultValue="table">
        <TabsList>
          <TabsTrigger value="table">Table</TabsTrigger>
          {categoryCol && firstNumeric && (
            <>
              <TabsTrigger value="bar">Bar</TabsTrigger>
              <TabsTrigger value="line">Line</TabsTrigger>
              <TabsTrigger value="pie">Pie</TabsTrigger>
            </>
          )}
        </TabsList>

        <TabsContent value="table" className="max-h-96 overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {columns.map((col) => (
                  <TableHead key={col} className="whitespace-nowrap">{col}</TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.slice(0, 50).map((row, i) => (
                <TableRow key={i}>
                  {row.map((cell, j) => (
                    <TableCell key={j} className="whitespace-nowrap">{String(cell ?? "")}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          {rows.length > 50 && <p className="mt-2 text-xs text-muted-foreground">Showing 50 of {rows.length} rows</p>}
        </TabsContent>

        {categoryCol && firstNumeric && (
          <TabsContent value="bar">
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={categoryCol} tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey={firstNumeric} fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        )}

        {categoryCol && firstNumeric && (
          <TabsContent value="line">
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={categoryCol} tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey={firstNumeric} stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        )}

        {categoryCol && firstNumeric && (
          <TabsContent value="pie">
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData} dataKey={firstNumeric} nameKey={categoryCol} cx="50%" cy="50%" outerRadius={100} label>
                    {chartData.map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}
