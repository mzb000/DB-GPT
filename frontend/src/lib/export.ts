export function exportCSV(columns: string[], rows: unknown[][], filename: string = "export.csv") {
  const header = columns.map((c) => `"${c.replace(/"/g, '""')}"`).join(",");
  const body = rows
    .map((row) =>
      row.map((cell) => `"${String(cell ?? "").replace(/"/g, '""')}"`).join(",")
    )
    .join("\n");
  const csv = `${header}\n${body}`;
  downloadBlob(csv, filename, "text/csv");
}

export function exportJSON(columns: string[], rows: unknown[][], filename: string = "export.json") {
  const data = rows.map((row) => {
    const obj: Record<string, unknown> = {};
    columns.forEach((col, i) => {
      obj[col] = row[i];
    });
    return obj;
  });
  const json = JSON.stringify(data, null, 2);
  downloadBlob(json, filename, "application/json");
}

function downloadBlob(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
