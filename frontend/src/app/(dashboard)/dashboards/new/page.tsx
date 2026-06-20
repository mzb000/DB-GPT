"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";

export default function NewDashboard() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    if (!name) return;
    setLoading(true);
    try {
      const dash = await api.post<{ id: string }>("/api/v1/dashboards/", { name, description: desc });
      router.push(`/dashboards/${dash.id}`);
    } catch {} finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg">
      <Button variant="ghost" size="sm" className="mb-4" onClick={() => router.back()}>
        <ArrowLeft className="mr-1 h-4 w-4" /> Back
      </Button>
      <Card>
        <CardHeader><CardTitle>New Dashboard</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Name</Label>
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Sales Dashboard" />
          </div>
          <div className="space-y-2">
            <Label>Description</Label>
            <Input value={desc} onChange={(e) => setDesc(e.target.value)} placeholder="Key metrics" />
          </div>
          <Button onClick={handleCreate} className="w-full" disabled={loading || !name}>
            {loading ? "Creating..." : "Create Dashboard"}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
