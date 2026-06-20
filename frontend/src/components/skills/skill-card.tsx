import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Trash2 } from "lucide-react";
import type { Skill } from "@/types";

interface Props {
  skill: Skill;
  onRun: () => void;
  onDelete: () => void;
}

export function SkillCard({ skill, onRun, onDelete }: Props) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <CardTitle className="text-base">{skill.name}</CardTitle>
          <Badge variant="secondary">{skill.category}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-sm text-muted-foreground line-clamp-2">{skill.description || skill.prompt_template}</p>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="flex-1" onClick={onRun}>
            <Play className="mr-1 h-3 w-3" /> Run
          </Button>
          <Button variant="ghost" size="icon" onClick={onDelete}>
            <Trash2 className="h-4 w-4 text-destructive" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
