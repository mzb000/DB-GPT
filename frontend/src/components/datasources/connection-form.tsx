"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DATASOURCE_TYPES } from "@/lib/constants";

interface Props {
  onDone: (ds: { name: string; type: string; config: string; description?: string }) => void;
}

const defaultConfigs: Record<string, Record<string, string>> = {
  postgresql: { host: "localhost", port: "5432", database: "postgres", user: "postgres", password: "" },
  mysql: { host: "localhost", port: "3306", database: "mysql", user: "root", password: "" },
  sqlite: { db_path: "" },
  mssql: { host: "localhost", port: "1433", database: "", user: "sa", password: "" },
};

export function ConnectionForm({ onDone }: Props) {
  const [type, setType] = useState("postgresql");
  const [name, setName] = useState("");
  const [config, setConfig] = useState<Record<string, string>>(defaultConfigs.postgresql);

  const handleTypeChange = (val: string) => {
    setType(val);
    setConfig(defaultConfigs[val] || {});
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name) return;
    onDone({
      name,
      type,
      config: JSON.stringify(config),
      description: `${type} database at ${config.host || config.db_path || ""}`,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label>Name</Label>
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="My Database" required />
      </div>
      <div className="space-y-2">
        <Label>Type</Label>
        <Select value={type} onValueChange={handleTypeChange}>
          <SelectTrigger><SelectValue /></SelectTrigger>
          <SelectContent>
            {DATASOURCE_TYPES.map((t) => (
              <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      {Object.entries(config).map(([key, val]) => (
        <div key={key} className="space-y-2">
          <Label className="capitalize">{key.replace(/_/g, " ")}</Label>
          <Input
            type={key === "password" ? "password" : "text"}
            value={val}
            onChange={(e) => setConfig((prev) => ({ ...prev, [key]: e.target.value }))}
            placeholder={val || `Enter ${key}`}
          />
        </div>
      ))}
      <Button type="submit" className="w-full">Connect</Button>
    </form>
  );
}
