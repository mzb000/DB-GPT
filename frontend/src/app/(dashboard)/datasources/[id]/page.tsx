"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft } from "lucide-react";
import type { Datasource } from "@/types";

export default function DatasourceDetail() {
  const { id } = useParams();
  const router = useRouter();
  const [ds, setDs] = useState<Datasource | null>(null);

  useEffect(() => {
    api.get<Datasource>(`/api/v1/datasources/${id}`).then(setDs);
  }, [id]);

  if (!ds) return <div className="py-20 text-center text-muted-foreground">Loading...</div>;

  return (
    <div className="max-w-3xl">
      <Button variant="ghost" size="sm" className="mb-4" onClick={() => router.back()}>
        <ArrowLeft className="mr-1 h-4 w-4" /> Back
      </Button>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {ds.name}
            <Badge variant="secondary">{ds.type}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm font-medium text-muted-foreground">Description</p>
            <p>{ds.description || "No description"}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Configuration</p>
            <pre className="mt-1 rounded-md bg-muted p-3 text-sm">{JSON.stringify(JSON.parse(ds.config), null, 2)}</pre>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
