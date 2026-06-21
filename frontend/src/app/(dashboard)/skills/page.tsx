"use client";

import { useState } from "react";
import { useSkills } from "@/hooks/use-skills";
import { useDatasources } from "@/hooks/use-datasources";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, Play, Trash2, Zap } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { PageHeader } from "@/components/common/page-header";
import { FavoriteButton } from "@/components/common/favorite-button";
import { useFavorites } from "@/hooks/use-favorites";
import { SkeletonCardGrid } from "@/components/common/skeleton-card";

export default function SkillsPage() {
  const { skills, loading, create, remove } = useSkills();
  const { isFavorited, toggle } = useFavorites();
  const { datasources } = useDatasources();
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [category, setCategory] = useState("general");
  const [prompt, setPrompt] = useState("");

  const handleCreate = async () => {
    if (!name || !prompt) return;
    await create({ name, prompt_template: prompt, category });
    setName("");
    setPrompt("");
    setOpen(false);
  };

  return (
    <div>
      <PageHeader
        title="Skills"
        description="Reusable analysis templates"
        breadcrumbs={[{ label: "Skills" }]}
        actions={
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button><Plus className="mr-1 h-4 w-4" /> New Skill</Button>
            </DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Create Skill</DialogTitle></DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Monthly Sales Report" />
              </div>
              <div className="space-y-2">
                <Label>Category</Label>
                <Select value={category} onValueChange={setCategory}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">General</SelectItem>
                    <SelectItem value="sales">Sales</SelectItem>
                    <SelectItem value="finance">Finance</SelectItem>
                    <SelectItem value="marketing">Marketing</SelectItem>
                    <SelectItem value="operations">Operations</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>{"Prompt Template (use {param} for variables)"}</Label>
                <textarea
                  className="min-h-[120px] w-full rounded-md border border-input bg-transparent p-3 text-sm"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Write a SQL query to show {metric} by {dimension} for the last {period}"
                />
              </div>
              <Button onClick={handleCreate} className="w-full">Save Skill</Button>
            </div>
          </DialogContent>
        </Dialog>
        }
      />

      {loading ? (
        <SkeletonCardGrid count={6} />
      ) : skills.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-20">
            <Zap className="h-12 w-12 text-muted-foreground/50" />
            <p className="text-muted-foreground">No skills yet. Create your first reusable analysis.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {skills.map((skill) => (
            <Card key={skill.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <CardTitle className="text-base">{skill.name}</CardTitle>
                  <div className="flex items-center gap-1">
                    <Badge variant="secondary">{skill.category}</Badge>
                    <FavoriteButton
                      favorited={isFavorited("skill", skill.id)}
                      onToggle={() => toggle("skill", skill.id)}
                    />
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground line-clamp-2">{skill.description || skill.prompt_template}</p>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Play className="mr-1 h-3 w-3" /> Run
                  </Button>
                  <Button variant="ghost" size="icon" onClick={() => remove(skill.id)}>
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
