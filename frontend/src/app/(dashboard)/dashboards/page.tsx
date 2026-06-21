"use client";

import { useState } from "react";
import { useDashboards } from "@/hooks/use-dashboards";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Plus, LayoutDashboard, Trash2, Eye, BarChart3 } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { PageHeader } from "@/components/common/page-header";
import { SkeletonCardGrid } from "@/components/common/skeleton-card";
import Link from "next/link";

export default function DashboardsPage() {
  const { dashboards, loading, create, remove } = useDashboards();
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");

  const handleCreate = async () => {
    if (!name) return;
    await create({ name, description: desc });
    setName("");
    setDesc("");
    setOpen(false);
  };

  return (
    <div>
      <PageHeader
        title="Dashboards"
        description="Custom data dashboards"
        breadcrumbs={[{ label: "Dashboards" }]}
        actions={
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button><Plus className="mr-1 h-4 w-4" /> New Dashboard</Button>
            </DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Create Dashboard</DialogTitle></DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Sales Overview" />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Input value={desc} onChange={(e) => setDesc(e.target.value)} placeholder="Key sales metrics" />
              </div>
              <Button onClick={handleCreate} className="w-full">Create</Button>
            </div>
          </DialogContent>
        </Dialog>
        }
      />

      {loading ? (
        <SkeletonCardGrid count={6} />
      ) : dashboards.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-20">
            <LayoutDashboard className="h-12 w-12 text-muted-foreground/50" />
            <p className="text-muted-foreground">No dashboards yet.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {dashboards.map((d) => (
            <Card key={d.id} className="group">
              <div className="flex h-28 items-center justify-center rounded-t-xl bg-gradient-to-br from-primary/5 to-primary/10 dark:from-primary/10 dark:to-primary/20">
                <BarChart3 className="h-10 w-10 text-primary/40" />
              </div>
              <CardHeader className="pb-2 pt-3">
                <div className="flex items-start justify-between">
                  <CardTitle className="text-base">{d.name}</CardTitle>
                  <Badge variant="secondary" className="text-[10px] shrink-0">
                    <LayoutDashboard className="mr-1 h-2.5 w-2.5" /> Dashboard
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground line-clamp-2">{d.description}</p>
                <p className="text-xs text-muted-foreground">{formatDate(d.created_at)}</p>
                <div className="flex gap-2">
                  <Link href={`/dashboards/${d.id}`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full">
                      <Eye className="mr-1 h-3 w-3" /> View
                    </Button>
                  </Link>
                  <Button variant="ghost" size="icon" onClick={() => remove(d.id)}>
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
