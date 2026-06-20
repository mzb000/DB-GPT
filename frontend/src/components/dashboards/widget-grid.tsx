import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { DashboardWidget } from "@/types";

interface Props {
  widgets: DashboardWidget[];
}

export function WidgetGrid({ widgets }: Props) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {widgets.map((w) => (
        <Card key={w.id} style={{ gridColumn: `span ${w.width}`, gridRow: `span ${Math.ceil(w.height / 3)}` }}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">{w.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex h-48 items-center justify-center text-sm text-muted-foreground">
              {w.type} widget
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
