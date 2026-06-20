"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Play } from "lucide-react";
import type { Skill } from "@/types";

export default function SkillDetail() {
  const { id } = useParams();
  const router = useRouter();
  const [skill, setSkill] = useState<Skill | null>(null);

  useEffect(() => {
    api.get<Skill>(`/api/v1/skills/${id}`).then(setSkill);
  }, [id]);

  if (!skill) return <div className="py-20 text-center text-muted-foreground">Loading...</div>;

  return (
    <div className="max-w-3xl">
      <Button variant="ghost" size="sm" className="mb-4" onClick={() => router.back()}>
        <ArrowLeft className="mr-1 h-4 w-4" /> Back
      </Button>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {skill.name}
            <Badge variant="secondary">{skill.category}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm font-medium text-muted-foreground">Description</p>
            <p>{skill.description || "No description"}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Prompt Template</p>
            <pre className="mt-1 rounded-md bg-muted p-3 text-sm whitespace-pre-wrap">{skill.prompt_template}</pre>
          </div>
          <Button><Play className="mr-1 h-4 w-4" /> Run Skill</Button>
        </CardContent>
      </Card>
    </div>
  );
}
