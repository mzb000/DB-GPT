"use client";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface Props {
  columns: string[];
  rows: unknown[][];
  maxRows?: number;
}

export function DataTable({ columns, rows, maxRows = 50 }: Props) {
  const displayRows = rows.slice(0, maxRows);
  return (
    <div>
      <div className="max-h-96 overflow-auto rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((col) => (
                <TableHead key={col} className="whitespace-nowrap bg-muted">{col}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {displayRows.map((row, i) => (
              <TableRow key={i}>
                {row.map((cell, j) => (
                  <TableCell key={j} className="whitespace-nowrap">{String(cell ?? "")}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {rows.length > maxRows && (
        <p className="mt-1 text-xs text-muted-foreground">Showing {maxRows} of {rows.length} rows</p>
      )}
    </div>
  );
}
